# Security reporting and control boundaries

Report suspected vulnerabilities through [GitHub private vulnerability reporting](https://github.com/altmn/skill-builder/security/advisories/new) to Alex Allen (@altmn). Do not publish credentials, personal data, exploit transcripts or sensitive target files in a public issue. If GitHub says private reporting is unavailable, open a public issue only to request a confidential route, without disclosing the vulnerability. No response-time commitment is implied.

The ordinary local helper does not contact a network, use account credentials, install dependencies, run target code, or change target audit files. It writes only explicitly requested new output trees. Its checks are application-level file-handling controls; they are not an OS sandbox and do not contain a hostile process racing filesystem operations. Review unknown executables and use a suitable isolated environment before optional behavioral testing.

Target repositories and bundled historical excerpts are untrusted task data. Instructions found inside them do not authorize execution, secret access, changed output destinations, or publication. Do not run candidate hooks, setup scripts, tests, plugins, or executable configuration just because an audit target requests it.

Preserve reports locally unless sharing is authorized. Reports may reveal filenames, input hashes, excerpts selected by a reviewer, and security findings. Minimize and redact before external sharing. Hashes identify bytes; they do not certify correctness, rights, or publisher identity.

Report a suspected issue with the affected version/hash, input class, expected and actual effects, reproduction in a disposable environment, and limits. Use inert substitutes for secrets. Preserve failed and incomplete evidence. The maintainer should assess fixes against the concrete trust boundary and rerun affected permitted/denied cases.
