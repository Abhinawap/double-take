"""Checks for the parts of stability.py that must never fail open. Run: python3 test_stability.py"""
import stability as s


def raises(f, *a):
    try:
        f(*a)
    except (ValueError, s.CheckFailed):
        return True
    return False


# parsing: valid shapes pass, including a fenced reply
assert s.parse_detect('{"leading": false, "neutral": ""}') == (False, "")
assert s.parse_detect('```json\n{"leading": true, "neutral": "How many?"}\n```') == (True, "How many?")
assert s.parse_judge('{"claim_a": "7", "claim_b": "5", "verdict": "DIFFERENT"}') == (True, "7", "5")
# anything unusable is a failure, never "not leading" or SAME
for bad in ["garbage", "", '{"leading": "yes", "neutral": "x"}', '{"leading": true, "neutral": ""}', "[1, 2]"]:
    assert raises(s.parse_detect, bad), bad
for bad in ["SAME", '{"verdict": "same", "claim_a": "a", "claim_b": "b"}', '{"verdict": "SAME", "claim_a": "", "claim_b": "b"}']:
    assert raises(s.parse_judge, bad), bad

# one retry, then CheckFailed
replies = iter(["garbage", '{"leading": true, "neutral": "How many stages?"}'])
s.ask = lambda p: next(replies)
assert s.detect("Why five stages?") == (True, "How many stages?")
replies = iter(["garbage", "still garbage", "never reached"])
assert raises(s.detect, "q")
assert next(replies) == "never reached"  # exactly two calls

# check(): a judge failure yields check_failed with the answer kept, not a silent pass
script = {"detect": '{"leading": true, "neutral": "How many stages?"}', "judge": "nope"}
s.ask = lambda p: script["detect"] if "Is the question leading" in p else script["judge"] if "main claim" in p else "Seven."
r = s.check("Why does it have five stages?")
assert r["outcome"] == "check_failed" and r["answer"] == "Seven." and "judge" in r["failure"], r
script["judge"] = '{"claim_a": "five", "claim_b": "seven", "verdict": "DIFFERENT"}'
r = s.check("Why does it have five stages?")
assert r["outcome"] == "warn" and r["claim_neutral"] == "seven" and r["prompt_version"] == "v2", r
script["detect"] = '{"leading": false, "neutral": ""}'
assert s.check("How many stages?")["outcome"] == "answer"
print("ok")
