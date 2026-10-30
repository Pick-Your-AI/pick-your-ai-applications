#!/usr/bin/env python3
"""Conservative, resumable GitHub bootstrap. Offline dry run unless explicitly applied."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import quote

TARGET = 'Pick-Your-AI/pick-your-ai-applications'
ORG = 'Pick-Your-AI'
PARENT_REPO = 'Pick-Your-AI/pick-your-ai-research'
PARENT_NUMBER = 509
PROJECT_TITLE = 'Pick Your AI — Applications Research'
PROJECT_MARKER = '<!-- bootstrap-id: pick-your-ai-applications-v1 -->'
API_VERSION = '2026-03-10'
MARKER_RE = re.compile(r'<!-- plan-id: (APP-[A-Z0-9.]+) -->')

class BootstrapError(Exception):
    pass


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise BootstrapError(f'Duplicate JSON key {key!r} in {path}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def canonical_body(text):
    return (text or '').replace('\r\n', '\n').rstrip() + '\n'


def index_issues(issues):
    indexed = {}
    for issue in issues:
        if 'pull_request' in issue:
            continue
        markers = MARKER_RE.findall(issue.get('body') or '')
        if len(markers) > 1:
            raise BootstrapError(f'Issue #{issue["number"]} contains multiple plan markers; reconcile manually.')
        if markers:
            key = markers[0]
            if key in indexed:
                raise BootstrapError(f'Duplicate live marker {key}; no issue is deleted or recreated.')
            indexed[key] = issue
    return indexed


def load_plan(root):
    plan = read_json(root / 'planning/backlog.json')
    config = read_json(root / 'planning/project-config.json')
    if plan.get('target_repository') != TARGET or config.get('repository') != TARGET:
        raise BootstrapError('Target must be exactly ' + TARGET)
    if config.get('owner') != ORG or config.get('title') != PROJECT_TITLE:
        raise BootstrapError('Organization/Project title differs from the authorized target.')
    parent = plan.get('external_parent', {})
    if parent.get('repository') != PARENT_REPO or parent.get('number') != PARENT_NUMBER:
        raise BootstrapError('External parent differs from research #509.')
    nodes = plan['nodes']
    by_id = {}
    labels = {label['name'] for label in config['labels']}
    for node in nodes:
        key = node['id']
        if not re.fullmatch(r'APP-[A-Z0-9.]+', key) or key in by_id:
            raise BootstrapError('Invalid or duplicate plan ID: ' + str(key))
        by_id[key] = node
        node['_body'] = canonical_body((root / 'planning/issue-bodies' / (key + '.md')).read_text(encoding='utf-8'))
        if MARKER_RE.findall(node['_body']) != [key]:
            raise BootstrapError('Issue body requires exactly its own marker: ' + key)
        node['_title'] = node.get('github_title', f'[{key}] {node["title"]}')
        if len(node['_title']) > 256:
            raise BootstrapError('Issue title exceeds GitHub limit: ' + key)
        if not set(node.get('labels', [])).issubset(labels):
            raise BootstrapError('Unconfigured labels in ' + key)
        for field in config['fields']:
            if field['type'] != 'SINGLE_SELECT':
                raise BootstrapError('This helper supports the prepared SINGLE_SELECT fields only.')
            if node.get(field['node_key']) not in field['options']:
                raise BootstrapError(f'{key}: invalid {field["name"]} value')
    roots = [n for n in nodes if n.get('parent_id') is None]
    if len(roots) != 1 or roots[0]['id'] != 'APP-PROGRAM':
        raise BootstrapError('Expected exactly APP-PROGRAM as root.')
    for node in nodes:
        seen = set()
        current = node
        while current.get('parent_id') is not None:
            if current['id'] in seen or current['parent_id'] not in by_id:
                raise BootstrapError('Cyclic or unresolved parent at ' + node['id'])
            seen.add(current['id'])
            current = by_id[current['parent_id']]
        if len(seen) + 1 > 7:  # research #509 adds one more level.
            raise BootstrapError('Hierarchy exceeds supported native nesting.')
    for node in nodes:
        if sum(n.get('parent_id') == node['id'] for n in nodes) > 100:
            raise BootstrapError('Too many direct children: ' + node['id'])
    return plan, config


class State:
    def __init__(self, path):
        self.path = path
        self.data = read_json(path) if path.exists() else {'version': 1, 'target': TARGET, 'issues': {}, 'items': {}}
        if self.data.get('target') != TARGET:
            raise BootstrapError('Checkpoint belongs to a different repository.')

    def save(self):
        temp = self.path.with_name(self.path.name + '.tmp')
        temp.write_text(json.dumps(self.data, indent=2) + '\n', encoding='utf-8')
        os.replace(temp, self.path)


def mark_live_plan(root):
    """Protect regeneration even when the durable checkpoint lives elsewhere."""
    marker = root / '.bootstrap-started.json'
    try:
        with marker.open('x', encoding='utf-8') as handle:
            json.dump({'version': 1, 'target': TARGET, 'reason': 'live provisioning requested'}, handle)
            handle.write('\n')
    except FileExistsError:
        if read_json(marker).get('target') != TARGET:
            raise BootstrapError('Local provisioning marker belongs to a different repository.')


class GitHub:
    """gh owns authentication. This code never obtains or prints credential values."""
    def __init__(self, state, apply=False, delay=1.1, max_mutations=0):
        self.state, self.apply = state, apply
        self.delay, self.max_mutations = delay, max_mutations
        self.mutations = 0

    def api(self, endpoint, method='GET', payload=None, mutation=False, missing_ok=False):
        if mutation:
            if not self.apply:
                raise BootstrapError('Mutation attempted in read-only mode.')
            if self.max_mutations and self.mutations >= self.max_mutations:
                raise BootstrapError('Configured mutation budget reached; checkpoint saved. Resume with the same command.')
            self.state.data['pending_action'] = {'method': method, 'endpoint': endpoint, 'mutation_number': self.mutations + 1}
            self.state.save()
            if self.mutations:
                time.sleep(self.delay)
            self.mutations += 1
        args = ['gh', 'api', endpoint, '--hostname', 'github.com', '--method', method,
                '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: ' + API_VERSION]
        if payload is not None:
            args += ['--input', '-']
        try:
            result = subprocess.run(args, input=json.dumps(payload) if payload is not None else None,
                                    text=True, capture_output=True, timeout=60, check=False)
        except FileNotFoundError as exc:
            raise BootstrapError('GitHub CLI gh is not installed; no credential or remote mutation attempted.') from exc
        except subprocess.TimeoutExpired as exc:
            raise BootstrapError('GitHub request timed out. Its outcome may be unknown; resume to reconcile live state before any retry.') from exc
        if result.returncode:
            detail = result.stdout + '\n' + result.stderr
            if missing_ok and (re.search(r'HTTP 404\b', detail) or '"status":"404"' in detail or '"status": "404"' in detail):
                return None
            if 'rate limit' in detail.lower() or 'secondary rate' in detail.lower() or 'HTTP 429' in detail:
                raise BootstrapError('GitHub rate limit stopped this run. Checkpoint retained; wait for GitHub recovery and resume. No automatic retry.')
            match = re.search(r'HTTP (\d{3})\b', detail)
            code = match.group(1) if match else 'CLI error'
            raise BootstrapError(f'GitHub {code} for {method} {endpoint}. Check gh authentication and authorized access; raw credential-bearing diagnostics are not printed.')
        try:
            data = json.loads(result.stdout) if result.stdout.strip() else {}
        except ValueError as exc:
            raise BootstrapError('GitHub returned invalid JSON; preserve checkpoint and inspect access separately.') from exc
        if isinstance(data, dict) and data.get('errors'):
            if any('rate' in str(e).lower() for e in data['errors']):
                raise BootstrapError('GitHub GraphQL rate limit; resume after recovery.')
            codes = [e.get('type', 'GRAPHQL_ERROR') for e in data['errors']]
            raise BootstrapError('GitHub GraphQL returned errors: ' + ', '.join(codes) + '. Partial mutation outcomes will be reconciled on resume.')
        if mutation:
            self.state.data.pop('pending_action', None)
            self.state.save()
        return data

    def graphql(self, query, variables=None, mutation=False):
        return self.api('graphql', 'POST', {'query': query, 'variables': variables or {}}, mutation=mutation)['data']

    def pages(self, endpoint):
        rows, page = [], 1
        while True:
            separator = '&' if '?' in endpoint else '?'
            part = self.api(endpoint + f'{separator}per_page=100&page={page}')
            if not isinstance(part, list):
                raise BootstrapError('Expected paginated array: ' + endpoint)
            rows.extend(part)
            if len(part) < 100:
                return rows
            page += 1


class Provisioner:
    def __init__(self, root, plan, config, gh, state):
        self.root, self.plan, self.config, self.gh, self.state = root, plan, config, gh, state
        self.nodes = plan['nodes']
        self.report = {'target_repository': TARGET, 'mode': 'apply' if gh.apply else 'verify', 'conflicts': [],
                       'views': 'Proposed only; this helper does not configure or verify UI views.',
                       'scaffold_committed': False, 'provisioning_complete': False, 'mission_complete': False}

    def ensure_repo(self):
        repo = self.gh.api('repos/' + TARGET, missing_ok=True)
        if repo is None and self.gh.apply:
            repo = self.gh.api('orgs/' + ORG + '/repos', 'POST', {
                'name': TARGET.split('/')[1], 'description': self.config['description'],
                'private': False, 'has_issues': True, 'auto_init': True}, mutation=True)
            self.state.data['repository_created'] = True
            self.state.save()
            repo = self.gh.api('repos/' + TARGET)
        if repo is None:
            raise BootstrapError('Target repository does not exist or is inaccessible; verification cannot claim completion.')
        if repo.get('full_name', '').lower() != TARGET.lower() or repo.get('private') is not False:
            raise BootstrapError('Existing repository identity/visibility differs; no repository visibility is changed.')
        if repo.get('archived') or not repo.get('has_issues'):
            raise BootstrapError('Target is archived or issues are disabled; settings are preserved.')
        self.repo = repo
        self.report['repository_url'] = repo['html_url']

    def ensure_labels(self):
        existing = {x['name']: x for x in self.gh.pages('repos/' + TARGET + '/labels')}
        for label in self.config['labels']:
            if label['name'] not in existing:
                if not self.gh.apply:
                    self.report['conflicts'].append('Missing label: ' + label['name'])
                    continue
                self.gh.api('repos/' + TARGET + '/labels', 'POST', label, mutation=True)
            # Existing label colors/descriptions are deliberately not overwritten.

    def projects(self):
        rows, cursor, owner_id = [], None, None
        while True:
            data = self.gh.graphql('''query($org:String!,$after:String){organization(login:$org){id projectsV2(first:100,after:$after){nodes{id number title url readme public closed} pageInfo{hasNextPage endCursor}}}}''', {'org': ORG, 'after': cursor})
            owner = data.get('organization')
            if owner is None:
                raise BootstrapError('Organization Projects are inaccessible.')
            owner_id = owner['id']; conn = owner['projectsV2']; rows.extend(conn['nodes'])
            if not conn['pageInfo']['hasNextPage']:
                return owner_id, rows
            cursor = conn['pageInfo']['endCursor']

    def ensure_project(self):
        owner_id, projects = self.projects()
        recorded = self.state.data.get('project', {})
        recorded_id = recorded.get('id') or self.state.data.get('created_project_id')
        recorded_number = recorded.get('number')
        receipt_path = self.root / 'planning/GITHUB_ESTABLISHMENT_RECEIPT.json'
        if receipt_path.exists():
            receipt = read_json(receipt_path)
            match = re.fullmatch(r'https://github\.com/orgs/Pick-Your-AI/projects/([1-9][0-9]*)', receipt.get('project_url', ''))
            if receipt.get('repository') != TARGET or match is None:
                raise BootstrapError('Invalid recorded Project identity; refusing discovery or creation.')
            receipt_number = int(match.group(1))
            if recorded_number is not None and recorded_number != receipt_number:
                raise BootstrapError('Checkpoint and receipt Project identities conflict; preserved without changes.')
            recorded_number = receipt_number
        has_recorded_identity = recorded_id is not None or recorded_number is not None
        if has_recorded_identity:
            matching = [p for p in projects if
                        (recorded_id is None or p['id'] == recorded_id) and
                        (recorded_number is None or p['number'] == recorded_number)]
            if not matching:
                raise BootstrapError('Recorded organization Project is inaccessible; refusing duplicate creation.')
        else:
            matching = [p for p in projects if p['title'] == PROJECT_TITLE or PROJECT_MARKER in (p.get('readme') or '')]
        if len(matching) > 1:
            raise BootstrapError('Multiple matching Projects; refusing duplicate creation or arbitrary selection.')
        project = matching[0] if matching else None
        if project is None and self.gh.apply:
            project = self.gh.graphql('''mutation($input:CreateProjectV2Input!){createProjectV2(input:$input){projectV2{id number title url readme public closed}}}''', {'input': {'ownerId': owner_id, 'title': PROJECT_TITLE}}, mutation=True)['createProjectV2']['projectV2']
            self.state.data['created_project_id'] = project['id']; self.state.save()
        if project is None:
            raise BootstrapError('Dedicated organization Project is missing.')
        if project['closed'] or (not has_recorded_identity and project['title'] != PROJECT_TITLE):
            raise BootstrapError('Matching Project is renamed or closed; preserved without changes.')
        if project['title'] != PROJECT_TITLE:
            self.report['project_title_drift'] = {'prepared_title': PROJECT_TITLE, 'observed_title': project['title']}
        own_new = self.state.data.get('created_project_id') == project['id']
        if own_new and self.gh.apply and not (project.get('readme') or ''):
            self.gh.graphql('''mutation($input:UpdateProjectV2Input!){updateProjectV2(input:$input){projectV2{id}}}''', {'input': {'projectId': project['id'], 'readme': PROJECT_MARKER + '\n\n' + self.config['description'], 'shortDescription': self.config['description'], 'public': bool(self.config.get('public', False))}}, mutation=True)
            _, current = self.projects(); project = next(p for p in current if p['id'] == project['id'])
        if project['public'] != self.config.get('public', False):
            raise BootstrapError('Existing Project visibility differs. Visibility/access settings of preexisting Projects are preserved.')
        self.project = project
        self.report['project_url'] = project['url']
        self.state.data['project'] = {k: project[k] for k in ['id', 'number', 'url']}; self.state.save()

    def linked_repositories(self):
        result, cursor = set(), None
        while True:
            data = self.gh.graphql('query($id:ID!,$after:String){node(id:$id){...on ProjectV2{repositories(first:100,after:$after){nodes{id nameWithOwner} pageInfo{hasNextPage endCursor}}}}}', {'id': self.project['id'], 'after': cursor})
            conn = data['node']['repositories']
            result.update(r['id'] for r in conn['nodes'])
            if not conn['pageInfo']['hasNextPage']:
                return result
            cursor = conn['pageInfo']['endCursor']

    def ensure_repository_link(self):
        repo_id = self.repo['node_id']
        if repo_id not in self.linked_repositories():
            if not self.gh.apply:
                raise BootstrapError('Project is not linked to the applications repository.')
            self.gh.graphql('mutation($input:LinkProjectV2ToRepositoryInput!){linkProjectV2ToRepository(input:$input){repository{id}}}', {'input': {'projectId': self.project['id'], 'repositoryId': repo_id}}, mutation=True)
            if repo_id not in self.linked_repositories():
                raise BootstrapError('Project repository link readback failed.')
        self.report['project_repository_link_verified'] = True

    def fields(self):
        rows, cursor = [], None
        while True:
            data = self.gh.graphql('''query($id:ID!,$after:String){node(id:$id){...on ProjectV2{fields(first:100,after:$after){nodes{...on ProjectV2Field{id name dataType} ...on ProjectV2SingleSelectField{id name dataType options{id name color description}} ...on ProjectV2IterationField{id name dataType} ...on ProjectV2MultiSelectField{id name dataType}} pageInfo{hasNextPage endCursor}}}}}''', {'id': self.project['id'], 'after': cursor})
            conn = data['node']['fields']; rows.extend(conn['nodes'])
            if not conn['pageInfo']['hasNextPage']:
                break
            cursor = conn['pageInfo']['endCursor']
        result = {}
        for field in rows:
            if field['name'] in result:
                raise BootstrapError('Duplicate Project field name: ' + field['name'])
            result[field['name']] = field
        return result

    def ensure_fields(self):
        fields = self.fields()
        for desired in self.config['fields']:
            field = fields.get(desired['name'])
            if field is None:
                if not self.gh.apply:
                    raise BootstrapError('Missing Project field: ' + desired['name'])
                self.gh.graphql('''mutation($input:CreateProjectV2FieldInput!){createProjectV2Field(input:$input){projectV2Field{...on ProjectV2SingleSelectField{id}}}}''', {'input': {'projectId': self.project['id'], 'dataType': 'SINGLE_SELECT', 'name': desired['name'], 'singleSelectOptions': [{'name': name, 'color': 'GRAY', 'description': ''} for name in desired['options']]}}, mutation=True)
                fields = self.fields(); field = fields[desired['name']]
            if field.get('dataType') != 'SINGLE_SELECT':
                raise BootstrapError('Existing Project field type differs: ' + desired['name'])
            options = {o['name']: o for o in field['options']}
            if len(options) != len(field['options']):
                raise BootstrapError('Duplicate option names in ' + desired['name'])
            missing = [name for name in desired['options'] if name not in options]
            if missing:
                if not self.gh.apply:
                    raise BootstrapError('Missing Project options: ' + desired['name'] + ': ' + ', '.join(missing))
                # Preserve existing option IDs; never replace an existing option or clear item values.
                merged = [{k: o[k] for k in ['id', 'name', 'color', 'description']} for o in field['options']]
                merged.extend({'name': name, 'color': 'GRAY', 'description': ''} for name in missing)
                self.gh.graphql('''mutation($input:UpdateProjectV2FieldInput!){updateProjectV2Field(input:$input){projectV2Field{...on ProjectV2SingleSelectField{id}}}}''', {'input': {'fieldId': field['id'], 'singleSelectOptions': merged}}, mutation=True)
                fields = self.fields()
        self.field_map = fields

    def all_issues(self):
        return index_issues(self.gh.pages('repos/' + TARGET + '/issues?state=all&sort=created&direction=desc'))

    def check_issue(self, node, issue):
        differences = []
        if issue['title'] != node['_title']:
            differences.append('title')
        if canonical_body(issue.get('body')) != node['_body']:
            differences.append('body')
        if issue['state'] != 'open':
            differences.append('state')
        labels = {x['name'] for x in issue.get('labels', [])}
        if not set(node.get('labels', [])).issubset(labels):
            differences.append('labels')
        if differences:
            raise BootstrapError(f'{node["id"]} existing #{issue["number"]} differs in {", ".join(differences)}; preserved. Reconcile plan and live progress before resuming.')

    def ensure_issues(self):
        current = self.all_issues()
        for node in self.nodes:
            key = node['id']; issue = current.get(key)
            if issue is None and self.gh.apply:
                # Reconcile immediately before each create, including lost-response retries.
                current = self.all_issues(); issue = current.get(key)
                if issue is None:
                    issue = self.gh.api('repos/' + TARGET + '/issues', 'POST', {'title': node['_title'], 'body': node['_body'], 'labels': node.get('labels', [])}, mutation=True)
                    issue = self.gh.api('repos/' + TARGET + '/issues/' + str(issue['number']))
                    current[key] = issue
            if issue is None:
                raise BootstrapError('Missing issue: ' + key)
            self.check_issue(node, issue)
            self.state.data['issues'][key] = {k: issue[k] for k in ['id', 'node_id', 'number', 'html_url']}
            self.state.save()
        current = self.all_issues()
        for node in self.nodes:
            if node['id'] not in current:
                raise BootstrapError('Issue disappeared during readback: ' + node['id'])
            self.check_issue(node, current[node['id']])
        self.issue_map = current
        self.report['issues_verified'] = len(self.nodes)

    def ensure_parents(self):
        external = self.gh.api(f'repos/{PARENT_REPO}/issues/{PARENT_NUMBER}')
        if 'pull_request' in external:
            raise BootstrapError('External parent unexpectedly resolves to a pull request.')
        count = 0
        for node in self.nodes:
            child = self.issue_map[node['id']]
            parent = self.issue_map[node['parent_id']] if node.get('parent_id') else external
            parent_repo = TARGET if node.get('parent_id') else PARENT_REPO
            endpoint = f'repos/{TARGET}/issues/{child["number"]}/parent'
            current = self.gh.api(endpoint, missing_ok=True)
            if current is None and self.gh.apply:
                # No replace_parent: another controller's parent will not be displaced.
                self.gh.api(f'repos/{parent_repo}/issues/{parent["number"]}/sub_issues', 'POST', {'sub_issue_id': child['id'], 'replace_parent': False}, mutation=True)
                current = self.gh.api(endpoint)
            if current is None or current['id'] != parent['id']:
                raise BootstrapError('Missing or conflicting native parent: ' + node['id'])
            count += 1
            self.state.data['issues'][node['id']]['native_parent_id'] = parent['id']; self.state.save()
        self.report['native_parent_relationships_verified'] = count

    def items(self):
        result, cursor = {}, None
        while True:
            data = self.gh.graphql('''query($id:ID!,$after:String){node(id:$id){...on ProjectV2{items(first:100,after:$after,archivedStates:[ARCHIVED,NOT_ARCHIVED]){nodes{id isArchived content{...on Issue{id number repository{nameWithOwner}}} fieldValues(first:100){nodes{...on ProjectV2ItemFieldSingleSelectValue{name optionId field{...on ProjectV2SingleSelectField{id name}}}} pageInfo{hasNextPage}}} pageInfo{hasNextPage endCursor}}}}}''', {'id': self.project['id'], 'after': cursor})
            conn = data['node']['items']
            for item in conn['nodes']:
                content = item.get('content')
                if not content or not content.get('id') or content.get('repository', {}).get('nameWithOwner', '').lower() != TARGET.lower():
                    continue
                if item['fieldValues']['pageInfo']['hasNextPage']:
                    raise BootstrapError('Project item exceeds field readback page; refusing partial verification.')
                if content['id'] in result:
                    raise BootstrapError('Duplicate Project item for issue: ' + str(content['number']))
                result[content['id']] = item
            if not conn['pageInfo']['hasNextPage']:
                return result
            cursor = conn['pageInfo']['endCursor']

    def item_snapshot(self, item_id):
        data = self.gh.graphql('query($id:ID!){node(id:$id){...on ProjectV2Item{id isArchived fieldValues(first:100){nodes{...on ProjectV2ItemFieldSingleSelectValue{name optionId field{...on ProjectV2SingleSelectField{id name}}}} pageInfo{hasNextPage}}}}}', {'id': item_id})
        item = data.get('node')
        if not item or item['fieldValues']['pageInfo']['hasNextPage']:
            raise BootstrapError('Project item disappeared or field readback is incomplete.')
        return item

    def ensure_items(self):
        current = self.items()
        for node in self.nodes:
            issue_id = self.issue_map[node['id']]['node_id']; item = current.get(issue_id)
            if item is None and self.gh.apply:
                # addProjectV2ItemById returns the existing item if it is already present.
                self.gh.graphql('''mutation($input:AddProjectV2ItemByIdInput!){addProjectV2ItemById(input:$input){item{id}}}''', {'input': {'projectId': self.project['id'], 'contentId': issue_id}}, mutation=True)
                current = self.items(); item = current.get(issue_id)
            if item is None:
                raise BootstrapError('Missing Project item: ' + node['id'])
            item = self.item_snapshot(item['id'])  # Refresh immediately before deciding any field mutation.
            if item.get('isArchived'):
                raise BootstrapError('Project item is archived; preserving live progress: ' + node['id'])
            values = {v['field']['name']: v for v in item['fieldValues']['nodes'] if v.get('field')}
            updates = []
            for desired in self.config['fields']:
                name = desired['name']; expected = node[desired['node_key']]; actual = values.get(name)
                if actual and actual['name'] != expected:
                    raise BootstrapError(f'{node["id"]} Project {name} is {actual["name"]!r}, expected initial {expected!r}; preserving live triage/progress.')
                if actual is None:
                    field = self.field_map[name]
                    option = next((o for o in field['options'] if o['name'] == expected), None)
                    if option is None:
                        raise BootstrapError('Project option disappeared; refresh and reconcile.')
                    updates.append({'projectId': self.project['id'], 'itemId': item['id'], 'fieldId': field['id'], 'value': {'singleSelectOptionId': option['id']}})
            if updates:
                if not self.gh.apply:
                    raise BootstrapError('Missing Project field values: ' + node['id'])
                declarations = ','.join(f'$v{i}:UpdateProjectV2ItemFieldValueInput!' for i in range(len(updates)))
                selections = ' '.join(f'u{i}:updateProjectV2ItemFieldValue(input:$v{i}){{projectV2Item{{id}}}}' for i in range(len(updates)))
                self.gh.graphql('mutation(' + declarations + '){' + selections + '}', {f'v{i}': value for i, value in enumerate(updates)}, mutation=True)
            self.state.data['items'][node['id']] = item['id']; self.state.save()
        # Independent readback checks every field after all mutations.
        current = self.items()
        for node in self.nodes:
            item = current[self.issue_map[node['id']]['node_id']]
            values = {v['field']['name']: v['name'] for v in item['fieldValues']['nodes'] if v.get('field')}
            for field in self.config['fields']:
                if values.get(field['name']) != node[field['node_key']]:
                    raise BootstrapError('Project field readback mismatch: ' + node['id'] + ' / ' + field['name'])
        self.report['project_items_verified'] = len(self.nodes)
        self.report['project_values_verified'] = len(self.nodes) * len(self.config['fields'])

    def verify_scaffold(self, commit):
        if not commit:
            self.report['scaffold_status'] = 'Not verified: supply --scaffold-commit after normal reviewed scaffold delivery. Auto-init README is not the scaffold.'
            return
        if not re.fullmatch(r'[0-9a-fA-F]{40}', commit):
            raise BootstrapError('--scaffold-commit must be an exact 40-character Git commit SHA.')
        commit = commit.lower()
        remote = self.gh.api(f'repos/{TARGET}/commits/{commit}')
        comparison = self.gh.api(f'repos/{TARGET}/compare/{commit}...{quote(self.repo["default_branch"], safe="")}')
        if comparison['status'] not in ('identical', 'ahead'):
            raise BootstrapError('Scaffold commit is not reachable from the current default branch.')
        tree = self.gh.api(f'repos/{TARGET}/git/trees/{remote["commit"]["tree"]["sha"]}?recursive=1')
        if tree.get('truncated'):
            raise BootstrapError('Scaffold tree readback truncated; no completeness claim.')
        remote_files = {entry['path']: entry['sha'] for entry in tree['tree'] if entry['type'] == 'blob'}
        checked = 0
        excluded = {'.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache'}
        state_names = {self.state.path.name, self.state.path.name + '.tmp', self.state.path.name + '.lock', '.bootstrap-started.json'}
        for path in sorted(self.root.rglob('*')):
            rel = path.relative_to(self.root)
            if any(part in excluded for part in rel.parts) or path.name in state_names or path.suffix == '.pyc':
                continue
            if path.is_symlink():
                raise BootstrapError('Scaffold contains a symlink; inspect it before claiming exact file verification: ' + str(rel))
            if not path.is_file():
                continue
            payload = path.read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
            if remote_files.get(rel.as_posix()) != digest:
                raise BootstrapError('Scaffold file does not match supplied committed revision: ' + rel.as_posix())
            checked += 1
        self.report.update(scaffold_committed=True, scaffold_commit=commit, scaffold_files_verified=checked,
                           scaffold_status='Local scaffold bytes match the supplied immutable commit reachable from the default branch; this does not fabricate review approval.')

    def run(self, commit=None):
        self.ensure_repo(); self.ensure_labels(); self.ensure_project(); self.ensure_repository_link(); self.ensure_fields()
        self.ensure_issues(); self.ensure_parents(); self.ensure_items(); self.verify_scaffold(commit)
        self.report['provisioning_complete'] = not self.report['conflicts']
        # UI views, access/review policy enforcement and independent research acceptance are outside this helper.
        self.report['mission_complete'] = False
        self.report['remaining'] = ['Configure and read back proposed Project views.', 'Verify team/review policy through the authorized owner; this helper never grants access or bypasses review.', 'Research work remains open; scaffolding is not completed product research.']
        if not self.report['scaffold_committed']:
            self.report['remaining'].insert(0, 'Deliver and independently review the full scaffold; rerun --verify --scaffold-commit SHA.')
        self.state.data.pop('pending_action', None)
        self.state.data.pop('last_error', None)
        self.state.data['last_report'] = self.report; self.state.save()
        return self.report


@contextlib.contextmanager
def locked(path):
    try:
        import fcntl
    except ImportError as exc:
        raise BootstrapError('This helper requires POSIX advisory locking; run on Linux/macOS to avoid concurrent controllers.') from exc
    with path.open('a+', encoding='utf-8') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BootstrapError('Another bootstrap process holds the checkpoint lock.') from exc
        yield


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true', help='Explicitly create missing authorized GitHub resources.')
    mode.add_argument('--verify', action='store_true', help='Read live GitHub state without remote mutations.')
    parser.add_argument('--state', type=Path, help='Durable local checkpoint; default ROOT/.bootstrap-state.json')
    parser.add_argument('--scaffold-commit', help='Exact normally reviewed scaffold commit to verify against local files/default branch.')
    parser.add_argument('--mutation-delay', type=float, default=1.1)
    parser.add_argument('--max-mutations', type=int, default=0, help='Optional per-run checkpoint budget; 0 means no local budget.')
    args = parser.parse_args(argv)
    root = args.root.resolve(); state = None
    try:
        if args.mutation_delay < 1 or args.mutation_delay > 60 or args.max_mutations < 0:
            raise BootstrapError('Mutation delay must be 1–60 seconds; mutation budget must be nonnegative.')
        plan, config = load_plan(root)
        if not args.apply and not args.verify:
            print(json.dumps({'mode': 'offline_dry_run', 'remote_calls': 0, 'target': TARGET,
                              'project_title': PROJECT_TITLE, 'issues': len(plan['nodes']),
                              'native_parent_relationships': len(plan['nodes']), 'project_fields': len(config['fields']),
                              'project_values': len(plan['nodes']) * len(config['fields']),
                              'labels': [x['name'] for x in config['labels']],
                              'views': 'Proposed only; not configured by this helper.',
                              'next': 'Use --apply only with authorized gh authentication. Resume with the same checkpoint after interruption.',
                              'mission_complete': False}, indent=2))
            return 0
        state_path = (args.state or root / '.bootstrap-state.json').resolve()
        with locked(state_path.with_name(state_path.name + '.lock')):
            state = State(state_path)
            if args.apply:
                mark_live_plan(root)
            gh = GitHub(state, args.apply, args.mutation_delay, args.max_mutations)
            runner = Provisioner(root, plan, config, gh, state)
            report = runner.run(args.scaffold_commit)
            print(json.dumps(report, indent=2))
            return 0 if report['provisioning_complete'] and report['scaffold_committed'] else 2
    except (BootstrapError, OSError, ValueError, KeyError) as exc:
        if state:
            state.data['last_error'] = str(exc); state.save()
        print(json.dumps({'status': 'incomplete', 'reason': str(exc), 'checkpoint': str(state.path) if state else None,
                          'mission_complete': False, 'remote_changes_rolled_back': False}, indent=2), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
