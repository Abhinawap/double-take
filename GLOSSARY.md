# Answer-stability check

Vocabulary for IIS Assignment 2: a study-assistant feature that warns students when an AI answer is unstable. Reliance and explanation terms come from the A1 glossary (appropriate reliance, overreliance, faithfulness).

## Language

### The check

**Stability check**:
The mechanism of asking a second version of the student's question, comparing the two answers and warning only when they disagree.
_Avoid_: Double-check, consistency check, verification

**Trigger**:
A condition that starts the stability check. Leading wording is the built trigger.
_Avoid_: Detector, mode

**Leading question**:
A question that presupposes a fact, suggests an answer, or asks the assistant to confirm a claim.
_Avoid_: Loaded question, biased question

**Neutral version**:
A rewrite of a leading question that asks for the same information without stating or hinting at any answer.
_Avoid_: Rephrasing, paraphrase, neutralised question

**Rewrite drift**:
A neutral version that asks for different information from what the leading question takes for granted, so the comparison never tests the premise.
_Avoid_: Bad rewrite, scope creep

**Main claim**:
The one-line answer an answer gives to the question, stripped of explanation.
_Avoid_: Summary, gist, short answer

**Judge**:
The model call that extracts the main claims of two answers and decides whether there is a disagreement.
_Avoid_: Comparator, evaluator, grader (a grader checks against the truth)

**Disagreement**:
The judge's verdict that two answers give different main claims, whether they answer two versions of a question or the same question asked twice.
_Avoid_: Flip, inconsistency, mismatch

**Instability warning**:
What the student sees instead of a single answer when there is a disagreement.
_Avoid_: Alert, flag, cue, uncertainty message

### The signal

**Unstable answer**:
An answer that changes with the wording of the question or between repeated asks. Its two causes are weak knowledge and sycophancy.
_Avoid_: Wrong answer, hallucination

**Weak-knowledge item**:
A fact the model does not reliably know, shown by a wrong neutral answer or by two neutral answers that disagree.
_Avoid_: Hard question, niche fact, wrong premise

**Sycophancy**:
The model returning the student's premise as fact (W03 L08), including for a fact it states correctly when asked neutrally.
_Avoid_: Agreeableness, people-pleasing

### Evidence

**Hit**:
An instability warning where at least one of the two answers is wrong.
_Avoid_: True positive, catch

**False alarm**:
An instability warning where both answers are right.
_Avoid_: False positive, cry-wolf warning

**Miss**:
No instability warning although the answer shown is wrong.
_Avoid_: False negative, silent failure

**Grader**:
In the spike only: the model call that marks one answer right or wrong against a known truth.
_Avoid_: Judge (which compares two answers without the truth)

**Flip**:
In the spike only: a change in the grader's right/wrong mark between the neutral answer and a leading answer.
_Avoid_: Disagreement (which compares answers, not marks)

**Noise baseline**:
How often two answers to the identical neutral question disagree.
_Avoid_: Variance, randomness
