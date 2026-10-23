"""
Run directly: `python3 -m scrapers.nh.tests.test_ought_to_pass_actions`
"""
from ..actions import Categorizer


def classify(text):
    return sorted(Categorizer().categorize(text)["classification"])


def test_ought_to_pass_actions():
    # committee reports
    assert classify(
        "Committee Report: Ought to Pass with Amendment # 2026-1917s, 05/14/2026, Vote 3-2;  SC 18A"
    ) == ["committee-passage-favorable"]
    assert classify(
        "Majority Committee Report: Ought to Pass  10/22/2025 (Vote 9-7; RC)  HC 51  P. 21"
    ) == ["committee-passage-favorable"]
    assert classify("Minority Committee Report: Ought to Pass") == []
    # floor votes
    assert classify(
        "Ought to Pass with Amendment 2026-0019h: MA RC 193-151 01/07/2026  HJ 1  P. 92"
    ) == ["passage"]
    assert classify(
        "Ought to Pass with Amendment # 2026-1987s, MA, VV; OT3rdg; 05/14/2026;  SJ 12"
    ) == ["passage"]
    assert classify(
        "Ought to Pass with Amendments #2026-1219s, RC 23Y-1N, by necessary 3/5, MA; OT3rdg; 03/26/2026;  SJ 7"
    ) == ["passage"]
    assert classify("Ought to Pass: MF RC 155-192 02/19/2026  HJ 5  P. 80") == []
    assert classify("Ought to Pass: MA, VV; 03/12/2026;  SJ 6") == []
    assert classify(
        "Ought to Pass: MA, VV; Refer to Finance Rule 4-5; 05/07/2026;  SJ 11"
    ) == ["referral-committee"]
    assert classify("Sen. Birdsell Moved Ought to Pass; 05/07/2026;  SJ 11") == []
    assert classify("Pending Motion OT3rdg; 03/12/2026;  SJ 6") == []


if __name__ == "__main__":
    test_ought_to_pass_actions()
