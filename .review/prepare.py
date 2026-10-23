#!/usr/bin/env python3
"""Apply one hash-pinned review fix; create commit objects, never move refs."""
from __future__ import annotations
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

REPO = 'Pick-Your-AI/pick-your-ai-applications'
BASE = '517ebf62e560341dc75239a4949e3645ba4007c4'
TREE = 'd716054cdb91c5e8632c0b49f3b1b3fcad68bb34'
BRANCH = 'contrib/CompleteDotTech/applications-foundation'
GZIP_SHA = 'c753b31a929ec9b0ff626936034c208557ffb2d9638fc665a977f0bba9aba8b9'
PATCH_SHA = '70230c5776f401ca126363ec2670f37c4099045f0176e03d906ac35056036524'
FILES = {
    '.gitignore': 'b17f5f3ddc7137063909c62a49071b461801e379',
    'docs/VALIDATION_HARDENING.md': '68dca5bb810432e529f7105fa41110a8fea0efbc',
    'scripts/provision_github.py': '94ea46bea0a7574a1a3f9c0966538747bc8ed0b6',
    'scripts/render_backlog.py': 'dba6a38f830d49e6b25cdd083b25582134ad0349',
    'scripts/validate_applications.py': '6eab8c54c51b8eccc5315ef94489d87e068fc08c',
    'scripts/validate_planning.py': '5363f2b19e5ae08f0c70a7f9f8229d9a0c4f81d7',
    'tests/test_application_contract.py': 'e27dd8fb655e6387e9389f78c4194185d2aac419',
    'tests/test_review_regressions.py': 'fcc51a12726fd73de872a979c095f8fb69293989',
}
ROOT = Path(__file__).resolve().parents[1]
WORK = Path(os.environ['GITHUB_WORKSPACE']) / 'foundation'
OUT = ROOT / '.review' / 'results'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(args, name, data=None):
    proc = subprocess.run(args, cwd=WORK, input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=180, check=False)
    text = proc.stdout.decode('utf-8', errors='replace')
    (OUT / f'{name}.log').write_text(text, encoding='utf-8')
    print(text, flush=True)
    require(proc.returncode == 0, f'{name} failed with exit {proc.returncode}')
    return text


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('API redirect refused')


def api(path, payload=None):
    # Only this repository's Git data endpoints; no refs mutation, issues,
    # secrets, access, organization endpoints, or credential creation.
    require(path.startswith(('git/trees', 'git/commits', 'git/ref/heads/')), 'API path outside scope')
    require(payload is None or path in {'git/trees', 'git/commits'}, 'Mutation outside scope')
    req = urllib.request.Request(
        f'https://api.github.com/repos/{REPO}/{path}',
        data=None if payload is None else json.dumps(payload).encode('utf-8'),
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
                 'X-GitHub-Api-Version': '2022-11-28'},
        method='GET' if payload is None else 'POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'GitHub API returned HTTP {exc.code}; no retry or credential change') from None


def main():
    require(os.environ.get('GITHUB_REPOSITORY') == REPO, 'Wrong repository')
    require(os.environ.get('GITHUB_ACTOR') == 'CompleteDotTech', 'Unexpected workflow actor')
    OUT.mkdir(parents=True, exist_ok=True)
    raw = b''.join((ROOT / '.review' / 'parts' / str(i)).read_bytes() for i in range(4))
    require(hashlib.sha256(raw).hexdigest() == GZIP_SHA, 'Compressed patch hash mismatch')
    patch = gzip.decompress(raw)
    require(len(patch) == 67759 and hashlib.sha256(patch).hexdigest() == PATCH_SHA, 'Patch hash mismatch')
    require(run(['git', 'rev-parse', 'HEAD'], 'base').strip() == BASE, 'Checkout is not exact base')
    run(['git', 'apply', '--check', '-'], 'apply-check', patch)
    run(['git', 'apply', '--index', '-'], 'apply', patch)
    changed = run(['git', 'diff', '--cached', '--name-only'], 'changed-files').splitlines()
    require(set(changed) == set(FILES) and len(changed) == len(FILES), 'Unexpected changed files')
    run(['git', 'diff', '--cached', '--check'], 'whitespace')
    entries = []
    for name, expected in FILES.items():
        file = WORK / name
        require(file.is_file() and not file.is_symlink(), 'Non-regular patch output')
        data = file.read_bytes()
        sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(sha == expected, f'Output hash mismatch: {name}')
        entries.append({'path': name, 'type': 'blob', 'mode': '100644', 'content': data.decode('utf-8')})
    # Validation code receives no API token. It cannot mutate GitHub.
    token = os.environ.pop('GH_TOKEN')
    try:
        run(['python3', 'scripts/validate_applications.py'], 'applications')
        run(['python3', 'scripts/validate_planning.py'], 'planning')
        tests = run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'tests')
        require('Ran 102 tests' in tests and '\nOK\n' in tests, 'Expected 102 passing tests')
    finally:
        os.environ['GH_TOKEN'] = token
    require(api('git/ref/heads/' + BRANCH)['object']['sha'] == BASE, 'Foundation advanced; reconcile before publishing')
    require(api('git/commits/' + BASE)['tree']['sha'] == TREE, 'Base tree mismatch')
    tree = api('git/trees', {'base_tree': TREE, 'tree': entries})
    tree_readback = api('git/trees/' + tree['sha'] + '?recursive=1')
    require(not tree_readback.get('truncated'), 'Truncated tree readback')
    require({entry['path']: entry['sha'] for entry in tree_readback['tree'] if entry['path'] in FILES} == FILES,
            'Server output tree does not match validated files')
    commit = api('git/commits', {'message': 'fix: enforce application evidence and planning integrity',
                               'tree': tree['sha'], 'parents': [BASE]})
    require(commit['tree']['sha'] == tree['sha'] and [p['sha'] for p in commit['parents']] == [BASE],
            'Created commit differs from expected parent or tree')
    receipt = {'repository': REPO, 'base_commit': BASE, 'commit': commit['sha'], 'tree': tree['sha'],
               'files': FILES, 'patch_sha256': PATCH_SHA, 'tests_passed': 102,
               'validators': {'applications': 'passed', 'planning': 'passed'},
               'branch_updated': False, 'main_updated': False, 'review_approval': False,
               'research_verified': False, 'observed_at': dt.datetime.now(dt.timezone.utc).isoformat()}
    (OUT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == '__main__':
    main()
