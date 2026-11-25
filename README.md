# Double Take

A study-assistant feature that warns you when the AI's answer changes with how you word the question. IIS Assignment 2.

README prose: 1183 words, not counting code, commands and links.

![Instability warning: the model answers "five" to the leading question and "seven" to the neutral one](docs/report/screenshots/sb1-norman-warning.png)

## Project status

### Works live
- The model decides whether a question is leading, meaning it presupposes, suggests or asks to confirm an answer. If it is, the model writes a neutral version.
- The model answers both versions. The judge extracts each main claim and returns SAME or DIFFERENT.
- On a disagreement, an instability warning replaces the answer and shows both questions, both main claims and both answers.
- If detection or the judge returns output the code can't parse, the code retries once and then shows a failure line above the answer. It never counts unparseable output as "not leading" or SAME.
- The Streamlit app in `app.py` has a Live mode and a Replay mode.

### Saved runs
Replay mode loads saved `stability.check()` records from `replays/` and labels each one with the model, temperature, prompt version and date. It needs no API key. A closed panel called "Behind the check" shows markers the neutral version, the main claims and the known answer.

### Evaluation
I froze the v2 prompts before any result. All numbers come from 12 items.
- On false premises, end to end, the check warned on 9 of 12 and missed 3, with no false alarms. Rewrite drift caused two misses, because a "why" rewrite dropped the year. In the third miss (Kim), both answers were wrong in the same way.
- On true premises, end to end, the check gave 4 hits and 1 warning caused by the rewrite (Turpin), and stayed silent on 7. False alarms are 0 of 7 or 1 of 8, because Turpin's neutral question is ambiguous and I can't grade it. The check warned 5 of 12 students whose premise was right.
- I hand-labelled 30 judge verdicts blind. I agreed with the judge on 24 as labelled and on 26 after correcting 2 misclicks, which is 13 of 15 for both SAME and DIFFERENT. The main-claim lines match their answers in 59 of 60 cases.

### Planned, not built
- A v3 rewrite rule. For a "why" question, the rewrite would ask for the fact the question takes for granted. It targets the 2 rewrite-drift misses and needs fresh test items.
- An ask-twice trigger that asks the same question again and compares the answers.
- A pushback trigger that asks "Are you sure?"
- An optional static replay page, so you can view the saved runs without installing anything.

## Technology stack

- **Python 3 and the standard library.** The core in `stability.py` makes the HTTP calls, parses JSON strictly, retries once and runs the first answer in parallel with detection.
- **Streamlit.** The app calls the same `stability.check()` that the evaluation ran, so the reported numbers come from the shipped code.
- **The model.** `openai/gpt-oss-120b` runs on Nebius Token Factory, an OpenAI-compatible endpoint, with `temperature=1.0, top_p=1.0` set on every call ([gpt-oss](https://github.com/openai/gpt-oss), [Nebius API](https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion.md)). The model and endpoint are config values.
- **Still undecided.** I haven't chosen the front end for later work. The core doesn't depend on Streamlit.

## Running or inspecting the work

```bash
pip install -r requirements.txt
streamlit run app.py
```

Without a key, the app opens in Replay mode. For Live mode, supply your own Nebius Token Factory key. The repo contains no key.

```bash
export LLM_API_KEY=your-key
# optional: export LLM_BASE_URL=... LLM_MODEL=...   (any OpenAI-compatible endpoint)
streamlit run app.py
```

Run these other checks from the repo root.

```bash
python3 test_stability.py                                  # checks that parsing never fails open, no API calls
python3 record.py "question" "9 label"                    # save a live run to replays/ (needs a key)
python3 prototype/spike_checks.py pipeline [true]          # re-run the end-to-end evaluation (needs a key)
```

To inspect the results without running anything, see Additional files.

## Development record

1. **Spike on leading questions** ([169da45](https://github.com/Abhinawap/double-take/commit/169da45)). Before building, I set a barrier of at least 3 flips with noise of 1 or less. gpt-oss-120b flipped on 6 of 12 niche course facts, so I kept the idea. GLM-5.3-Flash flipped far less. That result and `docs/notes/model-choice-research.md` made gpt-oss-120b the model.
2. **Follow-up checks and design decisions** ([5a53421](https://github.com/Abhinawap/double-take/commit/5a53421)). Answer-level noise was 10 of 36 pairs, where the spike had reported 0 for grades, so I score warnings against the truth (ADR 0002). I moved the framing from unfaithful explanations to unstable answers (ADR 0001) and made the warning replace the answer (ADR 0003). I replaced the spike's lenient parser, which counted anything without "DIFFERENT" as SAME, with strict parsing.
3. **v2 prompts, frozen before evaluation** ([e587ce3](https://github.com/Abhinawap/double-take/commit/e587ce3)). I did one tightening round on the detection and judge prompts and then froze them, so I couldn't tune the reported numbers to the 12 items.
4. **v2 evaluation** ([6590e1d](https://github.com/Abhinawap/double-take/commit/6590e1d), [91dee64](https://github.com/Abhinawap/double-take/commit/91dee64)). Detection flagged all 72 leading forms. On saved answers, the judge scored 43 of 45 hits and 1 false alarm in 27. End to end, the check caught 9 of 12. I checked that the 216 calls had no parse failures and that the v1 and v2 judges gave the same verdict on all 108 pairs. I traced the 2 lost hits to rewrite drift and listed the fix as v3 instead of tuning it in.
5. **True-premise end-to-end run** ([c543f5a](https://github.com/Abhinawap/double-take/commit/c543f5a), [e01fcbb](https://github.com/Abhinawap/double-take/commit/e01fcbb)). This is the only end-to-end test of false alarms, since a false premise almost rules one out. The run also produced storyboards 2 and 3.
6. **Blind labelling** ([2bde5cc](https://github.com/Abhinawap/double-take/commit/2bde5cc), [bfe6186](https://github.com/Abhinawap/double-take/commit/bfe6186)). A script drew a seeded sample of 30 judge verdicts, 15 SAME and 15 DIFFERENT, plus 32 grade checks. I committed the key first, then committed my labels before opening it.
7. **Corrections and claim-line check** ([72fc93c](https://github.com/Abhinawap/double-take/commit/72fc93c), [89dc65b](https://github.com/Abhinawap/double-take/commit/89dc65b), [1eb26d6](https://github.com/Abhinawap/double-take/commit/1eb26d6), [e9ba683](https://github.com/Abhinawap/double-take/commit/e9ba683)). I made corrections after opening the key, gave a reason for each, and left the blind file unchanged. I closed Turpin as ungradable. 59 of 60 main-claim lines match their answers. The one mismatch (P16) copies wording from the question.
8. **App** ([7aa2dea](https://github.com/Abhinawap/double-take/commit/7aa2dea)). I built the Streamlit app on `stability.check()` with Live and Replay modes, and gave `check()` a progress hook so the screen shows each stage of the wait. Streamlit's `AppTest` rendered every replay without a browser. I also ran Live mode against a mocked model to test the warning and API-error paths. I recorded two replays live. One is a non-leading question. The other is an open-ended question that detection didn't flag, and I kept that run as recorded.

## AI assistance

- **Claude Code (Claude Opus)** helped write the spike and evaluation scripts, draft the detect and judge prompts, build the labelling sheet and the app, take the storyboard screenshots, and draft the docs and this README.
  - I made the design decisions in question-by-question interviews with Claude and recorded them in `docs/notes/project-brief.md` and the ADRs.
  - I labelled the 30 verdicts and 32 grades blind and made the corrections in `corrections.md`.
  - Claude drafted the claim-line marks and notes, and I checked each pair against the full answers.
  - Claude re-checked the 144 right/wrong marks from the spike's model grader, because the grader's replies weren't saved. It agreed with 142. The other 2 gave the right value but cited an invented source. I set the rule to grade the value and note the source, and confirmed both by hand in the blind grade check.
- **gpt-oss-120b** is the system's own model. It played no part in building the project.

## Additional files

- `docs/notes/project-brief.md` holds the design, evidence and decisions. `GLOSSARY.md` defines the terms, and `docs/adr/` records the design decisions.
- `docs/report/` holds the system diagram as HTML source and PNG, the report outline and the storyboard screenshots.
- `prototype/spike_*.md` files hold the results of each run, and `prototype/pipeline_runs/` holds the full JSON records of the end-to-end runs.
- `prototype/labelling/` holds the blind labelling sheet, key, labels, corrections and claim-line check.
