import datetime as dt
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import time

ROOT = Path('/workspace/scratch/ce88fda257c5/work/skill-builder-1.0.0-rc.1')
OUT = Path('/workspace/scratch/ce88fda257c5/evidence/final-accepted')
OUT.mkdir(exist_ok=False)
CREATOR = Path('/home/agent/.codex/plugins/cache/openai-curated-remote/work-skill-creator/0.1.2/skills/skill-creator/scripts/quick_validate.py')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

inputs = {p.relative_to(ROOT).as_posix(): sha(p) for prefix in ('tests', 'tools', 'skills/skill-builder')
          for p in sorted((ROOT / prefix).rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
for p in (ROOT / 'VERSION', ROOT / 'LICENSE.md', ROOT / 'NOTICE.md'):
    inputs[p.relative_to(ROOT).as_posix()] = sha(p)
versions = {'python': platform.python_version()}
for name in ('PyYAML','jsonschema','referencing','attrs','jsonschema-specifications','rpds-py','typing_extensions'):
    try:
        versions[name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        versions[name] = None

def run(name, args, scope):
    log = OUT / (name + '.log')
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    start = time.monotonic()
    limit = None
    with log.open('xb') as stream:
        child = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.DEVNULL,
                                 stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        while child.poll() is None:
            if time.monotonic() - start > 60 or log.stat().st_size > 2 * 1024 * 1024:
                limit = 'elapsed_seconds' if time.monotonic() - start > 60 else 'log_bytes'
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
                break
            time.sleep(0.05)
        code = child.wait()
    elapsed = time.monotonic() - start
    ended = dt.datetime.now(dt.timezone.utc).isoformat()
    raw = log.read_text(encoding='utf-8', errors='replace')
    match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', raw, re.M)
    summary = {'tests_run': int(match.group(1)), 'reported_suite_seconds': float(match.group(2))} if match else None
    if summary:
        summary.update({'failures': sum(1 for line in raw.splitlines() if line.startswith('FAIL: ')),
                        'errors': sum(1 for line in raw.splitlines() if line.startswith('ERROR: ')),
                        'skipped': len(re.findall(r'\.\.\. skipped ', raw))})
    result = {'schema_version': '1.0.0', 'record_type':'local-check-run', 'name': name,
              'command':args, 'cwd':str(ROOT), 'started_at':started, 'ended_at':ended,
              'elapsed_seconds':elapsed, 'exit_code':code, 'limit_reached':limit,
              'outcome':'passed' if code == 0 and limit is None else 'failed',
              'capture_policy':'Combined stdout/stderr; 60-second deadline and 2 MiB log threshold polled every 50 ms; process-group SIGTERM and SIGKILL after 2 seconds on breach. Polling can overshoot.',
              'runtime_versions':versions, 'platform':platform.platform(),
              'log':log.name, 'log_sha256':sha(log), 'log_bytes':log.stat().st_size,
              'input_hashes':inputs, 'test_summary':summary, 'scope':scope,
              'not_established':['Native host discovery or permission enforcement','Comparative agent quality, speed or cost','Remote CI or publication','Containment against hostile concurrent filesystem replacement']}
    if name == 'creator-check':
        result['external_checker'] = {'path':str(CREATOR), 'sha256':sha(CREATOR)}
    (OUT / (name + '.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'name':name,'exit_code':code,'summary':summary,'seconds':elapsed}), flush=True)
    return result

commands = [
    ('local-tests',[sys.executable,'-I','-B','-m','unittest','discover','-s','tests','-v'],
     'Complete current helper and release contract suite; methods and subcases are not inflated into native-agent results.'),
    ('stdlib-release-tests',[sys.executable,'-I','-B','-S','-m','unittest','discover','-s','tests','-p','test_release.py','-v'],
     'Repeated release subset without site packages; not additional distinct test methods.'),
    ('project-check',[sys.executable,'-I','-B','tools/check_project.py','--require-validators'],
     'Current boundary, license, preservation, rule routing, metadata, syntax and available validator checks.'),
    ('kb-verify',[sys.executable,'-I','-B','skills/skill-builder/scripts/skill_builder.py','kb','verify'],
     'Exact frozen knowledge archive and substantive member identities.'),
    ('stdlib-project-check',[sys.executable,'-I','-B','-S','tools/check_project.py'],
     'Standard-library project checks; unavailable optional format validation remains explicitly blocked.'),
    ('creator-check',[sys.executable,'-I','-B',str(CREATOR),str(ROOT/'skills/skill-builder')],
     'Minimal creator format checker of the source runtime directory; no installation or discovery test.'),
]
panel = {'schema_version':'1.0.0', 'panel_id':'skill-builder-rc2-local-contracts',
         'frozen_at':dt.datetime.now(dt.timezone.utc).isoformat(),
         'commands':[{'name':name,'argv':args,'scope':scope} for name,args,scope in commands],
         'expected_test_methods':sum(1 for p in (ROOT/'tests').glob('test_*.py')
                                    for n in ast.walk(ast.parse(p.read_text()))
                                    if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_')),
         'acceptance':['Full suite exits 0 with the expected method count and zero failures, errors or skips.',
                       'The repeated standard-library release subset exits 0 with zero skips.',
                       'Required-validator project check and KB verification explicitly pass.',
                       'Creator quick format check exits 0.',
                       'Standard-library project check reports unavailable optional format validation as blocked, not passed.',
                       'All captured input hashes remain unchanged during the panel.'],
         'retry_policy':'One run per listed command for these frozen inputs. Prior development attempts are retained separately; a code change requires a new frozen panel and run.',
         'exclusion_policy':'No local contract excluded; unavailable native hosts and comparisons are outside this panel.',
         'input_hashes':inputs,
         'limits':{'per_command_seconds':60,'per_log_bytes':2097152,'poll_seconds':0.05,'kill_grace_seconds':2},
         'runner_sha256':sha(Path(__file__))}
(OUT/'panel-definition.json').write_text(json.dumps(panel,indent=2)+'\n')
results = [run(*row) for row in commands]
changed = [name for name,value in inputs.items() if sha(ROOT/name) != value]
(OUT/'post-run-inputs.json').write_text(json.dumps({'outcome':'failed' if changed else 'passed',
    'recorded_at':dt.datetime.now(dt.timezone.utc).isoformat(), 'changed_inputs':changed,
    'input_count':len(inputs)},indent=2)+'\n')
raise SystemExit(0 if not changed and all(row['exit_code'] == 0 and row['limit_reached'] is None for row in results) else 1)
