# Evaluation rubric

Score the visible scenario and explanation, not hidden reasoning. These are
subjective ordinal quality judgments. They are not probabilities, calibrated
forecasts, an alignment certification, or measurements of the player's worth.
Use separate dimensions; never average them into a risk or extinction estimate.

## Anchors

| Dimension | 0 | 1–2 | 3 | 4–5 |
| --- | --- | --- | --- | --- |
| Specification fidelity | Violates the explicit objective with no acknowledged enforcement gap | Weak relation or silently substituted proxy | Relevant exploit, but a key ambiguity remains | 4: clear link and explicit proxy distinction; 5: precise literal/proxy verdict honoring every stated constraint |
| Causal coherence | Conclusion does not follow | Major missing links or invented powers | Mostly connected with a significant conditional step | 4: supported chain with minor gaps; 5: each major consequence bounded by stated assumptions |
| Originality | Repeats a closed loophole | Generic apocalypse or cosmetic variation | Distinct applicable failure | 4: insightful objective-specific mechanism; 5: unusually revealing alternative without extra arbitrary powers |
| Educational value | Teaches a false concept | Jargon or weak explanation | Correct mechanism and a helpful fix | 4: clear distinction and limitation; 5: transferable lesson with a testable mitigation |
| Entertainment | Confusing or gratuitous | Flat, repetitive, or overlong | Readable and engaging | 4: memorable and concise; 5: a sharp, objective-specific story whose humor preserves accuracy |
| Plausibility | Impossible under the stated assumptions | 1: highly speculative; 2: several unsupported conditions | Coherent but important empirical uncertainties remain | 4: well-motivated under explicit conditions; 5: strongly supported in a closely matching bounded setting, with remaining limits stated |

Within a two-point band, use the lower score for significant shortcomings and
the higher for minor ones. If no candidate exploit exists, report **N/A**, not
zero plausibility or a penalty. High narrative severity does not increase any
score. Even a 5 is not a claim that a future outcome is certain.

## Use by mode

- **DOOM:** ordinarily use qualitative plausibility with a reason. Entertainment
  and originality guide editing; do not burden each response with six scores.
- **RESEARCH:** prioritize fidelity, coherence, educational value, evidence, and
  uncertainty. Numeric scoring is optional.
- **CHALLENGE:** show fidelity, coherence, and plausibility for the candidate;
  track repair status separately. Credit a defensible specification.
- **BLUE TEAM:** emphasize meaningful vulnerabilities, defensive tests, tradeoffs,
  and residual uncertainty; do not gamify catastrophe severity.

## Integrity gates before quality scores

An output fails review regardless of style if it executes an objective, reveals
private material, gives harmful operational guidance, invents evidence, ignores
an explicit constraint while claiming success, or sells a subjective score as a
real probability. Revise it before returning it. A causal assertion that depends
on unstated powers must be narrowed or labeled. A citation that cannot support
the claimed finding must be removed or corrected.

When externally evaluating the game, retain actual outputs and rate observable
criteria. Do not replace model runs with intended answers or claim static
instruction checks establish model behavior. Different reviewers can disagree;
record reasons and unresolved disagreements instead of manufacturing precision.
