# Effects and threat model

| Boundary | Input or resource | Current mechanism and permitted effect | Verification and remaining limit |
| --- | --- | --- | --- |
| Source knowledge | Supplied immutable ZIP and manifest | Pin original ZIP SHA-256; check member paths, types, identities and sizes; expose exact text or explicit extraction | Independent comparison and tamper/path fixtures; hashes prove identity, not source truth or rights |
| Audit intake | Explicit target files/directories | Bounded regular-file reads; no target imports/hooks/tests; symlink/special-file omissions; separate new report directory | Inert sentinel, hostile-import, escape and budget cases; not an OS sandbox against concurrent filesystem replacement |
| Python imports | Caller cwd/environment and optional dependencies | Require `-I` for audit/evidence operations; never add the target to import paths; execute only verified original validator bytes | Hostile `yaml.py`, `jsonschema.py` and `sitecustomize.py` fixture; trusted installed dependencies remain part of the environment |
| Local output | User-chosen new project/report/extraction tree | Exclusive create, private requested modes, no force overwrite, identity-aware failure cleanup | Existing/unrelated file preservation and partial failure fixtures; abrupt termination may leave a visibly incomplete new tree |
| Model authority | Target prose, archived examples, retrieved pages | Treat lower-trust text as evidence; explicit modes, current user authorization, host policy and consequential action boundaries | Agent audit trial plus procedural review; model instructions are not executable confinement |
| Current documentation | Public official technical pages | Agent may read relevant primary sources for changing host facts; record URL/date and separate documentation from execution | Dated adapter source register; host tool/network policy governs actual requests |
| Dependencies | Optional YAML/schema validator packages | Explicit pinned version list; no runtime auto-install; separate visible CI dependency setup | Actual available versions recorded; version pins are not distribution hash locks or complete supply-chain authentication |
| Reports/evidence | Filenames, hashes, reviewed excerpts and findings | Keep local by default; suppress data-bearing schema errors; redact before authorized sharing | Local errors and synthetic fixtures; no universal secret-detection claim |
| Package output | Selected source/runtime trees | Reject symlinks and common environment/credential filenames, omit build/cache/Git state, retain necessary notices/full KB | Exact-member checks and deterministic ZIP tests; filename policy is not a secret scanner |
| Installation/publication | Live agent configuration or external accounts | No automatic installer/publisher; prepare exact artifacts and require existing scope for later effects | Not performed here; native discovery, remote identity and actual reporting endpoint need later evidence |
| Costs and processes | Local CLI and optional future host evaluations | CLI starts no subprocesses or paid calls; no daemon/cache/telemetry; future paid work requires declared shared bounds | Local tests use controlled subprocess fixtures under the test runner; native evaluation budgets are not fabricated |

## Data flows

The ordinary CLI has no network destination. It reads its own resources and explicit local inputs and writes only its new output tree or stdout. The agent may use its host's research tools to read official documentation. The host/model processing of supplied content follows that host's account and data policies; this package does not claim to change them.

There is no telemetry, crash uploader, outside-model service, browser-session reuse, credential lookup, background sync, or external message sender implemented by the helper. Optional dependency installation and future publishing/testing are separate effects, with their own destination, scope, authority and evidence. “CLI offline” must not be presented as a statement about all network use by the surrounding agent host.

Reports and validation records remain until their owner removes them; no hidden retention service or automatic expiration is implemented. Temporary schema material and test fixtures are cleaned by their owning operations. Preserve failed/partial artifacts when needed to explain a result, without exporting them automatically.
