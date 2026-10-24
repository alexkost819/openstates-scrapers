"""
Run directly: `python3 -m scrapers.nh.tests.test_failure_actions`
"""
from ..actions import Categorizer


def classify(text):
    return sorted(Categorizer().categorize(text)["classification"])


def test_failure_actions():
    assert classify("Died on Table, Session ended 08/19/2026  HJ 16") == ["failure"]
    assert classify(
        "Indefinitely Postpone (Rep. Sweeney): MA RC 188-149 03/12/2026  HJ 7  P. 92"
    ) == ["failure"]
    assert classify("Indefinitely Postpone: MA, VV; 03/05/2026;  SJ 5") == ["failure"]
    assert (
        classify(
            "Indefinitely Postpone (Rep. M. Pearson): MF RC 133-205 01/07/2026  HJ 1  P. 170"
        )
        == []
    )
    assert classify("Sen. Gray Moved to Indefinitely Postpone; 03/05/2026;  SJ 5") == []
    assert classify(
        "Lay HB609 on Table (Rep. Wilhelm): MA RC 182-160 06/04/2026  HJ 15  P. 29"
    ) == ["deferral"]
    assert (
        classify(
            "Lay HB1361 on Table (Rep. Hill): MF DV 160-178 03/12/2026  HJ 8  P. 33"
        )
        == []
    )
    assert classify("Sen. Gray Moved Laid on Table, MA, VV; 03/26/2026;  SJ 7") == [
        "deferral"
    ]
    assert classify("Inexpedient to Legislate: MA VV 02/19/2026  HJ 5  P. 3") == [
        "failure"
    ]
    assert classify(
        "Inexpedient to Legislate, Senate Rule 3-23, 10/31/2025;  SJ 1"
    ) == ["failure"]
    assert classify("Inexpedient to Legislate: MF RC 165-176 03/12/2026  HJ 8") == []
    assert classify("Inexpedient to Legislate, MF, VV; 03/26/2026;  SJ 7") == []


if __name__ == "__main__":
    test_failure_actions()
