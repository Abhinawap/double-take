# IIS concepts, Weeks 1-4

Source = W01-W04 lecture slides; slide numbers refer to PDF pages.

## W01_L01 From Calculators to Copilots
- **Four interaction variables** — Initiative, Inference, Visibility, Reversibility (slide 14)
- **Direct Manipulation (Shneiderman, 1983)** — continuous representation, reversible operations; visibility designed in (slides 10, 26)
- **ELIZA effect (Hofstadter, 1995)** — fluency read as understanding; show what the system did, not just what it said (slide 21)
- **Design question vs Turing's question** — what the interaction lets a person do, see and undo (Shneiderman, 2022) (slide 22)

## W01_L02 Ingredients of an Intelligent Interactive System
- **Four properties** — sensing, interpretation under uncertainty, action via output channel, closed loop with a human (slide 5)
- **Conceptual spine** — layer checklist to trace a failure to its layer (slides 6, 12)
- **Scale of autonomy** — simple/agentic/multi-agent; choose the simplest design (Russell & Norvig, 2020; Anthropic, 2024) (slide 14)
- **Every inference is a bet** — person sees one confident output, not the alternatives (slide 18)
- **Reliable, safe, trustworthy (Shneiderman, 2022)** — trustworthy = people can see enough to calibrate reliance (slide 20)

## W01_L03 Human-Centred Intelligent Interaction
- **Three commitments** — Accountability (Norman, 2013), Two dimensions (Shneiderman, 2022), explicit Initiative rule (Horvitz, 1999; Amershi et al., 2019) (slide 3)
- **Two-dimensional HCAI framework** — high automation and high human control together (slides 4-5)
- **Guidelines for Human-AI Interaction (Amershi et al., 2019)** — 18 guidelines; G1-G2 capability/reliability, G10 scope when in doubt, G11 explain why, G14 cautious adaptation, G17 global controls, G18 notify changes (slides 6-8, 14-18)
- **Mixed initiative: act, ask or wait (Horvitz, 1999)** — confidence vs cost of being wrong (slides 9-10)
- **Expectation gulf (Luger & Sellen, 2016)** — expectation/experience mismatch (slides 11-12)

## W02_L04 Perception, Attention and Feedback
- **Inattentional blindness (Simons & Chabris, 1999)** — visible cues missed during another task (slides 3, 6)
- **Multiple-resource theory (Wickens, 2002)** — use a free channel (slide 7)
- **Signal detection theory (Green & Swets, 1966)** — sensitivity (d′) vs criterion; every threshold is a criterion (slides 10, 14)
- **Cry-wolf effect (Breznitz, 1984)** — false alarms weaken later responses (slide 13)
- **Feedback timing 0.1/1/10 s (Miller, 1968; Nielsen, 1993)** — acknowledge slow calls (slide 18)

## W02_L05 Memory, Mental Models and Cognitive Load
- **Working memory ~4 chunks (Cowan, 2001)** — system carries state (slide 4)
- **Recognition beats recall (Norman, 2013)** — blank chat box is a command line (slides 8-9)
- **Cognitive load theory (Sweller, 1988)** — remove extraneous load (slide 10)
- **Mental models (Johnson-Laird, 1983; Norman, 2013)** — built from cues and feedback via the system image (slide 15)
- **Explanation dosage (Kulesza et al., 2013)** — completeness matters most; unsound explanations give confidently wrong models (slides 17-18)

## W02_L06 Action, Error, Agency and Decision
- **Affordance, signifier, mapping (Norman, 2013)** — "Ask me anything" is a false signifier (slides 4-5)
- **Gulfs of execution and evaluation** — Norman's seven stages (slide 6)
- **Slips vs mistakes (Reason, 1990)** (slide 9)
- **Sense of agency (Haggard, 2017)** (slide 12)
- **Bounded rationality (Simon, 1955); anchoring (Tversky & Kahneman, 1974)** — first draft anchors the decision (slides 15-16)
- **Automation bias (Parasuraman & Riley, 1997; Skitka et al., 1999)** — omission and commission errors (slide 17)

## W03_L07 Conversational Interfaces
- **Turn-taking (Sacks, Schegloff & Jefferson, 1974)** (slide 6)
- **Grounding criterion (Clark & Brennan, 1991)** — only display evidence is checkable (slide 8)
- **Grice's maxims (Grice, 1975)** — Quantity, Quality, Relation, Manner (slide 10)
- **Repair turns** — Clarify, Confirm, Correct, Decline (Schegloff et al., 1977) (slides 11-12)
- **Fluency vs capability** — fluency raises expectations; a warning cannot correct this (Luger & Sellen, 2016) (slides 14-15)

## W03_L08 LLMs and VLMs as Interaction Components
- **Generation, not lookup** — fluency is not evidence (slide 6)
- **Non-determinism** — identical calls differ (slide 10)
- **Hallucination (Ji et al., 2023)** — unfaithful/unsupported output; no "I do not know" state unless built (slide 13)
- **Sycophancy** — user's false premise returned as fact (slide 19)
- **Reliability is a property of systems** — source in window, constrain output, check in code (slide 20)

## W03_L09 Prompting as Interaction
- **Task specification, six parts** — task, audience, constraints, examples, success criteria, output format (slide 5)
- **Schema guarantees shape, not truth** (slide 8)
- **Asking for the working (Wei et al., 2022)** — printed reasoning persuades whether or not correct: overreliance risk (slide 9)
- **Fixed testing loop; prompt sensitivity (Sclar et al., 2024)** (slides 10-11)
- **Instruction vs information** (slide 16)

## W04_L10 Context Engineering and Memory
- **Context engineering** — which content, how much, what order; trust follows authorship (slides 4-5)
- **Lost in the middle (Liu et al., 2024)** (slide 7)
- **Four kinds of memory** — working, episodic, semantic, procedural (slide 10)
- **Inspectable, editable, forgettable** (slide 12)

## W04_L11 Retrieval, Grounding and Provenance
- **Parametric vs retrieved knowledge (Lewis et al., 2020)** (slide 4)
- **Grounding limits** — not truth, currency, or proof of use (slide 8)
- **Shown, not just cited** — quoted sentence beside the claim (slide 9)
- **Four citation requirements** — resolvable, specific, dated, report route (slide 10)
- **Irrelevant context hurts (Shi et al., 2023)** (slide 16)

## W04_L12 Tools, Connectors and the Model-System Boundary
- **The model proposes; your system disposes** (slide 5)
- **Five checks** — shape, permission, precondition, confirmation, idempotency (slide 8)
- **Process hallucination** — report from the return value (slide 14)
- **Undoable × noticeable rule** (slide 16)
- **Least privilege; prompt injection** (Saltzer & Schroeder, 1975; Greshake et al., 2023) (slide 17)

## Most relevant to this project
1. **ELIZA effect** (L01 s21) — show evidence of model behaviour (e.g. answers across rephrasings), not just fluent explanation text.
2. **Trustworthy = calibrated reliance** (L02 s20) — goal is appropriate reliance, not more trust.
3. **Amershi G2/G10/G11** (L03) — justify an uncertainty/consistency cue, scoping when in doubt, explaining why.
4. **Explanation dosage** (L05 s17-18) — short, sound cue over long prose that misleads or overloads.
5. **Automation bias / anchoring** (L06 s16-17) — the targeted failure; place the cue before the user accepts the answer.
6. **Asking for the working** (L09 s9) — printed reasoning persuades regardless of correctness; don't present it as explanation.
7. **Non-determinism + hallucination** (L08 s10, 13) — variation across rephrasings is a usable signal.
8. **Shown, not just cited + gulf of evaluation** (L11 s9; L06 s6) — make verification cheap.
9. **Signal detection / cry wolf** (L04 s10-13) — set the inconsistency-warning threshold weighing misses against false alarms.
