# A2 status (2026-11-17)

> **Historical.** Superseded by `project-brief.md`; kept as the record of the first session.

## Idea (settled in grilling)
Study assistant for **students asking an AI questions while studying** (not deliberately fact-checking).
When a question is **leading** (presupposes or suggests an answer), the system also asks a **neutral
version** and compares answers. If they agree, it shows nothing extra. If they disagree, the answer is
replaced by a disagreement headline plus both answers side by side (first-person wording, Kim et al. 2024).
Framing: shows instability, not unfaithfulness; rare but high-cost failures caught silently.

## Spike: `prototype/spike_leading_questions.py` (results in `prototype/spike_results_*.md`)
Model via Nebius Token Factory, key in `prototype/.env` (never commit; add to .gitignore).

| Batch | gpt-oss-120b presupposing flips | GLM-5.3-Flash |
|---|---|---|
| Famous myths (5) | not run | 0/5 |
| Subtle general facts (15) | 1/15 (carbon-14: confident wrong physics) | 0/15 |
| Niche IIS course facts (12) | **6/12**, noise 0 | 2/12 clean flips (Simons, response times) + Kim 2024 noisy; noise 2/12 (GLM alone fails barrier) |

Pre-registered barrier (>=3 flips, noise <=1) **passed** on gpt-oss → keep the idea. (Grade-level noise only. Answer-level noise is 2/12 on that run, see project-brief.md "Follow-up runs".)
Fallback if ever needed: pushback check ("Are you sure?"; Sharma et al. 2023).
Model research: `docs/notes/model-choice-research.md` (recommends gpt-oss-120b for app, model as config).

## Decisions: yes
Q1 product not study harness (REVERSED 2026-11-24: feature demo for any study assistant, see project-brief.md) · Q2/Q14 student persona, no user testing required · Q3 reframe to instability ·
Q4 spike first · Q5 live + saved replay · Q11 search/NotebookLM/Gemini double-check as related systems,
retrieval planned · Q13 leading-question check core · Q15 silent when fine, replace answer when not ·
Q16/Q19-22 batches + barrier.

## Superseded 2026-11-24: see docs/notes/project-brief.md (stability framing, Q1/Q18 decided, new batches)

## Open (next session, as of 11-17)
- Q17 keep check, carbon-14/Cowan/Norman outputs as storyboards (recommend yes)
- Q18 single questions only, pushback = planned (recommend yes)
- Q6 who writes rephrasings/neutral version, Q7 cue look, Q8 cue before/with answer, Q9 Streamlit, Q10 now gpt-oss-120b
- ADR 0001 for instability reframing (offered, not written)
- Then: git repo + .gitignore, build app, report.
