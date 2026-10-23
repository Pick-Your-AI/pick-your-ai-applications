#!/usr/bin/env python3
"""Scope-limited, resumable import of the user-approved applications foundation.

Never writes main, overwrites edited issues, reassigns people, changes access,
creates credentials, approves PRs, or claims evidence/publication acceptance.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO = 'Pick-Your-AI/pick-your-ai-applications'
BRANCH = 'contrib/CompleteDotTech/applications-foundation'
INITIAL = 'a30d8579b9228dc692bf47fd0404443ad363a2c0'
BUNDLE_HASH = '679f2d6a336505e72f9851e767ec561ff044ca43fe9e9ffc03c5b1a50b237f8a'
FILES_HASH = 'f8ec36349341b9f515a6414b65e983744186bd5bf8ab23bdabeafc8ecefbafbc'
HERE = Path(__file__).resolve().parent
RECEIPT_PATH = 'planning/GITHUB_ESTABLISHMENT_RECEIPT.json'
RECEIPT = {
    'schema_version': '1.0.0', 'repository': REPO, 'branch': BRANCH,
    'status': 'running', 'issues': {}, 'verified_internal_relationships': [],
    'project_url': 'https://github.com/orgs/Pick-Your-AI/projects/10',
    'project_item_placement': 'not_attempted_by_repository_scoped_import',
    'project_field_population': 'not_attempted_by_repository_scoped_import',
    'external_parent_relationship': 'not_attempted_by_repository_scoped_import',
    'external_parent_url': 'https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509',
    'merge_status': 'not_merged_independent_review_required',
    'research_status': 'not_started_no_real_product_records',
    'validation_workflow': 'requires_user_authenticated_connector_commit',
}


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checkpoint():
    RECEIPT['updated_at'] = dt.datetime.now(dt.timezone.utc).isoformat()
    (HERE / 'receipt.json').write_text(json.dumps(RECEIPT, indent=2) + '\n')


def safe_path(name):
    p = PurePosixPath(name)
    check(isinstance(name, str) and name and not p.is_absolute(), 'Invalid bundle path')
    check('..' not in p.parts and '.' not in p.parts and '\\' not in name,
          'Unsafe bundle path')
    check(p.as_posix() == name and '.git' not in p.parts, 'Non-canonical bundle path')
    return p


def reconstruct():
    packed = b''.join((HERE / f'source.part{i:02d}').read_bytes() for i in range(8))
    check(digest(packed) == BUNDLE_HASH, 'Source bundle integrity mismatch')
    decoder = lzma.LZMADecompressor(memlimit=256 * 1024 * 1024)
    raw = decoder.decompress(packed, max_length=8 * 1024 * 1024)
    check(decoder.eof and not decoder.unused_data, 'Invalid or oversized source bundle')
    sources = json.loads(raw)
    check(isinstance(sources, dict) and len(sources) == 44, 'Unexpected source inventory')
    root = Path(tempfile.mkdtemp(prefix='applications-foundation-'))
    for name, content in sources.items():
        safe_path(name)
        check(isinstance(content, str), 'Non-text source')
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding='utf-8')
    (root / 'planning/issue-bodies').mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, 'scripts/render_backlog.py'], cwd=root, check=True)
    files = {p.relative_to(root).as_posix(): p.read_bytes()
             for p in root.rglob('*') if p.is_file()}
    hashes = {p: digest(data) for p, data in files.items()}
    signature = digest(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode())
    check(len(files) == 182 and signature == FILES_HASH, 'Generated scaffold integrity mismatch')
    for command in [
        [sys.executable, 'scripts/validate_applications.py'],
        [sys.executable, 'scripts/validate_planning.py'],
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
    ]:
        subprocess.run(command, cwd=root, check=True, timeout=180)
    plan = json.loads(files['planning/backlog.json'])
    nodes = plan['nodes']
    check(len(nodes) == 135 and len({n['id'] for n in nodes}) == 135, 'Bad plan inventory')
    seen = set()
    for node in nodes:
        check(node['parent_id'] is None or node['parent_id'] in seen, 'Parent order or cycle invalid')
        check(not node['assignees'], 'Bootstrap must not assign people')
        seen.add(node['id'])
    RECEIPT.update({'source_sha256': BUNDLE_HASH, 'files_manifest_sha256': FILES_HASH,
                    'scaffold_file_count': len(files), 'planned_counts': plan['counts'],
                    'local_validation': 'both_validators_and_60_tests_passed'})
    checkpoint()
    return files, nodes


class GitHub:
    def __init__(self):
        token = os.environ.get('GH_TOKEN')
        check(bool(token), 'GH_TOKEN is absent')
        self.headers = {'Authorization': 'Bearer ' + token,
                        'Accept': 'application/vnd.github+json',
                        'X-GitHub-Api-Version': '2026-03-10',
                        'User-Agent': 'pick-your-ai-applications-authorized-bootstrap'}
        self.last_write = 0.0

    def call(self, path, data=None, method='GET', missing_ok=False):
        # Every endpoint is relative to the one authorized repository.
        check(not path.startswith('/') and '..' not in path and '://' not in path,
              'Invalid API path')
        if method != 'GET':
            time.sleep(max(0.0, 1.3 - (time.monotonic() - self.last_write)))
        request = Request('https://api.github.com/repos/' + REPO + '/' + path,
                          data=None if data is None else json.dumps(data).encode(),
                          headers={**self.headers, 'Content-Type': 'application/json'},
                          method=method)
        try:
            with urlopen(request, timeout=60) as response:
                raw = response.read()
                result = json.loads(raw) if raw else None
        except HTTPError as error:
            if missing_ok and error.code == 404:
                return None
            raw = error.read().decode('utf-8', errors='replace')
            try:
                message = json.loads(raw).get('message', 'GitHub API error')
            except (ValueError, AttributeError):
                message = 'GitHub API error'
            # Stop; no rate-limit or access bypass and no blind write retries.
            raise RuntimeError(f'{method} {path}: HTTP {error.code}: {message}') from None
        finally:
            if method != 'GET':
                self.last_write = time.monotonic()
        return result

    def paged(self, path):
        items = []
        separator = '&' if '?' in path else '?'
        for page in range(1, 101):
            batch = self.call(f'{path}{separator}per_page=100&page={page}')
            check(isinstance(batch, list), 'Expected paginated list')
            items.extend(batch)
            if len(batch) < 100:
                return items
        raise RuntimeError('Pagination safety bound exceeded')


def git_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def publish_files(client, files, message, initial_allowed=False):
    check(BRANCH != 'main', 'Default-branch writes forbidden')
    refpath = 'git/refs/heads/' + BRANCH
    head = client.call('git/ref/heads/' + BRANCH)['object']['sha']
    commit = client.call('git/commits/' + head)
    tree = client.call('git/trees/' + commit['tree']['sha'] + '?recursive=1')
    check(not tree.get('truncated'), 'Truncated remote tree')
    entries = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    changes = []
    for name, data in files.items():
        safe_path(name)
        check(not name.startswith('.github/workflows/'), 'Workflow writes require user connector')
        expected = git_sha(data)
        old = entries.get(name)
        if old and old['sha'] == expected:
            continue
        allowed = initial_allowed and head == INITIAL and name == 'README.md'
        # Only our receipt may be refreshed on subsequent idempotent runs.
        check(old is None or allowed or name == RECEIPT_PATH,
              f'Preserving changed remote file: {name}')
        changes.append({'path': name, 'mode': '100644', 'type': 'blob',
                        'content': data.decode('utf-8')})
    if changes:
        new_tree = client.call('git/trees', {'base_tree': commit['tree']['sha'],
                                          'tree': changes}, 'POST')
        new_commit = client.call('git/commits', {
            'message': message, 'tree': new_tree['sha'], 'parents': [head]}, 'POST')
        check(client.call('git/ref/heads/' + BRANCH)['object']['sha'] == head,
              'Concurrent branch update; preserving it')
        client.call(refpath, {'sha': new_commit['sha'], 'force': False}, 'PATCH')
        head = new_commit['sha']
    current = client.call('git/ref/heads/' + BRANCH)['object']['sha']
    check(current == head, 'Branch readback differs')
    remote = client.call('git/trees/' + head + '?recursive=1')
    check(not remote.get('truncated'), 'Truncated verification tree')
    actual = {x['path']: x['sha'] for x in remote['tree'] if x['type'] == 'blob'}
    check(all(actual.get(p) == git_sha(data) for p, data in files.items()),
          'Published files do not match')
    return head


def issue_index(issues):
    result = {}
    for issue in issues:
        if 'pull_request' in issue:
            continue
        markers = re.findall(r'<!-- plan-id: ([A-Z0-9-]+) -->', issue.get('body') or '')
        check(len(markers) <= 1, 'Multiple plan markers on one issue')
        if markers:
            check(markers[0] not in result, 'Duplicate stable plan ID: ' + markers[0])
            result[markers[0]] = issue
    return result


def issue_matches(node, issue, body):
    check(issue['title'] == f"[{node['id']}] {node['title']}",
          'Preserving changed issue title: ' + node['id'])
    check((issue.get('body') or '').strip() == body.strip(),
          'Preserving changed issue body: ' + node['id'])
    check(issue['state'] == 'open', 'Preserving existing issue state: ' + node['id'])


def provision(client, files, nodes):
    config = json.loads(files['planning/project-config.json'])
    labels = {label['name'] for label in client.paged('labels')}
    for label in config['labels']:
        if label['name'] not in labels:
            client.call('labels', label, 'POST')
    current = issue_index(client.paged('issues?state=all'))
    for position, node in enumerate(nodes, 1):
        key = node['id']
        body = files[f'planning/issue-bodies/{key}.md'].decode()
        if key in current:
            issue = client.call(f"issues/{current[key]['number']}")
            issue_matches(node, issue, body)
            missing_labels = set(node['labels']) - {x['name'] for x in issue['labels']}
            if missing_labels:
                client.call(f"issues/{issue['number']}/labels",
                            {'labels': sorted(missing_labels)}, 'POST')
        else:
            issue = client.call('issues', {'title': f"[{key}] {node['title']}",
                                          'body': body, 'labels': node['labels']}, 'POST')
            current[key] = issue
        RECEIPT['issues'][key] = {k: issue[k] for k in ['id', 'node_id', 'number', 'html_url']}
        checkpoint()
        print(f'Issue {position}/{len(nodes)}: {key} -> #{issue["number"]}', flush=True)
    for node in nodes:
        if node['parent_id'] is None:
            continue
        child = RECEIPT['issues'][node['id']]
        parent = RECEIPT['issues'][node['parent_id']]
        existing = client.call(f"issues/{child['number']}/parent", missing_ok=True)
        if existing is None:
            client.call(f"issues/{parent['number']}/sub_issues",
                        {'sub_issue_id': child['id'], 'replace_parent': False}, 'POST')
            existing = client.call(f"issues/{child['number']}/parent")
        check(existing['id'] == parent['id'], 'Different native parent; no reparenting')
        RECEIPT['verified_internal_relationships'].append({
            'child': node['id'], 'parent': node['parent_id']})
        checkpoint()
        print(f"Native relationship {len(RECEIPT['verified_internal_relationships'])}/134", flush=True)
    final = issue_index(client.paged('issues?state=all'))
    for node in nodes:
        check(node['id'] in final, 'Missing issue at final readback')
        issue = final[node['id']]
        issue_matches(node, issue, files[f"planning/issue-bodies/{node['id']}.md"].decode())
        check(set(node['labels']) <= {x['name'] for x in issue['labels']}, 'Missing required label')
    check(len(RECEIPT['verified_internal_relationships']) == 134, 'Relationship count mismatch')
    RECEIPT['verified_issue_count'] = len(nodes)
    RECEIPT['status'] = 'repository_scaffold_and_native_backlog_verified_not_full_mission_complete'
    checkpoint()
    head = publish_files(client, {RECEIPT_PATH: (HERE / 'receipt.json').read_bytes()},
                         'docs: record verified applications backlog establishment')
    RECEIPT['receipt_commit'] = head
    checkpoint()


def main():
    try:
        files, nodes = reconstruct()
        if '--offline' in sys.argv:
            print('OFFLINE PASS: 182 exact files, 135 issue definitions, 134 internal edges')
            return
        check(os.environ.get('GITHUB_REPOSITORY') == REPO, 'Wrong repository')
        check(os.environ.get('GITHUB_ACTOR') == 'CompleteDotTech', 'Unexpected actor')
        client = GitHub()
        main_before = client.call('git/ref/heads/main')['object']['sha']
        RECEIPT['main_before'] = main_before
        payload = {p: data for p, data in files.items() if not p.startswith('.github/workflows/')}
        RECEIPT['scaffold_commit'] = publish_files(
            client, payload, 'feat: establish applications research taxonomy and delivery foundation',
            initial_allowed=True)
        RECEIPT['published_scaffold_files'] = len(payload)
        checkpoint()
        provision(client, files, nodes)
        RECEIPT['main_after'] = client.call('git/ref/heads/main')['object']['sha']
        RECEIPT['main_unchanged_during_run'] = RECEIPT['main_after'] == main_before
        checkpoint()
        print(json.dumps({k: v for k, v in RECEIPT.items()
                          if k not in ['issues', 'verified_internal_relationships']}, indent=2))
    except Exception as error:
        RECEIPT['status'] = 'stopped_preserving_partial_progress'
        RECEIPT['error'] = str(error)
        checkpoint()
        print('Import stopped: ' + str(error), file=sys.stderr)
        raise


if __name__ == '__main__':
    main()
