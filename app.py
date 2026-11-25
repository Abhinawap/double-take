"""Answer-stability check: Streamlit front end. Display only; all logic is in stability.py.

Run: streamlit run app.py   (Live mode needs LLM_API_KEY in the environment; without it the app replays saved runs.)
"""
import json, os, pathlib, re
import streamlit as st
import stability

REPLAYS = pathlib.Path(__file__).parent / "replays"
SCOPE = "When a factual question suggests its own answer, I compare two answers before showing one."
HEADLINE = "I gave two different answers to this, so don't take either as confirmed. Check your notes or slides."
FAILED = "I couldn't compare this with a second answer this time."


def first_paragraph(text):
    """Opening paragraph, keeping a leading heading with the paragraph under it."""
    out = []
    for p in (p for p in text.split("\n\n") if p.strip()):
        out.append(p)
        if not p.lstrip().startswith(("#", "**")) or len(p.strip().splitlines()) > 1:
            break
    # headings shown as bold, so the two columns line up whatever format each answer used
    return "\n\n".join(re.sub(r"^#+\s*(.+?)\s*$", r"**\1**", p, flags=re.M) for p in out)


def show(rec):
    outcome = rec["outcome"]
    if outcome == "warn":
        st.warning(HEADLINE, icon="⚠️")
        for col, label, q, claim, ans in zip(
            st.columns(2), ("You asked", "Asked neutrally"), (rec["question"], rec["neutral"]),
            (rec["claim_asked"], rec["claim_neutral"]), (rec["answer"], rec["neutral_answer"])):
            with col:
                st.caption(f"{label}: {q}")
                st.markdown(f"**{claim}**")
                st.markdown(first_paragraph(ans))
                with st.expander("Full answer"):
                    st.markdown(ans)
        st.info("Neither answer is marked as right: both can be wrong. Your notes or the slides are the check.")
        return
    if outcome == "check_failed":
        st.warning(FAILED)
    st.markdown(rec["answer"])  # 'answer' (not leading) and 'agree' look the same: no badge


st.set_page_config(page_title="Answer-stability check", page_icon="⚖️")
st.title("Answer-stability check")

live_ok = bool(os.environ.get("LLM_API_KEY"))
mode = st.radio("Mode", ["Live", "Replay"], horizontal=True, label_visibility="collapsed") if live_ok else "Replay"
if not live_ok:
    st.info("Replay mode: no LLM_API_KEY is set, so these are saved runs, not live calls. See the README to add a key.")

if mode == "Replay":
    files = sorted(REPLAYS.glob("*.json"))
    name = st.selectbox("Saved run", [f.stem for f in files])
    rec = json.loads((REPLAYS / f"{name}.json").read_text())
    st.text_input("Question", rec["question"], disabled=True)
    st.caption(SCOPE)
    st.caption(f"Saved run · {rec['model']} · temperature {rec['temperature']} · top_p {rec['top_p']} · "
               f"prompts {rec['prompt_version']} · {rec['date']}")
    show(rec)
    with st.expander("Behind the check (not shown to a student)"):
        st.write({k: rec.get(k) for k in ("leading", "neutral", "claim_asked", "claim_neutral", "outcome", "truth") if k in rec})
else:
    q = st.text_input("Question", placeholder="Ask a question about the course…")
    st.caption(SCOPE)
    retry = st.session_state.pop("retry", False)
    if (st.button("Ask", type="primary") or retry) and q.strip():
        slot = st.empty()  # emptied afterwards, so an agreeing answer carries no "checked" badge
        try:
            with slot.status("Checking your question…") as status:
                rec = stability.check(q.strip(), lambda label: status.update(label=label))
            st.session_state["live"] = rec
        except Exception as e:  # API or network failure: say so, show nothing, offer a retry
            st.session_state.pop("live", None)
            st.error(f"The model call failed, so nothing is shown. ({type(e).__name__}: {e})")
            st.button("Try again", on_click=lambda: st.session_state.update(retry=True))
        slot.empty()
    if (rec := st.session_state.get("live")) and rec["question"] == q.strip():
        show(rec)
