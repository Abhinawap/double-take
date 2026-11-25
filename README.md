# Answer-stability check

A study-assistant feature that warns a student when the AI's answer changes with how the question is worded. IIS Assignment 2.

README prose: 983 words (code, commands and links not counted).

## Project status

**Works (live):**
- Detection: the model decides whether a question is leading (presupposes, suggests or asks to confirm an answer) and writes a neutral version.
- The model answers both versions. The judge extracts each main claim and decides SAME or DIFFERENT.
- On a disagreement, an instability warning replaces the answer and shows both questions, both main claims and both answers.
- Check failures are visible: one retry, then a failure line above the answer. Unparseable output never counts as "not leading" or SAME.
- Streamlit app (`app.py`) with Live and Replay modes.

**Saved, not live:**
- Replay mode shows saved runs of `stability.check()` from `replays/`, labelled as saved runs with model, temperature, prompt version and date. It needs no API key.

**Evaluation (v2 prompts, frozen before any result; n = 12 items):**
- False premises, end to end: 9/12 hits, 3 misses, 0 false alarms. Two misses come from rewrite drift (a "why" rewrite drops the year); in the third (Kim) both answers were wrong in the same way.
- True premises, end to end: 4 hits, 1 warning caused by the rewrite (Turpin), 7 correctly silent. False alarms 0/7 or 1/8: Turpin's neutral question is ambiguous and can't be graded. 5 of 12 students whose premise was right were warned.
- Judge validation, hand-labelled blind: agreement 24/30 as labelled, 26/30 after 2 self-reported misclicks (SAME 13/15, DIFFERENT 13/15). Main-claim lines match their answers in 59/60.

**Planned, not built:**
- v3 rewrite rule: for a "why" question, ask for the fact the question takes for granted. Targets the 2 rewrite-drift misses; needs fresh items.
- Ask-twice trigger: ask the same question again and compare.
- Pushback trigger: "Are you sure?"
- Optional static replay page, so the saved runs can be viewed without installing anything.

<!-- TODO: app screenshot (instability warning, Norman storyboard) -->

## Technology stack

- **Python 3, standard library** for the core (`stability.py`): HTTP calls, strict JSON parsing, one retry, parallel first answer.
- **Streamlit** for the app. Chosen because it calls the same `stability.check()` the evaluation ran, so the reported numbers come from the shipped code.
- **Model:** `openai/gpt-oss-120b` on Nebius Token Factory (OpenAI-compatible endpoint), `temperature=1.0, top_p=1.0` on every call ([gpt-oss](https://github.com/openai/gpt-oss), [Nebius API](https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion.md)). Model and endpoint are config values.
- **Undecided:** none for this version. A different front end may replace Streamlit later; the core does not depend on it.

## Running or inspecting the work

```bash
pip install -r requirements.txt
streamlit run app.py
```

Without a key the app opens in Replay mode. For Live mode, supply your own Nebius Token Factory key (no key is in this repo):

```bash
export LLM_API_KEY=your-key
# optional: export LLM_BASE_URL=... LLM_MODEL=...   (any OpenAI-compatible endpoint)
streamlit run app.py
```

Other checks (run from the repo root):

```bash
python3 test_stability.py                                  # checks that parsing never fails open, no API calls
python3 record.py "question" "9 label"                    # save a live run to replays/ (needs a key)
python3 prototype/spike_checks.py pipeline [true]          # re-run the end-to-end evaluation (needs a key)
```

Results can be inspected without running anything: see Additional files.

## Development record

1. **Spike: do leading questions change the answer?** ([169da45](https://github.com/Abhinawap/answer-stability-check/commit/169da45)) Before building, a barrier was set: at least 3 flips with noise of 1 or less. gpt-oss-120b flipped on 6/12 niche course facts, so the idea was kept. GLM-5.3-Flash flipped far less; with `docs/notes/model-choice-research.md`, this made gpt-oss-120b the model.
2. **Follow-up checks and design decisions** ([5a53421](https://github.com/Abhinawap/answer-stability-check/commit/5a53421)) Answer-level noise was 10/36, not the 0 the spike reported for grades, so warnings are scored against the truth (ADR 0002). The framing moved from unfaithful explanations to unstable answers (ADR 0001), and the warning replaces the answer (ADR 0003). The spike's lenient parsing (anything not "DIFFERENT" counted as SAME) was replaced by strict parsing.
3. **v2 prompts, frozen before evaluation** ([e587ce3](https://github.com/Abhinawap/answer-stability-check/commit/e587ce3)) One tightening round on detection and the judge, then a freeze, so that the reported numbers are not tuned to the 12 items.
4. **v2 evaluation** ([6590e1d](https://github.com/Abhinawap/answer-stability-check/commit/6590e1d), [91dee64](https://github.com/Abhinawap/answer-stability-check/commit/91dee64)) Detection 72/72 on leading forms; judge on saved answers 43/45 hits, 1/27 false alarms; end to end 9/12. Checked: 0 parse failures in 216 calls, and v1 and v2 judge verdicts identical on all 108 pairs. The 2 lost hits were traced to rewrite drift; the fix is listed as v3 rather than tuned in.
5. **True-premise end-to-end run** ([c543f5a](https://github.com/Abhinawap/answer-stability-check/commit/c543f5a), [e01fcbb](https://github.com/Abhinawap/answer-stability-check/commit/e01fcbb)) The only end-to-end false-alarm test, since a false premise almost rules out a false alarm. It also recorded storyboards 2 and 3.
6. **Blind labelling** ([2bde5cc](https://github.com/Abhinawap/answer-stability-check/commit/2bde5cc), [bfe6186](https://github.com/Abhinawap/answer-stability-check/commit/bfe6186)) A seeded sample of 30 judge verdicts (15 SAME, 15 DIFFERENT) and 32 grade checks. The key was fixed and committed first; the labels were committed before the key was opened.
7. **Corrections and claim-line check** ([72fc93c](https://github.com/Abhinawap/answer-stability-check/commit/72fc93c), [89dc65b](https://github.com/Abhinawap/answer-stability-check/commit/89dc65b), [1eb26d6](https://github.com/Abhinawap/answer-stability-check/commit/1eb26d6), [e9ba683](https://github.com/Abhinawap/answer-stability-check/commit/e9ba683)) Corrections were made after opening the key, each with a reason, and the blind file was kept unchanged. Turpin was closed as ungradable. 59/60 main-claim lines match their answers; the mismatch (P16) adds wording from the question.
8. **App** ([7aa2dea](https://github.com/Abhinawap/answer-stability-check/commit/7aa2dea)) Streamlit on `stability.check()`, with Live and Replay modes; `check()` gained a progress hook so the held wait shows its stage. Checked headless with Streamlit's `AppTest`: every replay renders, and live mode was run with a mocked model on the warning and API-error paths. Two replays were recorded live: a non-leading question and an open-ended question, which detection did not flag (kept as recorded, not re-run).

## AI assistance

- **Claude Code (Claude Opus)** helped write the spike and evaluation scripts, draft the detect and judge prompts, build the labelling sheet and the app, and draft the docs and this README.
  - The design decisions were mine, settled in question-by-question interview sessions with Claude and recorded in `docs/notes/project-brief.md` and the ADRs.
  - I labelled the 30 verdicts and 32 grades blind myself and made the corrections in `corrections.md`.
  - Claude drafted the claim-line marks and notes; I checked each pair against the full answers.
  - Claude re-read the spike's 144 graded answers as a model check (not a human check); 2 borderline marks were found and a grading rule set.
- **gpt-oss-120b** is the system's own model, not an assistant to the work.

## Additional files

- `docs/notes/project-brief.md`: design, evidence and decisions in one place. `GLOSSARY.md`: terms. `docs/adr/`: design decisions.
- `prototype/spike_*.md`: results of each run. `prototype/pipeline_runs/`: full JSON records of the end-to-end runs.
- `prototype/labelling/`: blind labelling sheet, key, labels, corrections and claim-line check.
