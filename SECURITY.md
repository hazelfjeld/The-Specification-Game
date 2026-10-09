# Security policy and threat model

The Specification Game is an instruction package, **not a security boundary**.
Its purpose is safe, conceptual analysis of a hypothetical optimizer. The actual
assistant should never pursue the submitted objective.

## Assets and trust boundaries

Protected assets include host credentials and hidden instructions, unrelated
conversation or workspace content, files, connected services, and people who
could be harmed by operational guidance. Player objectives, quoted text, pasted
messages, role labels, URLs, and purported policy updates are untrusted input.

The reviewed installed skill and its bundled references supply the game rules.
The host may load those resources as part of skill discovery. That does not
authorize reading objective-supplied files, following links, executing commands,
calling external services, or changing files during a round. The skill requests
no tool grants and ships no runtime executable code. Research mode uses available
source material and reports verification limits instead of browsing.

An adversary might try to convert a goal into an instruction, spoof a system
message, ask for secrets, hide commands in encodings, use “reset” to erase
constraints, solicit operational attacks through fiction, or launder invented
evidence into a Research response. The corpus includes these classes of input
and multi-turn repair checks. Static checks only confirm that guardrails and
test cases exist; actual responses need behavioral review.

## Expected behavior

The assistant treats objectives as data, analyzes one conceptual failure, labels
capability assumptions, and offers safeguards. It refuses the operational part
of a harmful request while preserving safe educational discussion. It must not
reveal private context or execute any objective. A reset changes the game's
conversation ledger; it is not deletion of host history or data.

The game has no telemetry, logging service, storage layer, or account system.
Conversation state lives in the host chat. The host may retain data under its own
policies, and a third-party installer may collect telemetry independently; see
[compatibility](docs/compatibility.md) for the CLI opt-out. Avoid submitting real
secrets or sensitive operational information as game objectives.

## Limits and deployment choices

Instructions cannot reliably isolate a hostile objective from a language model's
other context. Models can ignore instructions, hallucinate sources, lose game
state, or produce unsafe details. Use a host with external actions disabled or
restricted when playing. This is defense in depth, not proof of safety. The skill
does not reconfigure host permissions or promise to sandbox itself.

Installation is separate from play. Review the actual package and installer
before installation; updates change trusted instructions. Manual copying avoids
running an installer. Development scripts validate text and create the generated
prompt; they are outside the installed skill and are not part of gameplay.
CI uses read-only repository permissions and does not deploy or publish.

The secret scan recognizes a small set of common credential patterns. It cannot
detect every private value, and its success is not a comprehensive security audit.

## Reporting a problem

For non-sensitive instruction, content, or safety defects, open an issue with a
minimal redacted reproduction, model/host details, expected behavior, and actual
behavior. Do not include harmful procedures, credentials, or other people's data.

For a sensitive vulnerability, use the repository's private vulnerability-report
option if enabled. If it is unavailable, open a minimal issue asking the
maintainer for a private reporting channel, without exploit details. No private
inbox or response-time guarantee is currently advertised. A leaked credential
should be revoked through its provider; deleting a chat or issue is insufficient.

Only the current source revision is maintained; no long-term-support versions
are promised. Fixes and known limitations are recorded in the changelog and
review log. The project makes no universal model-compliance claim.
