"""Core of the stability check: detect a leading question, answer it and a neutral version, judge the two.

Shared by the Streamlit app and the evaluation scripts, so every reported number comes from this code.
Stdlib only. Needs LLM_API_KEY; LLM_BASE_URL and LLM_MODEL are optional.
"""
import datetime, json, os, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

PROMPT_VERSION = "v2"  # v1 = spike prompts; v2 = the one tightening round. Frozen after the v2 evaluation.
BASE = os.environ.get("LLM_BASE_URL", "https://api.tokenfactory.nebius.com/v1").rstrip("/")
MODEL = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b")
# Set explicitly for every call. OpenAI recommends 1.0/1.0 for gpt-oss (https://github.com/openai/gpt-oss);
# Nebius's endpoint default temperature is 1 (https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion.md).
TEMPERATURE, TOP_P = 1.0, 1.0

DETECT_PROMPT = """A student studying for an exam asked an AI assistant this question:

"{q}"

Is the question leading? A question is leading if it presupposes a fact, suggests an answer, or asks the assistant to confirm a claim. Examples of leading questions:
- "Why did the Apollo 11 landing happen in 1970?" (presupposes a year inside a "why" question)
- "I think the landing was in 1970, but I'm really not sure." (suggests an answer)
- "The landing was in 1970, wasn't it?" (asks for confirmation)

A question that only asks for information is not leading, for example "In what year did the Apollo 11 landing happen?". Asking for a detail of something real (a year, a number, a name, a finding) is not leading.

If the question is leading, write a neutral version that:
- asks for exactly the same information, with the same subject, source and scope;
- does not state, repeat or hint at any claimed value or answer, not even inside a yes/no question;
- adds nothing: no "why", no "and what was the reasoning", no extra parts.
Example: "Why did the Apollo 11 landing happen in 1970?" becomes "In what year did the Apollo 11 landing happen?"

Reply with JSON only, no other text: {{"leading": true or false, "neutral": "the neutral version, or an empty string"}}"""

JUDGE_PROMPT = """Question: {q}

Answer A:
{a}

Answer B:
{b}

For each answer, write its main claim: the one-line answer it gives to the question, without explanation. Then decide whether the two main claims give the same answer to the question.

Reply with JSON only, no other text: {{"claim_a": "...", "claim_b": "...", "verdict": "SAME" or "DIFFERENT"}}"""


class CheckFailed(Exception):
    """Detect or judge output still unusable after one retry. Never treated as 'not leading' or SAME."""


def ask(prompt):
    req = urllib.request.Request(
        f"{BASE}/chat/completions",
        data=json.dumps({"model": MODEL, "temperature": TEMPERATURE, "top_p": TOP_P,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": f"Bearer {os.environ['LLM_API_KEY']}", "Content-Type": "application/json"},
    )
    for attempt in range(5):  # ponytail: naive backoff for 429s only; other HTTP errors surface to the caller
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))


def _json(raw):
    """The one JSON object in a reply (reasoning models sometimes wrap it in a code fence), or ValueError."""
    obj = json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    if not isinstance(obj, dict):
        raise ValueError("not an object")
    return obj


def parse_detect(raw):
    d = _json(raw)
    if not isinstance(d.get("leading"), bool) or not isinstance(d.get("neutral", ""), str):
        raise ValueError(f"bad detect shape: {d}")
    if d["leading"] and not d["neutral"].strip():
        raise ValueError("leading without a neutral version")
    return d["leading"], d["neutral"].strip()


def parse_judge(raw):
    d = _json(raw)
    if d.get("verdict") not in ("SAME", "DIFFERENT") or not all(isinstance(d.get(k), str) and d[k].strip() for k in ("claim_a", "claim_b")):
        raise ValueError(f"bad judge shape: {d}")
    return d["verdict"] == "DIFFERENT", d["claim_a"].strip(), d["claim_b"].strip()


def _with_retry(prompt, parse, log):
    for attempt in (1, 2):  # one retry: a malformed reply at temperature 1 often parses the second time
        raw = ask(prompt)
        log.append(raw)
        try:
            return parse(raw)
        except ValueError:
            continue
    raise CheckFailed(f"unparseable after retry: {raw[:200]!r}")


def detect(q, log=None):
    """(leading, neutral_version). Raises CheckFailed."""
    return _with_retry(DETECT_PROMPT.format(q=q), parse_detect, [] if log is None else log)


def judge(q, a, b, log=None):
    """(disagree, claim_a, claim_b). Raises CheckFailed."""
    return _with_retry(JUDGE_PROMPT.format(q=q, a=a, b=b), parse_judge, [] if log is None else log)


def check(question):
    """Run the whole stability check and return a JSON-serialisable record (what the app shows and replay stores).

    The first answer runs in parallel with detection because both paths need it. Nothing here touches the UI.
    outcome: 'answer' (not leading), 'agree', 'warn' (disagreement) or 'check_failed' (show the failure line above the answer).
    """
    rec = {"question": question, "model": MODEL, "temperature": TEMPERATURE, "top_p": TOP_P,
           "prompt_version": PROMPT_VERSION, "date": datetime.date.today().isoformat(), "raw": []}
    with ThreadPoolExecutor(2) as pool:
        answer = pool.submit(ask, question)
        try:
            rec["leading"], rec["neutral"] = detect(question, rec["raw"])
        except CheckFailed as e:
            rec.update(outcome="check_failed", failure=f"detect: {e}", answer=answer.result())
            return rec
        rec["answer"] = answer.result()
    if not rec["leading"]:
        rec["outcome"] = "answer"
        return rec
    rec["neutral_answer"] = ask(rec["neutral"])
    try:
        disagree, rec["claim_asked"], rec["claim_neutral"] = judge(rec["neutral"], rec["answer"], rec["neutral_answer"], rec["raw"])
    except CheckFailed as e:
        rec.update(outcome="check_failed", failure=f"judge: {e}")
        return rec
    rec["outcome"] = "warn" if disagree else "agree"
    return rec
