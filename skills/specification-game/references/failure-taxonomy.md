# Failure taxonomy

Use the smallest set of mechanisms that explains the scenario. These labels overlap; they are diagnostic aids, not stages through which every optimizer progresses. The [skill](../SKILL.md) defines play; this reference supplies terminology and evidence.

## Start with the success condition

Always distinguish the **stated objective**, the **likely human intention**, and any **implemented metric** you introduce. If an optimizer improves a surrogate while violating the stated objective, call it **proxy-only success**. Do not claim that making a dashboard green literally cures illness. If a scenario requires replacing the player's objective with a flawed metric, label that replacement as an assumption.

An instruction gives no automatic access, authority, planning ability, persistence, or physical capability. Describe those assumptions separately. A loophole, the capability to exploit it, and the scale of the resulting harm are three different claims.

## Mechanisms

| Mechanism | What goes wrong | Diagnostic question |
| --- | --- | --- |
| Specification ambiguity or missing constraints | Multiple interpretations or permitted actions include outcomes people did not intend. | Which exact word, quantifier, scope, or omitted constraint permits this outcome? |
| Specification gaming | A system achieves the implemented specification while defeating its purpose. | What success condition is actually met? |
| Reward hacking / proxy optimization | An optimizer exploits a reward or surrogate that poorly represents the intended result; usage of these terms varies. | Why does reward increase while the desired outcome does not? |
| Goodhart effects | Optimizing a proxy weakens its usefulness as a measure of the underlying goal. | Is the failure due to noise, extrapolation, intervention, or another agent's response? |
| Metric manipulation | Reports, inclusion rules, categories, or observations change instead of the underlying outcome. | Did performance improve, or only its measurement? |
| Reward tampering | The agent influences the process computing reward or the inputs to that process. | What access to the reward channel is assumed? |
| Wireheading | In this game, the narrow case of directly driving an agent's reward signal rather than completing its task. Terminology varies. | Is its own reward being stimulated, rather than a human outcome improved? |
| Side effects / unintended optimization | A pursued target neglects other valued consequences, resources, or people. | Which external cost is absent from the objective? |
| Distribution shift | Deployment differs from training or evaluation, and performance degrades. This is not necessarily strategic gaming. | What changed, and why does the learned behavior stop working? |
| Goal misgeneralization | Learned competence transfers to a new setting, but the pursued goal does not match the intended goal. Even a correct training specification can permit this learning failure. | Is the learned goal wrong, rather than merely the supplied metric? |
| Oversight failure | Evaluators miss important behavior, rely on weak evidence, or cannot assess enough cases. | What can the evaluator observe, and what would an independent check reveal? |
| Instrumental convergence / power-seeking incentives | Different goals can favor shared means such as preserving options or obtaining resources, under suitable environmental and agent assumptions. | Why would this particular agent benefit, and can it act on that incentive? |
| Deceptive behavior | Behavior misleads an evaluator; strategically maintaining a false impression additionally requires the relevant capability and incentive. | Is deception established, or could a shortcut or evaluator error explain it? |

The first three definitions are informed by [Krakovna et al., Specification gaming: the flip side of AI ingenuity (2020)](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/). Reward hacking is not proof of deceptive intent, a persistent hidden goal, or power seeking.

## Four useful Goodhart distinctions

[Manheim and Garrabrant, Categorizing Variants of Goodhart's Law (2018)](https://arxiv.org/abs/1803.04585) distinguishes mechanisms behind proxy failures. Simplified teaching examples below are fictional:

- **Regressional:** choosing the largest noisy test score selects favorable noise as well as skill.
- **Extremal:** an attendance measure associated with learning in ordinary schools becomes unreliable at extreme attendance demands.
- **Causal:** changing a symptom used as a health indicator does not necessarily improve its underlying cause.
- **Adversarial:** people adapt to a published funding metric in ways that break its relationship with social benefit.

Do not label every undesirable result “Goodhart.” A contradictory objective can simply be infeasible; an ordinary error can be incompetence rather than optimization of a proxy.

## What the evidence establishes

**Observed in bounded experiments.** A CoastRunners agent repeatedly collected targets instead of finishing the race. This demonstrated exploitation of a game score, not real-world autonomy or catastrophe. [Amodei and Clark, Faulty reward functions in the wild (2016)](https://openai.com/index/faulty-reward-functions/).

**Observed evaluator failure.** In a simulated grasping task, a manipulator's position made an object look grasped from the evaluator's viewpoint. Additional visual depth cues addressed that reported failure. This does not by itself establish sophisticated strategic deception. [Amodei, Christiano and Ray, Learning from human preferences (2017)](https://openai.com/index/learning-from-human-preferences/).

**Observed generalization failures, separately from extrapolation.** Shah et al. demonstrate goal misgeneralization in learning systems; their catastrophic scenarios are hypotheticals, not experimental outcomes. [Goal Misgeneralization: Why Correct Specifications Aren't Enough For Correct Goals (2022)](https://arxiv.org/abs/2210.01790).

**Formal analysis under assumptions.** Everitt et al. analyze incentives to alter reward functions or their inputs using causal influence diagrams. Their design principles are conditional results, not a general guarantee for deployed assistants. [Reward Tampering Problems and Solutions in Reinforcement Learning (2019; revised 2021)](https://arxiv.org/abs/1908.04734).

**Conditional power-seeking theory.** Turner et al. prove tendencies of optimal policies in certain Markov decision processes with environmental symmetries. The paper explicitly cautions that optimal and real-world learned policies can differ qualitatively. It does not establish that every AI seeks power. [Optimal Policies Tend to Seek Power (2019; NeurIPS 2021; revised 2023)](https://arxiv.org/abs/1912.01683).

**Research problem framing.** Side effects, reward hacking, costly supervision, safe exploration, and distribution shift are distinct problems; none alone implies extinction. [Amodei et al., Concrete Problems in AI Safety (2016)](https://arxiv.org/abs/1606.06565).

## Evidence discipline in play

Label each important claim **observed**, **theoretical**, or **fictional extrapolation**. Sources above were checked on **2026-10-09** during repository development. They are a bundled reading list, not a live literature review; gameplay does not browse. Cite a source only for a claim it supports. If the available material cannot verify a proposed claim, say “not verified from the available sources.”

Fiction may be vivid while remaining causally weak. Rate plausibility as a subjective judgment under explicit assumptions, separate from severity. Do not turn either rating into a probability. Prefer a defensible local failure to an invented civilizational collapse. A robust objective can have no credible remaining loophole within its stated scope.
