// Read-only verification of retained evidence and the private original attempts.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
const out = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const root = path.dirname(path.dirname(out));
const work = path.resolve(process.argv[2]);
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const read = async p => JSON.parse(await fs.readFile(p, 'utf8'));
const require = (v, m) => { if (!v) throw Error(m); };
const protocol = await read(path.join(out, 'protocol.json'));
const obs = await read(path.join(out, 'observations.json'));
const summary = await read(path.join(out, 'summary.json'));
require(obs.protocol_sha256 === hash(await fs.readFile(path.join(out, 'protocol.json'))), 'Protocol changed');
require(protocol.corpus_sha256 === hash(await fs.readFile(path.join(root, 'evals/field/execution.json'))), 'Field corpus changed');
require(obs.main_runs.length === 12 && obs.generated_subject_probes.length === 12 && obs.retries.length === 0, 'Denominator/retry mismatch');
let complete = 0, blocked = 0;
for (const run of [...obs.main_runs, ...obs.generated_subject_probes]) {
  const project = path.join(work, run.source_run_id ? 'probes' : 'runs', run.id, 'project');
  const base = path.dirname(project);
  const raw = await fs.readFile(path.join(base, 'raw.jsonl'));
  const stderr = await fs.readFile(path.join(base, 'stderr.txt'));
  require(hash(raw) === run.raw_sha256 && hash(stderr) === run.stderr_sha256, 'Raw evidence changed');
  require(raw.length + stderr.length === run.captured_bytes && run.captured_bytes <= protocol.capture_bytes_per_attempt, 'Capture accounting mismatch');
  require(run.source_run_id ? run.inputs_unchanged : run.inputs_unchanged && run.effect_review.passed, 'Input/effect gap');
  if (run.reason) {
    blocked++;
    require(run.infrastructure_capacity_error && run.observed_task_success === null && run.usage === null && run.answer_bytes === 0, 'Blocked attempt became a pass/zero usage');
    require(stderr.toString().includes('Selected model is at capacity'), 'Missing infrastructure reason');
  } else { complete++; require(run.exit_code === 0, 'Unexpected failed completion'); }
}
require(complete === 23 && blocked === 1, 'Completion accounting mismatch');
for (const entry of (await read(path.join(out, 'evidence-index.json'))).files) {
  const file = path.resolve(out, entry.path);
  require(file.startsWith(out + path.sep), 'Escaping evidence path');
  const raw = await fs.readFile(file);
  require(hash(raw) === entry.sha256 && raw.length === entry.bytes, 'Derived evidence changed');
}
for (const entry of protocol.candidate.files) {
  const raw = await fs.readFile(path.join(root, 'skills/skill-builder', entry.path));
  require(hash(raw) === entry.sha256, 'Current runtime differs from native snapshot');
}
require(hash(await fs.readFile(path.join(root, 'skills/skill-builder/references/knowledge-base.zip'))) === '9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204', 'Frozen KB changed');
for (const condition of protocol.conditions) {
  const rows = obs.main_runs.filter(r => r.condition === condition);
  const actual = summary.conditions[condition];
  require(rows.length === 4 && rows.filter(r => r.case_id.includes('CREATE') && r.task_success).length === actual.create.passed &&
    rows.filter(r => r.case_id.includes('AUDIT') && r.task_success).length === actual.audit.passed, 'Summary success mismatch');
  for (const [field, key] of [['input_tokens','input_tokens'],['cached_input_tokens','cached_input_tokens'],['output_tokens','output_tokens']]) {
    require(rows.reduce((n, r) => n + r.usage[field], 0) === actual.main_usage[key], 'Usage sum mismatch');
  }
}
console.log(JSON.stringify({ outcome: 'passed', native_attempts: 24, completed: 23, infrastructure_blocked: 1,
  frozen_inputs_and_evidence: 'matched', runtime_unchanged: true, semantic_judgment_limit: 'Checks accounting and identities, not independent reviewer truth or general benefit.' }));
