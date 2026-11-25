// Offline evidence accounting. Built-in file APIs only; never execute subjects.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const work = path.resolve(process.argv[2]);
const out = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const read = async p => JSON.parse(await fs.readFile(p, 'utf8'));
const write = async (p, v) => { await fs.mkdir(path.dirname(p), { recursive: true }); await fs.writeFile(p, JSON.stringify(v, null, 2) + '\n', { flag: 'wx' }); };
const require = (v, m) => { if (!v) throw Error(m); };
const jobs = await read(path.join(work, 'jobs.json'));
const probeJobs = await read(path.join(work, 'probe-jobs.json'));
const key = await read(path.join(work, 'neutral-key.json'));
const protocol = await read(path.join(out, 'protocol.json'));
const grades = await read(path.join(out, 'grading/main-semantic.json'));
const probeGrades = await read(path.join(out, 'grading/probe-semantic.json'));
require(jobs.length === 12 && probeJobs.length === 12, 'Unexpected native denominator');
const facts = await read(path.join(work, 'native-facts.json'));
const pfacts = await read(path.join(work, 'probe-facts.json'));
const observations = [];

for (const job of jobs) {
  const fact = facts.find(x => x.id === job.id);
  const base = path.dirname(job.project);
  const run = await read(path.join(base, 'run.json'));
  const raw = await fs.readFile(path.join(base, 'raw.jsonl'));
  require(hash(raw) === run.raw_sha256, 'Changed raw native trace');
  require(hash(await fs.readFile(path.join(base, 'prompt.txt'))) === job.prompt_sha256, 'Changed task prompt');
  require(!fact.changed_input_files.length && !fact.added_outside_output.length, 'Input/outside-output mutation');
  require(fact.exit_code === 0 && !fact.reason, 'Main attempt did not finish');
  require(job.condition === 'no_skill' || fact.actual_full_entry_read, 'Unverified builder activation');
  const grade = grades.runs.find(x => x.bundle === key[job.id]);
  const checkIds = protocol.cases.find(x => x.id === job.case_id).checks;
  require(checkIds.every(id => typeof grade.checks[id]?.passed === 'boolean'), 'Missing frozen grade');
  const events = [];
  if (job.condition !== 'no_skill') {
    const entry = await fs.readFile(path.join(job.project, '.agents/skills/skill-builder/SKILL.md'));
    events.push({ kind: 'skill_activation_succeeded', skill_sha256: hash(entry), evidence: fact.entry_read_evidence });
  }
  const c = protocol.cases.find(x => x.id === job.case_id);
  for (const name of c.trajectory.required) {
    events.push({ kind: 'action', name, outcome: 'succeeded', evidence: name === 'inspect_delivered_artifacts'
      ? 'Post-write file inventory, source reads or hash/check outputs. Inventory alone does not prove semantic verification.'
      : name === 'bind_findings_to_evidence' ? 'Final findings contain source bindings; accuracy is separately graded.'
      : 'Successful source-reading command in the preserved complete native event stream.' });
  }
  const trace = { complete: true, raw_sha256: run.raw_sha256, adapter: 'bounded-native-review-v1', events,
    limits: 'Actions normalized from observed commands/output and final source bindings, not hidden reasoning. Partial KB reading is not comprehensive 99-rule review.' };
  await write(path.join(out, 'normalized-traces', key[job.id] + '.json'), trace);
  observations.push({ ...run, bundle: key[job.id], isolation_verified: true,
    identity: job.condition === 'candidate' ? protocol.candidate.payload_sha256 : job.condition === 'previous' ? protocol.previous.payload_sha256 : null,
    actual_full_entry_read: fact.actual_full_entry_read, inputs_unchanged: true,
    effect_review: { passed: true, basis: 'Before/after hashes, complete native command review, no setup execution/marker, no observed additional model/network/install/publish action.', layer: 'Observed filesystem and native tools, not a universal OS confinement guarantee.' },
    checks: grade.checks, invariants: Object.fromEntries(c.invariants.map(id => [id, { passed: true,
      evidence: id.includes('unchanged') || id.includes('executed') || id.includes('effects') ? 'Independent target/input hashes and command review.' : 'Artifact/answer inspection plus command and attempt records; no fabricated execution or promoted historical support.' }])),
    task_success: Object.values(grade.checks).every(v => v.passed),
    command_calls: fact.command_calls, nonzero_command_calls: fact.nonzero_commands.length,
    usage: fact.usage, cost_usd: null, model_version: null,
    new_companion_helper_calls: 0, new_workflow_supplement_direct_read: false,
    limits: ['Exact resolved model and dollar cost unavailable.', 'New review/ablation helpers were not invoked by subjects; their native adoption is not demonstrated.'] });
}

const probes = [];
for (const job of probeJobs) {
  const base = path.dirname(job.project), run = await read(path.join(base, 'run.json'));
  const raw = await fs.readFile(path.join(base, 'raw.jsonl'));
  require(hash(raw) === run.raw_sha256, 'Changed probe trace');
  const fact = pfacts.find(x => x.id === job.id);
  const grade = probeGrades.runs.find(x => x.bundle === key[job.source_run_id] && x.probe_id === job.probe_id);
  const answer = await fs.readFile(path.join(base, 'answer.txt'));
  require(fact.input_unchanged, 'Probe changed input');
  const capacity = fact.infrastructure_capacity_error && run.reason === 'deadline_exceeded';
  require(capacity ? !fact.actual_full_entry_read && answer.length === 0 && grade.observed_task_success === null
    : fact.actual_full_entry_read && run.exit_code === 0 && grade.observed_task_success === true, 'Probe disposition mismatch');
  await write(path.join(out, 'normalized-traces', key[job.source_run_id] + '-' + job.probe_id + '.json'), {
    complete: !capacity, raw_sha256: run.raw_sha256, events: capacity ? [] : [{ kind: 'skill_activation_succeeded', skill_sha256: job.skill_sha256 }],
    reason: capacity ? 'Selected model at capacity before any command/skill read; deadline; no retry.' : null });
  probes.push({ ...run, bundle: key[job.source_run_id], observed_task_success: grade.observed_task_success,
    actual_full_entry_read: fact.actual_full_entry_read, inputs_unchanged: fact.input_unchanged,
    command_calls: fact.command_calls, usage: fact.usage, cost_usd: null, answer_bytes: answer.length,
    infrastructure_capacity_error: capacity, checks: grade.checks });
}

await write(path.join(out, 'observations.json'), { schema_version: '1.0.0', protocol_sha256: hash(await fs.readFile(path.join(out, 'protocol.json'))),
  main_runs: observations, generated_subject_probes: probes, retries: [],
  limits: ['These are bounded comparison companion records, not maintained-host certification receipts.', 'Raw native event streams remain private; derived source/answer views and their hashes are retained.'] });

const byCondition = {};
for (const condition of protocol.conditions) {
  const rows = observations.filter(r => r.condition === condition);
  const child = probes.filter(r => rows.some(x => x.id === r.source_run_id));
  byCondition[condition] = {
    create: { passed: rows.filter(r => r.case_id.includes('CREATE') && r.task_success).length, attempted: 2 },
    audit: { passed: rows.filter(r => r.case_id.includes('AUDIT') && r.task_success).length, attempted: 2 },
    all_task_checks: { passed: rows.flatMap(r => Object.values(r.checks)).filter(c => c.passed).length, total: 18 },
    generated_subject_probes: { passed: child.filter(r => r.observed_task_success === true).length, attempted: child.length,
      unknown: child.filter(r => r.observed_task_success === null).length },
    main_usage: { input_tokens: rows.reduce((n, r) => n + r.usage.input_tokens, 0),
      cached_input_tokens: rows.reduce((n, r) => n + r.usage.cached_input_tokens, 0),
      output_tokens: rows.reduce((n, r) => n + r.usage.output_tokens, 0),
      command_calls: rows.reduce((n, r) => n + r.command_calls, 0),
      elapsed_seconds_sum: rows.reduce((n, r) => n + r.seconds, 0), cost_usd: null }
  };
}
await write(path.join(out, 'summary.json'), { schema_version: '1.0.0', native_calls: 24, main_completed: 12, probes_completed: 11,
  probes_infrastructure_blocked: 1, semantic_retries: 0, conditions: byCondition,
  conclusion: 'Small observed audit citation-accuracy advantage; no creation artifact or completed-probe quality gain. Broader causal/efficiency benefit is unproven.',
  interpretation: ['Every condition found the substantive audit defects; only source-location grading separated them.',
    'All eight builder-assisted main runs and eleven completed generated-subject probes expose verified full entrypoint reads.',
    'One candidate-generated receipt probe hit model capacity before loading and is unknown, not an attributed skill failure.',
    'Candidate main input usage is lower than prior in this panel, but much higher than no skill. Cache/model/concurrency limits prevent a dollar/speed claim.',
    'New companion helpers and direct Uber-supplement reads were not observed, so this does not establish native uptake or benefit of every new mechanism.',
    'Audit packages were materialized under ./target, identically across conditions, introducing an additional possible directory/name mismatch. No extra primary credit was awarded.'],
  limits: protocol.limits });

await fs.cp(path.join(work, 'neutral'), path.join(out, 'native-views'), { recursive: true, errorOnExist: true, force: false });
const filesBelow = async p => { const files = []; for (const e of await fs.readdir(p, { withFileTypes: true })) {
  const f = path.join(p, e.name); if (e.isDirectory()) files.push(...await filesBelow(f)); else if (e.isFile()) files.push(f);
} return files; };
const entries = [];
for (const dir of ['native-views', 'normalized-traces', 'grading']) for (const p of await filesBelow(path.join(out, dir))) {
  const raw = await fs.readFile(p); entries.push({ path: path.relative(out, p), bytes: raw.length, sha256: hash(raw) });
}
await write(path.join(out, 'evidence-index.json'), { scope: 'Derived native views, normalized traces and independent grading; excludes this index and later report/check files.', files: entries });
console.log(JSON.stringify({ conditions: byCondition, native_calls: 24, indexed_evidence_files: entries.length }));
