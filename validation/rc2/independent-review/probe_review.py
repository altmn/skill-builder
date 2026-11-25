"""Independent local probes. Writes only beneath this evidence directory."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.metadata
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import zipfile

BASE = Path(__file__).absolute().parent
PROJECT = Path('/workspace/scratch/ce88fda257c5/work/skill-builder-1.0.0-rc.1')
SCRIPT = PROJECT / 'skills/skill-builder/scripts/skill_builder.py'
ORIGINAL = Path('/workspace/scratch/ce88fda257c5/upload/skill-builder-1.0.0-rc.1-source(2).zip')
BASE.joinpath('tmp').mkdir(exist_ok=True)
tempfile.tempdir = str(BASE / 'tmp')
os.environ['TMPDIR'] = str(BASE / 'tmp')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

builder = load('integration_builder', SCRIPT)
release = load('integration_release', PROJECT / 'tools/build_release.py')
result = {
    'environment': {'python': sys.version, 'platform': platform.platform(),
                    'isolated': bool(sys.flags.isolated)},
    'reviewed_identity': {str(p.relative_to(PROJECT)): sha(p.read_bytes()) for p in
                         (SCRIPT, PROJECT / 'tools/build_release.py', PROJECT / 'tools/check_project.py')},
    'observations': [],
    'scope_limits': ['Local Linux mechanics only; no native agent host or remote service was exercised.',
                     'Original embedded utilities were inspected before the trusted utility path was executed.',
                     'No adversarial filesystem race resistance or third-party rights adjudication is claimed.'],
}
for package in ('PyYAML', 'jsonschema', 'referencing'):
    try:
        result['environment'][package] = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        result['environment'][package] = None

def record(name, passed, **details):
    item = {'name': name, 'passed': passed, **details}
    result['observations'].append(item)
    (BASE / 'observations.json').write_text(json.dumps(result, indent=2, ensure_ascii=True) + '\n')
    print(name + ': ' + ('passed' if passed else 'FAILED'), flush=True)

kb = builder.KnowledgeBase()
preservation = kb.verify()
with zipfile.ZipFile(ORIGINAL) as archive:
    original_kb = archive.read('skill-builder-1.0.0-rc.1/skills/skill-builder/references/knowledge-base.zip')
    original_manifest = archive.read('skill-builder-1.0.0-rc.1/skills/skill-builder/references/knowledge-base-manifest.json')
record('full_preservation', preservation['outcome'] == 'passed'
       and original_kb == kb.archive_bytes
       and original_manifest == (builder.REFERENCE_ROOT / 'knowledge-base-manifest.json').read_bytes(),
       result=preservation, original_source_sha256=sha(ORIGINAL.read_bytes()),
       kb_entries=len(kb.archive.infolist()))
canonical = kb.json('catalogs/requirements.json')['rules']
selection = builder.select_profile(kb, 'instruction', [], {})
retained = all(all(row[key] == source_value for key, source_value in original.items())
               for row, original in zip(selection['rules'], canonical))
record('canonical_rule_full_fields_preserved', retained and len(canonical) == len(selection['rules']) == 99)

import yaml
started = time.monotonic()
count, batches, failures = 0, 0, []
batch = []
def examine(chars):
    global batches
    value = 'x' + ''.join(chars)
    serialized = builder.yaml_quoted_scalar(value)
    actual = yaml.safe_load('description: ' + serialized + '\n')['description']
    batches += 1
    if actual != value:
        failures.append({'batch': batches, 'first_codepoint': ord(chars[0])})
for codepoint in range(1, 0x110000):
    if 0xD800 <= codepoint <= 0xDFFF:
        continue
    batch.append(chr(codepoint))
    count += 1
    if len(batch) == 1023:
        examine(batch)
        batch = []
if batch:
    examine(batch)
record('all_accepted_unicode_scalars_serializer_roundtrip', not failures,
       scalar_values_examined=count, description_batches=batches, failures=failures,
       seconds=round(time.monotonic() - started, 3),
       oracle='yaml.safe_load equality for descriptions of at most 1024 scalars; U+0000 and surrogate codepoints excluded by the public contract')

def cli(name, *args):
    command = [sys.executable, '-I', '-B', str(SCRIPT), *map(str, args)]
    response = subprocess.run(command, capture_output=True, timeout=45, cwd=BASE,
                              env={**os.environ, 'TMPDIR': str(BASE / 'tmp')})
    (BASE / (name + '.stdout')).write_bytes(response.stdout)
    (BASE / (name + '.stderr')).write_bytes(response.stderr)
    return response

description = 'Quoted "word"; slash \\; controls\x01\x7f\x85\u2028\u2029\ufffe\uffff; unicode café Проверка 中文 😀\U0010ffff\r\nend'
output = BASE / 'unicode-created'
created = cli('unicode-create', 'skill-builder-create', '--name', 'unicode-example', '--description', description,
              '--output', output, '--profile', 'instruction')
if created.returncode == 0:
    text = (output / 'skills/unicode-example/SKILL.md').read_text()
    actual = yaml.safe_load(text.split('---', 2)[1])['description']
    inventory = {'files': [{'path': 'skills/unicode-example/SKILL.md', 'kind': 'regular_file', 'status': 'hashed'}]}
    format_result = builder.format_checks(kb, output, inventory)
else:
    actual, format_result = None, None
record('cli_unicode_create_roundtrip_and_portable_format', created.returncode == 0 and actual == description
       and format_result['outcome'] == 'passed', exit_code=created.returncode, format_result=format_result)

records = BASE / 'record-fixtures'
records.mkdir()
valid = kb.read('examples/records/evaluation-receipt.json')
fixtures = [('valid-first', valid, 'passed')]
baseline = json.loads(valid)
for token in ('1e999', '-1e999', 'NaN', 'Infinity', '-Infinity', '1.7976931348623157e308', '1e-300'):
    item = json.loads(valid)
    item['elapsed']['value'] = 'TOKEN'
    fixtures.append(('number-' + str(len(fixtures)), json.dumps(item).replace('"TOKEN"', token).encode(),
                     'passed' if token in ('1.7976931348623157e308', '1e-300') else 'failed'))
for value in ([], {}, None, True, 42, 'UNKNOWN', ['SYNTHETIC-NO-ECHO'], {'x': 'SYNTHETIC-NO-ECHO'}):
    fixtures.append(('dispatch-' + str(len(fixtures)), json.dumps({'record_type': value}).encode(), 'failed'))
fixtures.extend([
    ('nested-duplicate', b'{"record_type":"evaluation-receipt","x":{"k":1,"k":2}}', 'failed'),
    ('invalid-utf8', b'\xff\xfe', 'failed'),
    ('giant-integer', b'{"record_type":"evaluation-receipt","x":' + b'9' * 5000 + b'}', 'failed'),
    ('deep-json', b'[' * 1100 + b'0' + b']' * 1100, 'failed'),
    ('valid-last', valid, 'passed'),
])
paths, expected = [], []
for name, data, outcome in fixtures:
    path = records / (name + '.json')
    path.write_bytes(data)
    paths.append(str(path))
    expected.append(outcome)
batch = cli('record-batch', 'check', *(arg for path in paths for arg in ('--record', path)))
try:
    batch_payload = json.loads(batch.stdout)
    actual_rows = batch_payload['records']['records']
    succeeded = (batch.returncode == 1 and not batch.stderr
                 and [row['path'] for row in actual_rows] == paths
                 and [row['outcome'] for row in actual_rows] == expected
                 and b'SYNTHETIC-NO-ECHO' not in batch.stdout)
except (ValueError, KeyError):
    succeeded, batch_payload = False, None
record('mixed_record_batch_continues_and_hides_values', succeeded,
       exit_code=batch.returncode, records=len(paths), expected=expected,
       actual=None if batch_payload is None else batch_payload.get('records'))

# A nonexistent Unix-user shorthand is a supported Path.expanduser input shape;
# no account lookup or external service is performed by this local probe.
unknown_path = '~skill_builder_integration_no_such_user_9a4255/evidence.json'
unknown = cli('unknown-user-record', 'check', '--record', paths[0], '--record', unknown_path, '--record', paths[-1])
try:
    payload = json.loads(unknown.stdout)
    rows = payload['records']['records']
    good = unknown.returncode == 1 and [row['outcome'] for row in rows] == ['passed', 'failed', 'passed']
except (ValueError, KeyError):
    good, payload = False, None
record('unresolvable_user_path_retains_batch', good, exit_code=unknown.returncode,
       stdout_bytes=len(unknown.stdout), stderr_bytes=len(unknown.stderr),
       traceback='Traceback (most recent call last)' in unknown.stderr.decode(errors='replace'),
       public_contract='Each unreadable/malformed input record produces its own failure; remaining requested records continue in order.')

license_data = release.license_metadata()
record('current_license_consistency', license_data['status'] == 'selected'
       and (PROJECT / 'LICENSE.md').read_bytes() == (release.SKILL / 'LICENSE.md').read_bytes(),
       decision=license_data)

record('reviewed_code_unchanged_during_probe', all(sha((PROJECT / p).read_bytes()) == digest
       for p, digest in result['reviewed_identity'].items()))
print(json.dumps({'observations': len(result['observations']),
                  'failed': [row['name'] for row in result['observations'] if not row['passed']]}))
