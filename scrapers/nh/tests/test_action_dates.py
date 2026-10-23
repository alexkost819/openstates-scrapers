"""
Run directly: `python3 -m scrapers.nh.tests.test_action_dates`
"""
from ..bills import action_date


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


if __name__ == "__main__":
    test_action_dates()
