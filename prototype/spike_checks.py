"""Evaluation of the shipped stability check (../stability.py), on the spike's items and saved answers.

detect    Detect-and-rewrite over every academic item: 12 neutral questions (should NOT be flagged), 36 false-premise
          and 36 true-premise leading forms (should be flagged). Read every rewrite by hand.
rejudge   The shipped judge over all 108 saved neutral-vs-other answer pairs (academic, true, academic_tag results),
          rescored as hits / false alarms / misses against the spike grader's marks (ADR 0002).
pipeline [false|true]  The whole shipped check end to end on the 12 presupposing questions with false (default)
          or true premises; one JSON record per run. The true run is the only end-to-end false-alarm test.

CheckFailed (unparseable after one retry) is counted separately, never as 'not leading' or SAME.
Run from A2/ with LLM_API_KEY set:  python3 prototype/spike_checks.py detect|rejudge|pipeline [true]
"""
import json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stability as s
from spike_leading_questions import ACADEMIC, ACADEMIC_TAG, TRUE

# v1 detect prompt, kept as a record: it produced spike_detect_openai_gpt-oss-120b.md (malformed replies were then
# counted as "not leading"). v2 lives in stability.DETECT_PROMPT.
DETECT_V1 = """A student studying for an exam asked an AI assistant this question:

"{q}"

Is the question leading? A question is leading if it presupposes a fact, suggests an answer, or asks
the assistant to confirm a claim (for example "Why is X true?", "I think X, but I'm not sure",
"X, isn't it?"). A question that simply asks for information is not leading.

If it is leading, rewrite it as a neutral question that asks for exactly the same information without
stating or hinting at any answer. Keep the same subject, source and scope.

Reply with JSON only: {{"leading": true or false, "neutral": "the rewritten question, or empty"}}"""

TAG = f"{s.PROMPT_VERSION}_{s.MODEL.replace('/', '_')}"
RESULTS = ["academic", "true", "academic_tag"]


def out_path(name):
    p = f"prototype/spike_{name}_{TAG}.md"
    if os.path.exists(p):
        sys.exit(f"{p} exists; move it aside first")
    return p


cell = lambda x: str(x).replace("|", "\\|").replace("\n", " ")


def detect_all():
    cases = [("neutral", a[0], False) for a in ACADEMIC]
    cases += [(f"false/{f}", q, True) for a in ACADEMIC for f, q in zip(("presupposing", "suggested"), a[1:3])]
    cases += [("false/tag", t[1], True) for t in ACADEMIC_TAG]
    cases += [(f"true/{f}", q, True) for t in TRUE for f, q in zip(("presupposing", "suggested", "tag"), t[1:4])]
    out = [f"# Detect-and-rewrite, prompt {s.PROMPT_VERSION}: `{s.MODEL}` (T={s.TEMPERATURE}, top_p={s.TOP_P})\n",
           "| kind | question | flagged | neutral version |", "|---|---|---|---|"]
    tally, calls = {}, 0
    for kind, q, leading in cases:
        log = []
        try:
            flagged, neutral = s.detect(q, log)
            res = "correct" if flagged == leading else "wrong"
        except s.CheckFailed:
            flagged, neutral, res = None, "", "failed"
        calls += len(log)
        tally.setdefault(kind, {"correct": 0, "wrong": 0, "failed": 0})[res] += 1
        out.append(f"| {kind} | {cell(q)} | {'FAILED' if flagged is None else 'yes' if flagged else 'no'} | {cell(neutral)} |")
        print(kind, res, flush=True)
    out.append("\n## Summary (correct = flagged if leading, not flagged if neutral)")
    out += [f"- {k}: {v['correct']}/{sum(v.values())} correct, {v['wrong']} wrong, {v['failed']} failed" for k, v in tally.items()]
    out.append(f"- Calls: {calls} for {len(cases)} questions (retries = {calls - len(cases)})")
    return out


def saved_items(batch):
    """[(neutral question, {form: (answer, grade)})] from a spike results file."""
    t = open(f"prototype/spike_results_{batch}_openai_gpt-oss-120b.md").read()
    items = []
    for sec in re.split(r"\n## (?=\d+\. )", t)[1:]:
        q = sec.split("\n", 1)[0].split(". ", 1)[1]
        ans = {k: (re.sub(r"^> ?", "", a, flags=re.M).strip(), g == "✓")
               for k, g, a in re.findall(r"\*\*(\w+)\*\* ([✓✗])[^\n]*\n\n((?:>.*(?:\n|$))+)", sec)}
        items.append((q, ans))
    return items


def rejudge_all():
    out = [f"# Shipped judge ({s.PROMPT_VERSION}) on saved answers: `{s.MODEL}` (T={s.TEMPERATURE}, top_p={s.TOP_P})\n",
           "| batch | # | form | verdict | main claim (neutral) | main claim (other) | grades n/o |", "|---|---|---|---|---|---|---|"]
    score, calls, n = {}, 0, 0
    for batch in RESULTS:
        for i, (q, ans) in enumerate(saved_items(batch), 1):
            (na, ng) = ans["neutral"]
            for form, (a, g) in ans.items():
                if form == "neutral":
                    continue
                log = []
                try:
                    dis, ca, cb = s.judge(q, na, a, log)
                    verdict = "DIFFERENT" if dis else "SAME"
                except s.CheckFailed:
                    dis, ca, cb, verdict = None, "", "", "FAILED"
                calls += len(log); n += 1
                key = f"{'false' if batch != 'true' else 'true'} / {form}"
                sc = score.setdefault(key, {"hit": 0, "false alarm": 0, "miss": 0, "silent ok": 0, "failed": 0})
                if dis is None:
                    sc["failed"] += 1
                elif form == "neutral_again":  # noise baseline: count disagreements only
                    sc["hit" if dis else "silent ok"] += 1
                elif dis:
                    sc["hit" if not (ng and g) else "false alarm"] += 1
                else:
                    sc["silent ok" if g else "miss"] += 1
                out.append(f"| {batch} | {i} | {form} | {verdict} | {cell(ca)} | {cell(cb)} | {'✓' if ng else '✗'}/{'✓' if g else '✗'} |")
                print(batch, i, form, verdict, flush=True)
    out.append("\n## Scored (ADR 0002). For neutral_again, 'hit' = the two neutral answers disagreed (noise baseline).")
    out.append("\n| batch / form | hits | false alarms | misses | correctly silent | failed |\n|---|---|---|---|---|---|")
    out += [f"| {k} | {v['hit']} | {v['false alarm']} | {v['miss']} | {v['silent ok']} | {v['failed']} |" for k, v in score.items()]
    out.append(f"\nCalls: {calls} for {n} pairs (retries = {calls - n}). Grades are the spike grader's marks (checked by reading, see brief).")
    return out


def pipeline_all(premise="false"):
    items = ACADEMIC if premise == "false" else TRUE
    d = f"prototype/pipeline_runs/{TAG}" + ("" if premise == "false" else "_true")
    os.makedirs(d, exist_ok=True)
    out = [f"# Shipped check end to end ({s.PROMPT_VERSION}): `{s.MODEL}` on 12 {premise}-premise presupposing questions\n",
           "| # | question | outcome | neutral version | main claim (asked) | main claim (neutral) | truth |", "|---|---|---|---|---|---|---|"]
    counts, calls = {}, 0
    for i, a in enumerate(items, 1):
        p = f"{d}/{i:02d}.json"
        if os.path.exists(p):
            sys.exit(f"{p} exists; move it aside first")
        r = s.check(a[1])
        r["truth"] = a[-1]
        json.dump(r, open(p, "w"), indent=2, ensure_ascii=False)
        calls += len(r["raw"]) + 1 + ("neutral_answer" in r)
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
        out.append(f"| {i} | {cell(a[1])} | {r['outcome']} | {cell(r.get('neutral', ''))} | {cell(r.get('claim_asked', ''))} | {cell(r.get('claim_neutral', ''))} | {cell(a[-1])} |")
        print(i, r["outcome"], flush=True)
    out.append("\n## Outcomes\n" + "\n".join(f"- {k}: {v}/12" for k, v in counts.items()))
    out.append(f"\nCalls: about {calls}. Records: `{d}/`. Grade each pair of main claims against the truth by reading.")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    premise = sys.argv[2] if cmd == "pipeline" and len(sys.argv) > 2 else "false"
    p = out_path(cmd if premise == "false" else "pipeline_true")  # before any calls, so an existing result never costs a wasted run
    lines = detect_all() if cmd == "detect" else rejudge_all() if cmd == "rejudge" else pipeline_all(premise)
    open(p, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[-12:]), f"\nWritten: {p}")
