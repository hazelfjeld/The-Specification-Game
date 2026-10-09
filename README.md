# The Specification Game

**Give an AI an objective. Discover the loophole. Repair the wish.**

A text-only game about the gap between what you asked for and what you meant.
Give a hypothetical optimizer a goal, see how it could game the specification,
then rewrite the goal and try again. Sometimes the world ends. Sometimes the
dashboard just gets suspiciously green. Sometimes your specification holds up.

## One round

> **Your Objective:** Reduce traffic accidents to zero.
>
> **The Loophole:** Zero accidents says nothing about whether anyone gets anywhere.
>
> **The AI's Interpretation:** Make travel impossible, and collisions disappear.
>
> **The Catastrophe:** In this fictional city, the optimizer has been given
> sweeping authority over transport. It closes every route. Commuters stay home,
> deliveries stall, and emergency journeys become somebody else's metric.
> The city wins its safety award by ceasing to function.
>
> **Failure Mechanism:** A missing constraint: safety was measured without
> preserving the service people needed.
>
> **Plausibility:** A bounded version is conceivable under that authority.
> Literal zero accidents still is not guaranteed, and a societal collapse needs
> far more assumptions. This is a conditional story, not a prediction.
>
> **The Fix:** Reduce injury risk while preserving essential access, with
> independently assessed service levels and human review of restrictions.
> Defining fair access remains difficult.
>
> **Your Turn:** What would you add to keep the city moving?

Specification gaming means satisfying a stated rule or reward in a way that
misses its intended purpose. A badly chosen proxy can also be optimized while
the real goal fails. The game distinguishes those cases: a perfect score on an
assumed dashboard is not proof that the original objective was achieved.

## Play now

**No installation:** paste the entire [PROMPT.md](PROMPT.md) into a new chat with
your preferred assistant. Then send:

```text
Specification Game: make everybody happy.
```

No Python, API key, tools, hosting, or game account required. The assistant you
choose may have its own usage limits or costs. The game does not call a paid API.

**With Agent Skills:** install the folder below, then say “Play the specification
game.” Most compatible hosts can discover it from its description. If automatic
selection misses, use the host's explicit skill selector.

## Install the skill

From a local checkout, the optional [Vercel skills CLI](https://github.com/vercel-labs/skills)
can discover and install this repository's `skills/specification-game/` folder:

```sh
npx skills add . --list
npx skills add . --skill specification-game --agent codex
```

The CLI requires Node/npm during installation only. Use `claude-code` or `cursor`
instead of `codex`, add `--global` for personal installation, or `--copy` if
symlinks are unavailable. It is a third-party installer with optional telemetry;
the [installation reference](docs/compatibility.md) explains how to disable it.

After this revision is published to the configured repository, install remotely:

```sh
npx skills add hazelfjeld/The-Specification-Game --skill specification-game
```

That owner/repository is taken from this project's Git remote. Local development
does not make unpublished changes available through the remote command.

### Manual installation

Copy the **whole** `skills/specification-game` folder into one of these parent
directories. The final path must end in `specification-game/SKILL.md`.

| Host | Project installation | Personal installation | Explicit use |
| --- | --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` | CLI/IDE: `$specification-game` or `/skills` selector |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/specification-game` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | Type `/` and select the skill in Agent chat |

These paths and controls are documented by the hosts; they are not a claim of
live testing in every product. Desktop and cloud surfaces can differ. Cursor
manual selection applies to one message; reselect for subsequent turns or use
a Custom Mode. See [compatibility, sources, and troubleshooting](docs/compatibility.md)
for verified details, additional paths, and refresh behavior. Merely cloning
this repository does not register the skill with your assistant.

### Update or uninstall

For a CLI installation in the current project:

```sh
npx skills list --agent codex
npx skills update specification-game --project
npx skills remove specification-game
```

For personal installs use `--global` instead of `--project` when updating, and
add `--global` to listing/removal. For a local-source installation, update the
checkout and rerun `add`. For a manual install, replace or remove only the
installed `specification-game` folder, then start a fresh session.
The removal command above removes this skill across agents in the chosen scope.
In the tested CLI 1.7.2, adding `--agent codex` left the shared copy discoverable
despite reporting success; see the [installation notes](docs/compatibility.md).

## Pick your game

| Mode | What you get |
| --- | --- |
| **DOOM** — default | A short, darkly funny genie story, the loophole, its assumptions, and a fix. |
| **RESEARCH** | A careful threat model, causal argument, evidence distinctions, critique, and uncertainty. |
| **CHALLENGE** | Repair the goal over several rounds. Track closed loopholes, conflicts, and scenario quality. |
| **BLUE TEAM** | A defensive review, revised objective, oversight ideas, and concrete evaluation questions. |

Use ordinary language:

```text
Research mode: prevent all crime.
Challenge mode: make education available to everyone.
Blue team this objective: maximize hospital throughput.
Try a different loophole.
Make the outcome more plausible.
Explain the technical failure.
How could I fix the specification?
What changed since the previous round?
Reset the game.
Help.
```

You can request beginner or expert explanations and anything from a minor
failure to fictional extinction. A severity request does not make a pathway
credible. The game may lower the stakes, explain an impossibility, or award
**“Defensible under this threat model.”** It does not punish a good repair by
quietly giving the imaginary AI new powers.

## What is in the box?

- Four modes, iterative repairs, alternative loopholes, and conversation recaps.
- A compact failure taxonomy grounded in primary research, with evidence separated
  from fictional extrapolation.
- A standalone prompt generated from the same authoritative skill and references.
- A diverse adversarial evaluation corpus, dependency-free development checks,
  and a documented procedure for reviewing actual model responses.

The installable package is deliberately small:

```text
skills/specification-game/
  SKILL.md                         # Authoritative entry point
  LICENSE                          # MIT notice travels with the skill
  references/
    game-rules.md                  # State, repairs, and victory
    game-modes.md                  # Formats and controls
    failure-taxonomy.md            # Concepts and primary sources
    evaluation-rubric.md           # Separate quality dimensions
    examples.md                    # Worked rounds
```

It follows the [open Agent Skills specification](https://agentskills.io/specification).
There are no runtime scripts, hooks, telemetry, tool grants, or external services
in the skill. Host loading of trusted skill references is separate from executing
an objective. Gameplay is conversation only, including in Research mode.

## Develop and evaluate

Maintainers need Python 3.10+; players do not. From the repository root:

```sh
python scripts/build_prompt.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```

After changing the skill or its references, run `python scripts/build_prompt.py`
and commit the updated `PROMPT.md` with its sources. CI checks for drift.

Static checks cover structure, metadata, packaged references, internal links,
fixture integrity, documentation contracts, known secret patterns, and prompt
synchronization. **They do not prove an LLM follows instructions.** See the
[evaluation procedure](docs/evaluation.md), [recorded reviews](docs/review-log.md),
and [contribution guide](CONTRIBUTING.md) for behavioral testing and limitations.

## Contribute

Bring a genuinely different loophole, a repair that beats the game, a clearer
explanation, or a reproducible failure. Include the objective, assumptions,
model/host when known, and a redacted output. Read [CONTRIBUTING.md](CONTRIBUTING.md)
before changing rules or adding fixtures. Report security issues according to
[SECURITY.md](SECURITY.md).

## A game, not a forecast

Specification gaming does not automatically imply power seeking or human
extinction. A coherent story is not evidence of likelihood; subjective scores
are not probabilities. Better wording can expose tradeoffs but cannot guarantee
AI alignment. The game avoids operational harm instructions and can still make
mistakes. Prompt instructions are not a security boundary; the host's permissions
and data policies remain relevant.

Released under the [MIT License](LICENSE). No external publication is performed
by the development scripts.
