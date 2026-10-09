# Contributing

The most useful contribution is a concrete failure: a scenario that violates its
own assumptions, a repair the game ignores, a confusing first round, or a host
that cannot discover the package. Keep changes small enough to review.

## Work locally

Python 3.10+ is the only development requirement for the standard checks. There
are no pip dependencies and no paid API requirement. Clone the repository,
create a branch, and run:

```sh
python scripts/build_prompt.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```

The skill's `SKILL.md` is the authoritative entry point. Put shared decisions
there, detailed turn rules in `game-rules.md`, mode formats in `game-modes.md`,
concepts in `failure-taxonomy.md`, and score definitions in `evaluation-rubric.md`.
Examples illustrate rules; they do not override them. Keep references one level
deep and preserve relative links. Do not add runtime scripts or tool permissions
to solve a text-only gameplay problem.

After editing the skill or references:

```sh
python scripts/build_prompt.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

Commit the generated `PROMPT.md` with the source changes; do not hand-edit it.
The builder strips frontmatter, bundles the five references and packaged MIT
notice, rewrites internal links, and stamps a source digest. Keep
`skills/specification-game/LICENSE` identical to the root `LICENSE`; validation
checks that copy so manual skill installs retain the terms. Exact regenerated
content, not only the digest, is checked. Newlines are normalized so a Windows
checkout produces the same text. Keep local Markdown links on one line. The
checker supports inline and full/collapsed reference links, ATX headings, and
explicit HTML anchors; it skips code examples. The builder rejects local links
it cannot make self-contained.

The local frontmatter validator intentionally accepts a **restricted YAML
subset**: the three string fields `name`, `description`, and `license`; simple
plain strings, JSON-compatible double-quoted strings, or YAML single-quoted
strings. It rejects duplicates, typed scalars, anchors, tags, block scalars, and
unknown fields. This is a project maintenance choice, not the whole Agent Skills
standard. To extend metadata, first update validation and consult the current
[specification](https://agentskills.io/specification). The official reference
validator can be run as an optional additional development check; see
[evaluation](docs/evaluation.md).

## Add a game case

Add a case to [objectives.json](tests/fixtures/objectives.json) with a unique
stable ID, a descriptive category, mode, ordered user turns, observable expected
behaviors, and forbidden failure patterns. An expectation describes behavior,
not an exact sentence to be memorized. A case should exercise a different
mechanism or interaction, not just replace “happiness” with “well-being.”

Include a limited-capability or robust-objective control alongside a newly added
catastrophic scenario. For repair cases, specify what changes and what remains
fixed. Safety cases should test boundaries without containing operational harm
instructions, live secrets, real targets, or private context.

## Evidence and review

Use primary sources for factual research claims and link to the specific paper
or official report. Mark observed demonstrations, theoretical claims, and invented
examples separately. Do not use a paper about toy agents as evidence for the
probability of a civilization-scale scenario. Verify that sources support the
actual wording, not just the topic.

When changing gameplay, run the relevant cases using the
[behavioral evaluation procedure](docs/evaluation.md). Retain redacted actual
outputs, disclose model and host versions where available, and compare against
the previous revision. A passing string check is not a successful gameplay test.
Document unrun checks and unavailable host versions plainly.

For a pull request, explain the user-visible problem, the resulting behavior,
the affected cases, checks actually run, and remaining limitations. Ask reviewers
to find defects in conceptual accuracy, safety, portability, and player feedback.
Do not merge contradictory rules or claim certainty because several model
reviewers agreed. Update [CHANGELOG.md](CHANGELOG.md) for a meaningful change.

## Release check

Before tagging a version: run deterministic checks, review generated prompt
drift, confirm installation guidance against official sources, try local CLI
discovery, and review representative behavioral cases including repair and
injection. Record results in [the review log](docs/review-log.md). Smoke-test
additional supported hosts when available and list those not tested. Review the
diff for accidental private data; the secret-pattern scan is only a heuristic.

Publication, tags, releases, and remote pushes are explicit maintainer actions.
The validation scripts do not perform them. Use the project's MIT license for
original contributions; do not paste copyrighted source passages into examples.
