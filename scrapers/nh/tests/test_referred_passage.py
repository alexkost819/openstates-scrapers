"""
Run directly: `python3 -m scrapers.nh.tests.test_referred_passage`
"""
from openstates.scrape import Bill

from ..bills import unmark_referred_passage


def test_referred_passage():
    bill = Bill("HB 54", "2026", "t", chamber="lower")
    first = bill.add_action(
        "Ought to Pass: MA RC 358-14 03/06/2025  HJ 7  P. 40",
        "2025-03-06",
        chamber="lower",
        classification=["passage"],
    )
    bill.add_action(
        "Referred to Finance 03/06/2025  HJ 7  P. 42", "2025-03-06", chamber="lower"
    )
    second = bill.add_action(
        "Ought to Pass: MA VV 04/10/2025  HJ 12",
        "2025-04-10",
        chamber="lower",
        classification=["passage"],
    )
    senate = bill.add_action(
        "Ought to Pass: MA, VV; OT3rdg; 05/14/2026;  SJ 12",
        "2026-05-14",
        chamber="upper",
        classification=["passage"],
    )
    bill.add_action(
        "Referred to Finance 05/14/2026  HJ 13", "2026-05-14", chamber="lower"
    )
    unmark_referred_passage(bill.actions)
    assert first["classification"] == []
    assert second["classification"] == ["passage"]
    assert senate["classification"] == ["passage"]


if __name__ == "__main__":
    test_referred_passage()
