# Release-candidate review log

Date: **2026-10-09**. Scope: local `0.1.0` release preparation. No remote push,
tag, release, or host-wide skill installation was performed.

## Pass 1 — independent rule review

A separate Codex subagent reviewed the core for compatibility, security,
conceptual integrity, and game design. Another authored the taxonomy and corpus.
These were separate contexts in the same Codex session, not external researchers
or diverse-model reviewers.

| Finding | Resolution |
| --- | --- |
| Mode-only requests could ask for an objective even with one active | Scoped the opening rule to absence of a current objective; mode changes retain it. |
| A blanket missing-objective rule also caught Help | Restricted it to scenario-dependent controls; Help/reset work before an objective. |
| Candidate analysis demanded completed success, rejecting valid examples of harmful optimization progress | Added a separate progress-without-completion verdict; prohibited claiming an optimum from partial progress. |
| Challenge examples omitted scorecards and credited an undiscussed loophole | Added quality/progress scorecards, N/A victory, and counts limited to discussed vulnerabilities. |
| Research example omitted source-verification status | Added the explicit bundled-source limitation. |

## Pass 2 — implementation and behavioral review

The validation subagent exercised malformed fixtures and changed source trees,
rather than treating tests that merely search rule phrases as behavioral proof.
During implementation, anchor rebasing and an unresolved-link postcondition were
added to keep the standalone prompt self-contained. Root review added a packaged
MIT notice and exact license-copy validation so manual installs retain the terms.

Two additional subagents received only the skill, relevant references, and player
turns, without expected answers. Their **15 actual replies across 8 selected
cases/variants** are preserved in [smoke A](evaluations/smoke-a.json) and
[smoke B](evaluations/smoke-b.json). Case IDs, actual added mode/reset prefixes,
loaded-file hashes, evidence excerpts, and limitations are recorded. No gameplay
tool calls occurred; setup file reads and subsequent evaluation work are separate.
The local configured model is `gpt-6-astra`; runtime routing and exact revision
are not exposed by this subagent interface. This is a smoke test, not a full
52-case behavioral sweep or an end-user host-discovery test.

The players self-scored 46 case-level assertions: **44 met, 1 missed, 1 unclear**.
The root agent reviewed all actual replies and agreed with the recorded results.
The missed criterion asks for an explicit overdiagnosis distinction in a medical
classifier review; the unclear one asks for specific clinical oversight and
sensitivity/specificity evaluation. The output discussed incorrect positives and
missed cases without unsafe clinical advice or a false equivalence, but omitted
part of those compound expectations. These minor domain-detail gaps remain
visible; no failed run or assertion was relabeled as a pass. This sample is not
a statistical success-rate estimate. Other corpus cases remain untested.

An additional standalone entry-point run is preserved in
[standalone](evaluations/standalone.json). It produced a bounded library example,
but its setup file read was truncated, so it is only evidence of first-round
behavior from the visible portion of the prompt. A fresh agent then loaded the
entire prompt without truncation and played the same objective. That
[full-load repeat](evaluations/standalone-full.json) also produced a bounded,
conditional failure and useful repair. Root reviewed the response against five
qualitative criteria and found them met. Both actual outputs are retained. File
loading tests the prompt text, not UI copy/paste or host discovery.

## Pass 3 — final repository review

The independent compatibility reviewer revisited the final package, instructions,
licensing, generation, tests, and security claims. It found a procedure bug:
most fixture modes live in a separate `mode` field, but the procedure only sent
the user turns. The procedure now initializes and records the mode before sending
those turns. The actual smoke runs used explicit mode prefixes and disclose their
departures from exact fixture execution. No other major defect was identified
in that static pass. Same-model review is useful criticism, not independent
researcher certification.

Root installation testing then exposed an upstream CLI removal issue. CLI 1.7.2
reported success with `remove specification-game --agent codex --yes` but left
the shared copy discoverable. Removal without the agent filter removed the copy,
and a subsequent list showed no project skills. The README now uses that tested
command, explains its cross-agent scope, and records the limitation in the
compatibility guide.

## Executed checks

- Local Vercel `skills` **1.7.2** discovery: `npx skills add . --list` found exactly
  `specification-game`. Its `--help` output confirmed documented CLI flags.
- Local CLI installation with `--copy --agent codex --yes` succeeded in a new
  temporary project outside the repository. All **7 installed files** matched
  source hashes. Listing found the skill, and complete removal was verified as
  described above. No personal installation requested. Remote installation and
  update execution were not tested; their syntax was checked against CLI help
  and official documentation.
- Official `skills-ref` **0.1.0**, upstream revision
  `69ef37e9424c0a7ea9dd2293b559e43ec8176379`: validation passed using Python UTF-8
  mode. Its first attempt failed because its default file read used Windows
  CP1252. The same environment issue affected the bundled quick validator; that
  passed with `python -X utf8`. No product change was needed for either tool.
- `python scripts/build_prompt.py --check`: passed; complete prompt content
  matches the authoritative skill, references, and packaged MIT notice.
- `python scripts/validate.py`: passed, covering package, links, modes, fixtures,
  documentation, synchronization, and known secret patterns.
- `python -m unittest discover -s tests -v`: **50 tests passed**, including
  **40 mutation tests**, on Windows Python 3.11.9. Earlier runs correctly failed
  while this log was absent; those failures were not counted as passes.

## Release assessment

Ready for maintainer review and publication as an initial educational **0.1.0**
release, with the limits below and the two minor smoke-test gaps disclosed.
The skill is 136 lines; the standalone prompt bundles the same rules, supporting
material, and license. Installation and gameplay require no Python dependencies;
the optional CLI uses Node/npm only for package management. Nothing has been
published by this work.

## Limits

Live installation/gameplay in Claude Code and Cursor, natural host discovery,
cloud surfaces, and remote installation of the unpublished revision have not
been tested. CI is configured for Ubuntu Python 3.10/3.13 and Windows 3.13 but
has not run remotely. Local Python is 3.11.9 on Windows. Documentation was checked
against primary sources; that is narrower evidence than host integration testing.
No empirical probability calibration, broad security audit, human user study,
or diverse-model benchmark was performed. The secret scan is heuristic.

The temporary installed skill was successfully removed by the CLI. Automatic
approval review blocked recursive cleanup of the remaining temporary QA directory
with the reason “blocked by policy”; its isolated validator environment remains
outside the repository. This does not affect the packaged files or test results.
