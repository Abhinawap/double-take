# The instability warning replaces the answer, and the answer is held until the comparison finishes

When a leading question produces a disagreement, the student sees the instability warning with both answers side by side, never one answer with a banner (anchoring, automation bias, inattentional blindness). As a result, no answer is streamed. Every answer waits for detection. An answer to a leading question also waits until the neutral version has been answered and judged, even when the answers turn out to agree. Otherwise an answer swapped out after streaming would already have anchored.

## Consequences
- The first answer runs **in parallel** with detection, since both paths need it. The wait is then detection, followed for leading questions by the neutral answer and the judge: three steps rather than four. The worker thread only returns text, because Streamlit calls must stay on the main thread, and the answer stays hidden until detection returns, even if it finishes first.
- Answers to non-leading questions appear as soon as detection returns.
- A progress line covers the wait (feedback timing: acknowledge anything over about 1 s, show progress near 10 s; Miller 1968, Nielsen 1993).
- If detection or the judge fails to parse after one retry, the answer is shown with *"I couldn't compare this with a second answer this time."* **above** it, for the same anchoring reason.
