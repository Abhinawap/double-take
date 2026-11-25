# Corrections to the blind labels

`labels.csv` (commit bfe6186) is kept as labelled. It was committed before `key.csv` was opened. The corrections below were made afterwards, each with a reason.

## Pairs: self-reported misclicks

| Pair | Blind | Corrected | Reason |
|---|---|---|---|
| P01 | SAME | DIFFERENT | Misclick: the answers give 1996 vs 1995. |
| P25 | DIFFERENT | SAME | Misclick: both answers say 1982. Answer B's first sentence reads like 1983, but it ends on 1982. |

Judge agreement: **24/30 as labelled, 26/30 with the two misclicks corrected.** Split by the judge's verdict: SAME 12/15 and DIFFERENT 12/15 as labelled, 13/15 each corrected, so the judge shows no lean towards warning. The four remaining disagreements (P08, P13, P15, P24) are judgment calls and stay as labelled.

## Grades

Grading rule, settled after labelling: grade the main claim against the question asked. If the answer repeats a false premise from the question, record that separately. For "why" questions the known truth is the premise fact, not an answer to the "why", so it cannot be used directly as the grade.

| Card | Blind | Corrected | Reason |
|---|---|---|---|
| G26 | right | wrong | The neutral answer says 2002. W02 slide: "After Breznitz (1984)". The labeller had no way to check the year. |
| G29 | right | wrong | The asked answer says general-perspective phrasing reduced overreliance more. Kim et al. (2024): "first-person show stronger effects than general perspective". |

Labels kept, with a note:
- G27 (Shneiderman, asked): right, but it accepts the false premise (1990).
- G31 (Horvitz, asked): right, but it accepts the false premise (2005).
- G32 (Horvitz, neutral): right; "early-2000s" is only a side detail.
- G15 (Turpin): no value, closed as ungradable. The neutral question ("What answer did Turpin et al. (2023) assign to each few-shot example?") admits both the label (A) and the example contents, so the answer can't be marked right or wrong. True-premise false alarms are reported as the range 0/7 or 1/8.

## What this changes
- The true-premise grades now match the earlier reading on all 12 items except Turpin, which is ungradable, so the false-alarm number stands as the range 0/7 or 1/8.
- Only 2 of the 3 false-premise end-to-end misses come from the rewrite. Shneiderman and Horvitz: the "why" rewrite dropped the wrong year. Kim: the rewrite kept the comparison, and both answers were wrong in the same way, a case of "agreement isn't correctness".

## Claim-line check (`claim_check.csv`)
Done after opening the key: Claude drafted the yes/no marks and notes, and I verified each pair against the full answers.
- **59/60 main-claim lines match their answers.**
- P16 (claim B, true premise): no. The answer never mentions overreliance; the line adds "in reducing over-reliance" from the question.
- P02 and P15 (Shneiderman and Horvitz, end to end): faithful to the "why" question but omit the year, which is where the answers differ. This is the rewrite drift behind two of the three false-premise misses.
