"""
Run directly: `python3 -m scrapers.nh.tests.test_action_dates`
"""
from ..bills import action_date, journal_dates


def test_action_dates():
    def date(action, timestamp):
        return action_date(action, timestamp).strftime("%Y-%m-%d")

    assert (
        date(
            "Ought to Pass: MA, VV; OT3rdg; 03/26/2026;  SJ 7",
            "3/23/2026 12:00:00 AM",
        )
        == "2026-03-26"
    )
    assert (
        date(
            "House Non-Concurs with Senate Amendment 2026-1987s and Requests CofC "
            "(Rep. Roy): MA VV 05/14/2026  HJ 13  P. 147",
            "5/18/2026 12:00:00 AM",
        )
        == "2026-05-14"
    )
    assert (
        date("Died on Table, Session ended 08/19/2026  HJ 16", "8/20/2026 12:00:00 AM")
        == "2026-08-19"
    )
    # no journal citation, or an "in recess" entry: keep the posting date
    assert (
        date(
            "Committee Report: Ought to Pass with Amendment # 2026-1917s, "
            "05/14/2026, Vote 3-2;  SC 18A",
            "5/12/2026 12:00:00 AM",
        )
        == "2026-05-12"
    )
    assert (
        date(
            "Sen. Gannon Accedes to House Request for Committee of Conference, "
            "MA, VV; (In recess 05/14/2026);  SJ 13",
            "5/20/2026 12:00:00 AM",
        )
        == "2026-05-20"
    )
    assert (
        date(
            "Enrolled (in recess of) 04/09/2026  HJ 10  P. 28", "4/15/2026 12:00:00 AM"
        )
        == "2026-04-15"
    )
    assert (
        date(
            "Reconsider HB1491 (Rep. N. Germana): MF VV 09/19/2026  HJ 16  P. 48",
            "8/19/2026 2:27:49 PM",
        )
        == "2026-08-19"
    )


def test_floor_votes_take_journal_date():
    hj8 = "Ought to Pass: MA VV 03/12/2026  HJ 8  P. 3"
    typo = "Inexpedient to Legislate: MF RC 165-176 03/13/2026  HJ 8  P. 90"
    consent = "Removed from Consent (Reps. A, B) 03/10/2026  HJ 8  P. 1"
    carry_over = "Ought to Pass: MA VV 03/13/2025  HJ 8  P. 12"
    journals = journal_dates([hj8, hj8, typo, consent, carry_over])

    def date(action):
        return action_date(action, "3/16/2026 12:00:00 AM", journals).strftime(
            "%Y-%m-%d"
        )

    assert date(typo) == "2026-03-12"
    assert date(consent) == "2026-03-10"
    assert date(carry_over) == "2025-03-13"


if __name__ == "__main__":
    test_floor_votes_take_journal_date()
    test_action_dates()
