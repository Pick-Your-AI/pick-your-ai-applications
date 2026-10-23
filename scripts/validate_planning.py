#!/usr/bin/env python3
"""Offline taxonomy, hierarchy and coverage integrity; not evidence verification."""
from __future__ import annotations

import json
import math
import datetime as dt
from urllib.parse import urlsplit
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def unique(values, description):
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {description}")


def validate_coverage_receipts(row, as_of):
    """Check scoped receipt metadata, not remote review or actual publication."""
    receipts = row.get('acceptance_receipts', [])
    if not isinstance(receipts, list):
        raise ValueError('coverage acceptance receipts must be a list')
    admitted, seen_urls = set(), set()
    for receipt in receipts:
        required = {'receipt_url', 'artifact_commit', 'consumer_commit', 'product_ids',
                    'category_id', 'reviewer', 'accepted_on'}
        if not isinstance(receipt, dict) or not required <= receipt.keys():
            raise ValueError('published coverage requires structured acceptance receipts')
        locator = receipt['receipt_url']
        if not isinstance(locator, str) or any(ord(c) <= 32 or ord(c) == 127 for c in locator) or '\\' in locator:
            raise ValueError('coverage receipt needs a canonical URL without whitespace or controls')
        parts = urlsplit(locator)
        # Project decisions live in GitHub. Accept a reviewed PR/issue decision
        # or an immutable committed receipt; a general webpage is not a receipt.
        if parts is None or parts.scheme != 'https' or parts.netloc != 'github.com' or parts.query or not re.fullmatch(r'/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(?:(?:pull|issues)/[1-9][0-9]*|blob/[0-9a-f]{40}/[^\s?#]+)', parts.path):
            raise ValueError('coverage receipt needs a canonical GitHub decision or immutable receipt URL')
        if receipt['receipt_url'] in seen_urls:
            raise ValueError('duplicate coverage acceptance receipt')
        seen_urls.add(receipt['receipt_url'])
        if receipt['category_id'] != row['category_id']:
            raise ValueError('coverage receipt category does not match the row')
        if any(not isinstance(receipt[k], str) or not re.fullmatch(r'[0-9a-f]{40}', receipt[k]) for k in ('artifact_commit', 'consumer_commit')):
            raise ValueError('coverage receipts must pin exact artifact and consumer commits')
        if not isinstance(receipt['reviewer'], str) or not receipt['reviewer'].strip():
            raise ValueError('coverage receipt requires a nonempty reviewer')
        try:
            accepted = dt.date.fromisoformat(receipt['accepted_on'])
            if accepted.isoformat() != receipt['accepted_on'] or accepted > as_of:
                raise ValueError()
        except (TypeError, ValueError):
            raise ValueError('coverage receipt requires a real, nonfuture canonical acceptance date') from None
        products = receipt['product_ids']
        if not isinstance(products, list) or not products or any(not isinstance(x, str) or not re.fullmatch(r'app:[a-z0-9][a-z0-9._/-]*', x) for x in products) or len(set(products)) != len(products):
            raise ValueError('coverage receipt requires unique canonical application product IDs')
        admitted.update(products)
    if len(admitted) != row['published_product_count']:
        raise ValueError('published coverage count must equal distinct products supported by acceptance receipts')


def validate_coverage_percentages(row, as_of):
    keys = [key for key in ('coverage_percent', 'coverage_percentage', 'market_coverage_percent') if key in row]
    if not keys:
        return
    scope = row['survey_scope']
    basis = row.get('coverage_basis', {})
    if not scope.get('source_sets') or not isinstance(basis, dict) or not basis.get('denominator_product_ids'):
        raise ValueError('coverage percentage without denominator: enumerate the bounded product universe')
    if not isinstance(scope.get('denominator_definition'), str) or not scope['denominator_definition'].strip() or scope['denominator_definition'].startswith('No source universe'):
        raise ValueError('coverage percentage needs an explicit bounded denominator definition')
    try:
        cutoff = dt.date.fromisoformat(scope['cutoff_date'])
        if cutoff.isoformat() != scope['cutoff_date'] or cutoff > as_of:
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise ValueError('coverage denominator requires a real nonfuture cutoff date') from None
    for key in ('numerator_product_ids', 'denominator_product_ids'):
        values = basis.get(key)
        if not isinstance(values, list) or any(not isinstance(x, str) or not re.fullmatch(r'app:[a-z0-9][a-z0-9._/-]*', x) for x in values) or len(set(values)) != len(values):
            raise ValueError('coverage basis requires unique canonical product ID lists')
    numerator, denominator = set(basis['numerator_product_ids']), set(basis['denominator_product_ids'])
    if not numerator <= denominator or len(numerator) != row['deduplicated_product_count']:
        raise ValueError('coverage numerator must match deduplicated products within the declared denominator')
    expected = 100 * len(numerator) / len(denominator)
    for key in keys:
        value = row[key]
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError('coverage percentage must be a finite number from 0 through 100')
        if not math.isclose(value, expected, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError('coverage percentage disagrees with its explicit numerator and denominator')


def validate(taxonomy, ledger, plan, project, *, as_of=None):
    as_of = as_of or dt.datetime.now(dt.timezone.utc).date()
    categories=taxonomy['categories']; groups=taxonomy['groups']; nodes=plan['nodes']
    category_ids=[c['id'] for c in categories]; group_ids=[g['id'] for g in groups]
    unique(category_ids,'category ID'); unique(group_ids,'domain ID')
    if not categories or not groups:
        raise ValueError('empty taxonomy')
    sub_ids=[]
    for c in categories:
        if c['group_id'] not in group_ids or c['domain_id']!=c['group_id']:
            raise ValueError('orphan category')
        for key in ['inclusion','exclusion','overlap','comparison_fields','research_questions','acceptance_criteria','task_groups','source_discovery_strategy']:
            if not c.get(key):
                raise ValueError(f"missing category {key}")
        for s in c['subcategories']:
            if not s['id'].startswith(c['id']+'.') or not s['name'].strip():
                raise ValueError('invalid subcategory identity')
            sub_ids.append(s['id'])
    unique(sub_ids,'subcategory ID')
    row_ids=[r['category_id'] for r in ledger['rows']]; unique(row_ids,'coverage category')
    if set(row_ids)!=set(category_ids):
        raise ValueError('coverage does not match taxonomy')
    for row in ledger['rows']:
        counts={k:v for k,v in row.items() if k.endswith('_count')}
        if any(type(v) is not int or v<0 for v in counts.values()):
            raise ValueError('coverage counts must be nonnegative integers')
        order=['candidate_sightings_count','deduplicated_product_count','primary_sourced_product_count','reviewed_product_count','publication_eligible_product_count','published_product_count']
        if any(row[a]<row[b] for a,b in zip(order,order[1:])):
            raise ValueError('coverage stage prerequisites violated')
        if row['independently_measured_product_count']>row['primary_sourced_product_count']:
            raise ValueError('independent evidence exceeds sourced coverage')
        if row['research_status']=='not_started' and any(counts.values()):
            raise ValueError('not-started category has research counts')
        validate_coverage_receipts(row, as_of)
        validate_coverage_percentages(row, as_of)
    by_id={n['id']:n for n in nodes}; unique([n['id'] for n in nodes],'native issue ID')
    roots=[n for n in nodes if n['parent_id'] is None]
    if len(roots)!=1 or roots[0]['id']!='APP-PROGRAM':
        raise ValueError('expected single program root')
    if plan['external_parent']['repository']!='Pick-Your-AI/pick-your-ai-research' or plan['external_parent']['number']!=509:
        raise ValueError('wrong external parent')
    expected_parent={'epic':'program','work_package':'epic','task':'work_package'}
    all_ids=list(by_id)
    for n in nodes:
        visited=set(); cur=n
        while cur['parent_id'] is not None:
            if cur['id'] in visited:
                raise ValueError('cyclic parent hierarchy')
            visited.add(cur['id'])
            if cur['parent_id'] not in by_id:
                raise ValueError('orphan native issue')
            cur=by_id[cur['parent_id']]
        if n['kind']!='program' and by_id[n['parent_id']]['kind']!=expected_parent.get(n['kind']):
            raise ValueError('invalid native hierarchy level')
        for key in ['deliverable_paths','scope_in','scope_out','research_questions','acceptance_criteria','priority_rationale','readiness_rationale']:
            if not n.get(key):
                raise ValueError(f"missing issue {key}")
        for p in n['deliverable_paths']:
            if Path(p).is_absolute() or '..' in Path(p).parts:
                raise ValueError('unsafe deliverable path')
        for i,t in enumerate(n['task_groups'],1):
            tid=f"{n['id']}.T{i:02d}"; all_ids.append(tid)
            if not t['title'].strip() or not t['subtasks']:
                raise ValueError('empty checklist task')
            all_ids += [f'{tid}.S{j:02d}' for j,_ in enumerate(t['subtasks'],1)]
        for s in n['subtasks']:
            all_ids.append(s['id'])
            if not s['text'].strip() or s['representation']!='checklist' or s['completed']:
                raise ValueError('invalid initial subtask state')
        for d in n['dependencies']:
            if d['target'].startswith('APP-') and d['target'] not in by_id:
                raise ValueError('unresolved internal dependency')
            if d.get('native_blocker'):
                raise ValueError('initial plan has unapproved native blocker')
        for field in project['fields']:
            if n[field['node_key']] not in field['options']:
                raise ValueError('issue value absent from Project options')
        if plan['status']=='prepared_not_provisioned' and any(n['github'][k] for k in ['number','url','node_id','native_parent_verified','project_item_verified']):
            raise ValueError('unprovisioned plan asserts live GitHub state')
    unique(all_ids,'delivery ID across native issues and checklists')
    actual=dict(Counter(n['kind'] for n in nodes))
    actual.update(native_relationships_internal=len(nodes)-1,checklist_task_groups=sum(len(n['task_groups']) for n in nodes),small_subtasks=sum(sum(len(t['subtasks']) for t in n['task_groups'])+len(n['subtasks']) for n in nodes))
    if actual!=plan['counts']:
        raise ValueError('plan counts do not match records')
    if {n.get('category_id') for n in nodes if n.get('category_id')}!=set(category_ids):
        raise ValueError('category missing native research package')
    return actual


def main():
    files=['taxonomy/taxonomy.json','coverage/ledger.json','planning/backlog.json','planning/project-config.json']
    from validate_applications import load_json
    data=[load_json(ROOT/f) for f in files]
    counts=validate(*data)
    from render_backlog import render_body
    nodes=data[2]['nodes']; by_id={n['id']:n for n in nodes}
    for n in nodes:
        body=ROOT/'planning/issue-bodies'/f"{n['id']}.md"
        if body.read_text()!=render_body(n,by_id):
            raise ValueError(f"stale generated issue body: {n['id']}")
        if re.search(r'- \[[ x]\].*https://github.com/.*/issues/',body.read_text()):
            raise ValueError('native issue link duplicated as checklist')
    print(json.dumps({'validation':'passed','scope':'offline planning integrity, not GitHub creation or product verification','categories':len(data[0]['categories']),'subcategories':sum(len(c['subcategories']) for c in data[0]['categories']),'counts':counts},indent=2))


if __name__=='__main__':
    main()
