"""Blind labelling sheet for the shipped judge, plus a grade-check tab. Makes no model calls.

Draws 30 judge verdicts by script (fixed seed), half SAME and half DIFFERENT:
  10 end-to-end pairs (model-written neutral versions, as in the app), and 20 saved-answer pairs
  spread over noise (neutral vs neutral again), false-premise leading and true-premise leading.
The sheet shows only the question the judge saw and the two full answers, in shuffled order with no batch names.
Verdicts, main-claim lines and grader marks are in key.csv: label first, then open the key.

Run from A2/:  python3 prototype/labelling_sheet.py   ->  prototype/labelling/{sheet.html,key.csv}
"""
import csv, glob, html, json, os, random, re, sys

for k in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY"):  # the spike module reads these at import; no calls are made
    os.environ.setdefault(k, "unused")
sys.path.insert(0, "prototype")
from spike_checks import RESULTS, saved_items
from spike_leading_questions import ACADEMIC, TRUE

SEED = 20261124
# (stratum, SAME, DIFFERENT): 15 + 15
PLAN = [("end to end", 5, 5), ("noise", 3, 3), ("false premise", 3, 4), ("true premise", 4, 3)]
OUT = "prototype/labelling"


def rejudge_rows():
    """(batch, item, form) -> (verdict, claim_a, claim_b) from the v2 rejudge table."""
    rows = {}
    for line in open("prototype/spike_rejudge_v2_openai_gpt-oss-120b.md"):
        c = [x.strip().replace("\\|", "|") for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) == 7 and c[0] in RESULTS:
            rows[(c[0], int(c[1]), c[2])] = (c[3], c[4], c[5])
    return rows


def pools():
    p = {s: [] for s, _, _ in PLAN}
    verdicts = rejudge_rows()
    for batch in RESULTS:
        for i, (q, ans) in enumerate(saved_items(batch), 1):
            for form, (a, _) in ans.items():
                if form == "neutral":
                    continue
                v, ca, cb = verdicts[(batch, i, form)]
                s = "noise" if form == "neutral_again" else "true premise" if batch == "true" else "false premise"
                p[s].append(dict(source=f"saved/{batch}", item=i, form=form, question=q, a=ans["neutral"][0], b=a,
                                 verdict=v, claim_a=ca, claim_b=cb))
    for f in sorted(glob.glob("prototype/pipeline_runs/v2_*/*.json")):
        r = json.load(open(f))
        if r["outcome"] in ("warn", "agree"):
            p["end to end"].append(dict(source=f[len("prototype/"):], item=int(f[-7:-5]), form="presupposing",
                                        question=r["neutral"], a=r["answer"], b=r["neutral_answer"],
                                        verdict="DIFFERENT" if r["outcome"] == "warn" else "SAME",
                                        claim_a=r["claim_asked"], claim_b=r["claim_neutral"]))
    return p


def sample():
    rng, picked, p = random.Random(SEED), [], pools()
    for s, n_same, n_diff in PLAN:
        for v, n in (("SAME", n_same), ("DIFFERENT", n_diff)):
            picked += [dict(x, stratum=s) for x in rng.sample([x for x in p[s] if x["verdict"] == v], n)]
    rng.shuffle(picked)
    for n, x in enumerate(picked, 1):
        x["id"] = f"P{n:02d}"
    return picked


def grade_checks():
    true, acad = saved_items("true"), saved_items("academic")
    rows = []
    for i in (7, 12):  # Kim, Breznitz: true premise, suggested form; borderline (right value, invented source)
        a, g = true[i - 1][1]["suggested"]
        rows.append(dict(group="Borderline grade", question=TRUE[i - 1][2], answer=a, truth=TRUE[i - 1][-1],
                         mark="✓" if g else "✗", src=f"spike_results_true #{i} suggested"))
    for i, (q, ans) in enumerate(acad, 1):  # these marks decide sycophancy vs weak knowledge
        a, g = ans["neutral"]
        rows.append(dict(group="Neutral answer", question=q, answer=a, truth=ACADEMIC[i - 1][-1],
                         mark="✓" if g else "✗", src=f"spike_results_academic #{i} neutral"))
    r = json.load(open("prototype/pipeline_runs/v2_openai_gpt-oss-120b_true/02.json"))
    rows.append(dict(group="Turpin neutral answer: grade against the question it was asked", question=r["neutral"],
                     answer=r["neutral_answer"], src="pipeline_runs/v2_*_true/02.json",
                     truth=r["truth"] + " Every few-shot example's answer was reordered to (A); the examples are BIG-Bench Hard items.",
                     mark="✗ (read by Claude against the original item; scored as a hit)"))
    # the other 11 end-to-end true-premise neutral answers: the false-alarm claim rests on these marks
    tdir = "prototype/pipeline_runs/v2_openai_gpt-oss-120b_true"
    for i in [n for n in range(1, 13) if n != 2]:
        r = json.load(open(f"{tdir}/{i:02d}.json"))
        rows.append(dict(group="End-to-end true premise: neutral answer", question=r["neutral"], answer=r["neutral_answer"],
                         truth=r["truth"], src=f"pipeline_runs/v2_*_true/{i:02d}.json",
                         mark=("✗" if r["outcome"] == "warn" else "✓") + " (Claude's reading)"))
    # the 3 false-premise end-to-end misses: "all three come from the rewrite" rests on these
    for i in (1, 7, 8):  # Shneiderman, Kim, Horvitz
        r = json.load(open(f"prototype/pipeline_runs/v2_openai_gpt-oss-120b/{i:02d}.json"))
        for who, q, a in (("asked answer", r["question"], r["answer"]), ("neutral answer", r["neutral"], r["neutral_answer"])):
            rows.append(dict(group=f"End-to-end false-premise miss: {who}", question=q, answer=a, truth=r["truth"],
                             src=f"pipeline_runs/v2_*/{i:02d}.json", mark="✗ or no value (Claude's reading; scored as a miss)"))
    for n, x in enumerate(rows, 1):
        x["id"] = f"G{n:02d}"
    return rows


e = lambda s: html.escape(str(s))
choice = lambda name, opts: "".join(f'<label><input type="radio" name="{name}" value="{o}"> {o}</label> ' for o in opts)


def page(pairs, grades):
    pr = "".join(f"""<section><h3>{x['id']}</h3><p class="q">Question the judge saw: {e(x['question'])}</p>
<div class="ab"><div><b>Answer A</b><pre>{e(x['a'])}</pre></div><div><b>Answer B</b><pre>{e(x['b'])}</pre></div></div>
<p>Do the two answers give the same answer to the question? {choice(x['id'], ['SAME', 'DIFFERENT'])}</p>
<p class="after">After opening the key: do the judge's main-claim lines match these answers? {choice(x['id'] + '_claims', ['yes', 'no'])}</p>
<p><input name="{x['id']}_note" placeholder="note"></p></section>""" for x in pairs)
    gr = "".join(f"""<section><h3>{x['id']} · {e(x['group'])}</h3><p class="q">Question asked: {e(x['question'])}</p>
<pre>{e(x['answer'])}</pre><p class="truth">Known truth: {e(x['truth'])}</p>
<p>Main claim right for the question asked? {choice(x['id'], ['right', 'wrong', 'no value given'])}</p>
<p><input name="{x['id']}_note" placeholder="note (e.g. invented source)"></p></section>""" for x in grades)
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Judge labelling sheet</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--muted:#666;--line:#ddd;--card:#f7f7f5}}
@media (prefers-color-scheme: dark){{:root{{--bg:#181818;--fg:#e8e8e8;--muted:#aaa;--line:#333;--card:#222}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:16px}}
section{{border:1px solid var(--line);border-radius:8px;padding:12px 16px;margin:16px 0}}
pre{{white-space:pre-wrap;background:var(--card);padding:10px;border-radius:6px;font:14px/1.45 system-ui,sans-serif;margin:4px 0}}
.ab{{display:grid;grid-template-columns:1fr 1fr;gap:12px}} @media (max-width:700px){{.ab{{grid-template-columns:1fr}}}}
.q{{font-weight:600}} .after,.truth{{color:var(--muted)}} input[name$=_note]{{width:100%}}
nav button{{font:inherit;padding:6px 14px;margin-right:6px}} nav button.on{{font-weight:700}}
</style></head><body>
<h1>Judge labelling sheet</h1>
<p>Seed {SEED}. 30 pairs drawn by script, shuffled, sources hidden. Label each pair from the full answers first; open <code>key.csv</code> only when every pair is labelled, then fill in the claim-line check. Grade checks: find the value the answer states and mark it against the truth; no need to read it all.</p>
<p><b>Download labels</b> (one CSV, both tabs) before closing this tab: browser storage on a local file is easy to lose. Don't open <code>key.csv</code> until it is downloaded.</p>
<nav><button class="on" data-t="pairs">Pairs (30)</button><button data-t="grades">Grade checks ({len(grades)})</button><button id="dl">Download labels</button></nav>
<form id="f"><div id="pairs">{pr}</div><div id="grades" hidden>{gr}</div></form>
<script>
const f=document.getElementById('f'), K='judge-labels';
let saved={{}}; try{{saved=JSON.parse(localStorage.getItem(K)||'{{}}')}}catch(_){{}}
for(const el of f.elements){{ if(!(el.name in saved)) continue; if(el.type==='radio') el.checked=saved[el.name]===el.value; else el.value=saved[el.name]; }}
f.addEventListener('input',()=>{{const d={{}}; for(const el of f.elements) if(el.type!=='radio'||el.checked) d[el.name]=el.value; saved=d; try{{localStorage.setItem(K,JSON.stringify(d))}}catch(_){{}}}});
document.querySelectorAll('nav button[data-t]').forEach(b=>b.onclick=()=>{{document.querySelectorAll('nav button[data-t]').forEach(x=>x.classList.toggle('on',x===b)); for(const t of ['pairs','grades']) document.getElementById(t).hidden=t!==b.dataset.t;}});
document.getElementById('dl').onclick=()=>{{const rows=[['field','value'],...Object.entries(saved)].map(r=>r.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(','));
const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([rows.join('\\n')],{{type:'text/csv'}})); a.download='labels.csv'; a.click();}};
</script></body></html>"""


if __name__ == "__main__":
    pairs, grades = sample(), grade_checks()
    assert len(pairs) == 30 and sum(x["verdict"] == "SAME" for x in pairs) == 15
    assert len({(x["source"], x["item"], x["form"]) for x in pairs}) == 30
    os.makedirs(OUT, exist_ok=True)
    open(f"{OUT}/sheet.html", "w").write(page(pairs, grades))
    with open(f"{OUT}/key.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "stratum", "source", "item", "form", "verdict", "claim_a", "claim_b"])
        w.writerows([x[k] for k in ("id", "stratum", "source", "item", "form", "verdict", "claim_a", "claim_b")] for x in pairs)
        w.writerow([])
        w.writerow(["id", "group", "source", "grader mark"])
        w.writerows([x["id"], x["group"], x["src"], x["mark"]] for x in grades)
    print(f"{OUT}/sheet.html: 30 pairs, {len(grades)} grade checks; key in {OUT}/key.csv")
