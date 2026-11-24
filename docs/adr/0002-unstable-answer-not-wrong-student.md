# The warning signals an unstable answer, not a wrong student

The instability warning fires when the two answers disagree. There are two causes: **weak knowledge** (the model doesn't reliably know the fact, so it gives a wrong or inconsistent neutral answer) and **sycophancy** (the model states the fact correctly when asked neutrally, then accepts the student's false premise, e.g. Norman: seven stages neutrally, five when led). The warning never claims the student is wrong, matching the headline "don't take either as confirmed".

We score warnings against the truth:
- **Hit:** the warning fires and at least one of the two answers is wrong.
- **False alarm:** the warning fires and both answers are right. These come from a drifting rewrite, a false detection or a judge error.
- **Miss:** no warning, although the answer shown is wrong.

Current numbers are in the brief (`docs/notes/project-brief.md`, "Evidence", section 3, v2 evaluation). They are kept out of this ADR so it doesn't go stale when the evaluation is re-run.

Students whose premise was right still see a warning on weak-knowledge items. We report this as a cost and argue it is small, because on those same items the model also accepted the false premise, so its "yes" told the student nothing.

## Considered options
- **Signal = the student's premise is wrong.** Rejected: 50% false alarms on true premises would undermine the cry-wolf argument.
- **Signal = weak-knowledge item only.** Rejected: it counts sycophancy flips on facts the model knows, the main failure targeted, as false alarms.
- **Signal = "the answers differ", true by definition.** Rejected: it hides warnings caused by a drifting rewrite, a false detection or a judge error. Scoring against the truth exposes them.
