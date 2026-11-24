# Show instability, not unfaithfulness

A1's research question had two parts: can everyday users detect unfaithful LLM explanations, and does showing how the model's answers differ across rephrased versions of the same question help them reject wrong answers? Unfaithfulness can't be observed from outside the model, but a disagreement between two answers can be. So the system takes the second part: it shows students that an answer is unstable and makes no claim about whether the reasoning is faithful.

The original spike measured flips in right/wrong grades. The follow-up runs measured disagreement directly, comparing answer against answer with a noise baseline.

## Considered options
- **Detect unfaithful explanations.** Rejected: there is no ground truth for faithfulness at run time.
- **Express uncertainty from the model's self-reported confidence.** Rejected: an LLM has no "I do not know" state unless the system builds one (W03 L08, hallucination), models rarely express uncertainty unprompted (Zhou et al., 2024), and a self-report shows what the model said, not what it did (ELIZA effect).
