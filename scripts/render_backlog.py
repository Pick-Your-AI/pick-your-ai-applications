#!/usr/bin/env python3
"""Render authored research planning sources; this never creates GitHub objects."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def guard_regeneration(root):
    """Never erase live identifiers or overwrite a plan after provisioning starts."""
    if (root/'.bootstrap-state.json').exists():
        raise ValueError('provisioning state exists; reconcile the live plan before regeneration')
    path=root/'planning/backlog.json'
    if path.exists():
        old=json.loads(path.read_text())
        if old.get('status')!='prepared_not_provisioned' or any(any(n.get('github',{}).values()) for n in old.get('nodes',[])):
            raise ValueError('live GitHub state exists; refuse to reset identifiers or status')


def base_node(identifier, title, kind, parent, workstream, priority="High"):
    return {
        "id": identifier, "title": title, "kind": kind, "parent_id": parent,
        "representation": "native_issue", "workstream": workstream,
        "work_type": {"program":"Program","epic":"Epic","work_package":"Research","task":"Task"}[kind],
        "labels": ["type: " + {"program":"program","epic":"epic","work_package":"research","task":"task"}[kind]],
        "status": "Backlog", "priority": priority,
        "priority_rationale": "Sequencing judgment for the research plan; not a product score.",
        "readiness": "Ready",
        "readiness_rationale": "Meaningful bounded research or planning can start from current methods. Final acceptance may need receiving review.",
        "research_confidence": "Unverified", "dependency_status": "Unblocked",
        "assignees": [], "review_roles": ["Independent application research reviewer"],
        "scope_in": [], "scope_out": ["Frozen builder contract changes", "Website or pipeline runtime implementation", "Unsupported product or publication claims"],
        "deliverable_paths": [], "research_questions": [], "acceptance_criteria": [],
        "dependencies": [], "task_groups": [], "subtasks": [],
        "github": {"number": None, "url": None, "node_id": None, "native_parent_verified": False, "project_item_verified": False},
    }


def render_body(n, by_id):
    lines = [f"<!-- plan-id: {n['id']} -->", f"# {n['title']}", "", "## User decision", "", n.get("user_decision", n["title"]), "",
             "**State:** planned research. This issue does not establish verified product capabilities, publication rights, completed research or a delivered website.", "",
             "## Scope", "", "### Included", ""]
    lines += ["- " + s for s in n["scope_in"]]
    lines += ["", "### Excluded / existing owners", ""] + ["- " + s for s in n["scope_out"]]
    lines += ["", "## Deliverables", ""] + [f"- `{p}`" for p in n["deliverable_paths"]]
    lines += ["", "## Research questions", ""] + ["- " + q for q in n["research_questions"]]
    lines += ["", "## Evidence and comparison rules", "",
              "Use dated primary sources and the application contract. Bind claims to the exact product, release/channel, plan, platform, region and other applicable conditions. Preserve Unknown; source checked is not independently verified. Review, source-use eligibility and consumer delivery are separate. Record vendor statements, independent measurements and estimates distinctly."]
    if n.get("comparison_fields"):
        lines += ["", "Category comparison fields:", ""] + ["- " + f for f in n["comparison_fields"]]
    if n.get("subcategories"):
        lines += ["", "Research territories (not verified capabilities):", ""] + [f"- {s['id']}: {s['name']}" for s in n["subcategories"]]
    if n.get("task_groups"):
        lines += ["", "## Tasks and small subtasks", ""]
        for i, task in enumerate(n["task_groups"], 1):
            lines += [f"- [ ] {n['id']}.T{i:02d}: {task['title']}"]
            lines += [f"  - [ ] {n['id']}.T{i:02d}.S{j:02d}: {s}" for j,s in enumerate(task['subtasks'],1)]
    if n.get("subtasks"):
        lines += ["", "## Small subtasks", ""]
        lines += [f"- [ ] {s['id']}: {s['text']}" for s in n["subtasks"]]
    children = [x["id"] for x in by_id.values() if x["parent_id"] == n["id"]]
    if children:
        lines += ["", "## Native delivery hierarchy", "", f"{len(children)} independently reviewable child outcomes are defined in `planning/backlog.json` and must be attached through GitHub's native sub-issue relationship. Their canonical issue records carry the work; do not duplicate those children as body checkboxes."]
    lines += ["", "## Dependencies and receiving handoffs", ""]
    if n["parent_id"]:
        lines += [f"Planning parent: `{n['parent_id']}`. Use the native parent relationship after provisioning.", ""]
    lines += ["Parent scope: [research #509 / G12](https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509). Existing T1/T4 and market research remain canonical for their own records.", ""]
    for dep in n["dependencies"]:
        lines += [f"- **{dep['kind']}** — `{dep['target']}`: {dep['rationale']} Native blocker: {'yes' if dep.get('native_blocker') else 'no'}."]
    lines += ["", "## Acceptance criteria", ""] + ["- [ ] " + a for a in n["acceptance_criteria"]]
    lines += ["", "## Ownership and triage", "", "Live GitHub Assignees are authoritative. No personal assignment or receiving approval is implied. The dedicated Project owns status, priority, readiness and workstream; this plan supplies initial rationale only.", "", f"Priority rationale: {n['priority_rationale']}", "", f"Readiness rationale: {n['readiness_rationale']}", "", "Keep partial work open. Close only after the scoped decision record is merged, acceptance is met and required receiving decisions are recorded at exact revisions.", ""]
    return "\n".join(lines)


def main():
    guard_regeneration(ROOT)
    taxonomy=json.loads((ROOT/'taxonomy/taxonomy.json').read_text())
    foundations=json.loads((ROOT/'planning/foundation-backlog.json').read_text())
    nodes=[]
    program=base_node('APP-PROGRAM','Evidence-backed AI applications directory research program','program',None,'Program','Critical')
    program.update(user_decision='Which AI software applications and software-delivered services can users compare using scoped, source-linked and independently reviewable evidence?',scope_in=['Eight application research domains and the versioned taxonomy','Application identity, evidence, commercial terms, trust, coverage, maintenance and consumer handoffs','Native delivery hierarchy and explicit task/subtask acceptance'],deliverable_paths=['taxonomy/taxonomy.json','coverage/ledger.json','planning/backlog.json','docs/HANDOFFS.md'],research_questions=['What is the declared research universe and what remains unexamined?','Which independently reviewed application facts can be published for each intended use?'],acceptance_criteria=['All native child outcomes satisfy their own scoped acceptance and required receiving reviews.','Coverage reports bounded denominators, actual records, unknowns and duplication rather than a global exhaustive percentage.','Every eligible consumer projection links exact research/evidence/rights revisions and an actual receiving decision.','Research completion, independent product verification, artifact release and website delivery are reported separately.'])
    nodes.append(program)
    domain_ids={g['id']:f'APP-D{i:02d}' for i,g in enumerate(taxonomy['groups'],1)}
    for g in taxonomy['groups']:
        epic=base_node(domain_ids[g['id']],g['name'],'epic','APP-PROGRAM',g['name'])
        epic.update(scope_in=[c['name'] for c in taxonomy['categories'] if c['group_id']==g['id']],deliverable_paths=[f"research/domains/{g['id']}.md",'coverage/ledger.json'],research_questions=['What distinct product workflows and source/region/language gaps remain in this domain?','Which comparison criteria differ across its categories and user audiences?'],acceptance_criteria=['Every category child has a bounded, reviewed decision record and explicit unresolved gaps.','Cross-category products are deduplicated and secondary membership is not summed as new products.','Synthesis preserves evidence/rights/consumer limitations and actual receiving decisions.'])
        nodes.append(epic)
    for f in foundations['workstreams']:
        epic=base_node(f['id'],f['title'],'epic','APP-PROGRAM',f['title'],f['priority'])
        epic.update(user_decision=f['user_decision'],scope_in=[p['title'] for p in f['packages']],deliverable_paths=[f"research/foundations/{f['id'].lower()}-synthesis.md"],research_questions=[f['user_decision']],acceptance_criteria=['All native work packages meet their scoped criteria and independent review.','Versioned foundation decisions retain unknowns and canonical research-owner boundaries.','Final receiving gates are evidenced without claiming runtime deployment.'])
        nodes.append(epic)
    for c in taxonomy['categories']:
        n=base_node(c['id'],c['name'],'work_package',domain_ids[c['group_id']],next(g['name'] for g in taxonomy['groups'] if g['id']==c['group_id']),c['priority_proposal']['value'])
        n.update(user_decision=c['definition'],scope_in=[c['inclusion']],scope_out=c['exclusion'],deliverable_paths=[c['research_deliverable'],c['paths']['candidate_notes'],'coverage/ledger.json'],research_questions=c['research_questions'],acceptance_criteria=c['acceptance_criteria'],task_groups=c['task_groups'],comparison_fields=c['comparison_fields'],subcategories=c['subcategories'],priority_rationale=c['priority_proposal']['rationale'],overlap=c['overlap'],category_id=c['id'])
        nodes.append(n)
    for f in foundations['workstreams']:
        for p in f['packages']:
            n=base_node(p['id'],p['title'],'work_package',f['id'],f['title'],p['priority'])
            for k in ['status','priority_rationale','readiness','readiness_rationale','research_confidence','assignees','review_roles','user_decision','scope_in','scope_out','deliverable_paths','research_questions','acceptance_criteria','dependencies']:
                n[k]=p[k]
            nodes.append(n)
            for task in p['tasks']:
                t=base_node(task['id'],task['title'],'task',p['id'],f['title'],p['priority'])
                t.update(user_decision=task['independently_reviewable_output'],scope_in=[task['independently_reviewable_output']],deliverable_paths=p['deliverable_paths'],research_questions=[p['user_decision']],acceptance_criteria=task['acceptance_criteria'],subtasks=task['subtasks'],dependencies=p['dependencies'])
                nodes.append(t)
    # Keep provisioning parent-before-child even when sources group nested records.
    by_id={n['id']:n for n in nodes}
    def depth(n):
        return 0 if n['parent_id'] is None else 1+depth(by_id[n['parent_id']])
    nodes.sort(key=lambda n:(depth(n),n['id']))
    counts=dict(Counter(n['kind'] for n in nodes))
    counts['native_relationships_internal']=len(nodes)-1
    counts['checklist_task_groups']=sum(len(n['task_groups']) for n in nodes)
    counts['small_subtasks']=sum(sum(len(t['subtasks']) for t in n['task_groups'])+len(n['subtasks']) for n in nodes)
    plan={'schema_version':'1.0.0','status':'prepared_not_provisioned','target_repository':'Pick-Your-AI/pick-your-ai-applications','external_parent':{'repository':'Pick-Your-AI/pick-your-ai-research','number':509,'url':'https://github.com/Pick-Your-AI/pick-your-ai-research/issues/509','relationship':'native_parent_of_program','verified':False},'counts':counts,'nodes':nodes}
    write_json(ROOT/'planning/backlog.json',plan)
    for n in nodes:
        (ROOT/'planning/issue-bodies'/f"{n['id']}.md").write_text(render_body(n,by_id))
    out=['# Applications delivery backlog','','This is the complete authored issue specification. Remote issue IDs and native relationships are not claimed until the establishment receipt records successful readbacks. Product research remains not started.','',f"**{len(nodes)} native issue definitions:** {counts['program']} program, {counts['epic']} epics, {counts['work_package']} work packages and {counts['task']} independent task issues. Category work packages contain {counts['checklist_task_groups']} smaller task groups. There are {counts['small_subtasks']} small subtasks across the backlog.",'','The program belongs under research #509. Native children must be attached through actual GitHub relationships. Small checklist tasks/subtasks are intentionally kept in their containing issue, following organization methodology.','', '| ID | Level | Parent | Outcome | Initial priority |','| --- | --- | --- | --- | --- |']
    for n in nodes:
        out.append(f"| [{n['id']}](issue-bodies/{n['id']}.md) | {n['kind']} | {n['parent_id'] or 'research #509'} | {n['title']} | {n['priority']} |")
    (ROOT/'planning/BACKLOG.md').write_text('\n'.join(out)+'\n')
    readme=['# Application research taxonomy','','Version 0.1.0 is an authored research scope proposal. Its categories and facets are not product findings or a claim of worldwide exhaustive coverage.','',f"{len(taxonomy['groups'])} domains, {len(taxonomy['categories'])} categories, {sum(len(c['subcategories']) for c in taxonomy['categories'])} subcategories and {len(taxonomy['facets'])} cross-cutting facets.",'','See [machine-readable taxonomy](taxonomy.json), [coverage ledger](../coverage/ledger.json) and [delivery backlog](../planning/BACKLOG.md).','']
    for g in taxonomy['groups']:
        readme += ['## '+g['name'],'']
        for c in taxonomy['categories']:
            if c['group_id']==g['id']:
                readme += [f"- **{c['id']} — {c['name']}:** "+'; '.join(s['name'] for s in c['subcategories'])+'.']
        readme += ['']
    readme += ['## Classification rules','']+['- '+v for v in taxonomy['classification_policy'].values()]+['','## Exclusions','']+['- '+v for v in taxonomy['global_exclusions']]
    (ROOT/'taxonomy/README.md').write_text('\n'.join(readme)+'\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    main()
