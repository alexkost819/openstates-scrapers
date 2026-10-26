"""
testdata/bill_status_2026_0720.html is
https://gc.nh.gov/bill_status/legacy/bs2016/bill_status.aspx?lsr=720&sy=2026&txtsessionyear=2026&txtbillnumber=hb728&sortoption=billnumber
(HB 728, whose billinfo.aspx page lists no sponsors).
Run directly: `python3 -m scrapers.nh.tests.test_legacy_sponsors`
"""
import os
import tempfile
from types import SimpleNamespace

from openstates.scrape import Bill

from ..bills import NHBillScraper

HERE = os.path.dirname(__file__)


def test_legacy_sponsors():
    with open(os.path.join(HERE, "testdata", "bill_status_2026_0720.html"), "rb") as f:
        content = f.read()
    with tempfile.TemporaryDirectory() as tmp:
        scraper = NHBillScraper({"name": "New Hampshire"}, tmp)
        scraper.get = lambda *args, **kwargs: SimpleNamespace(content=content)
        bill = Bill("HB 728", legislative_session="2026", chamber="lower", title="t")
        scraper.scrape_sponsors_from_legacy_page(bill, "0720", "2026")
        assert [(s["name"], s["primary"]) for s in bill.sponsorships] == [
            ("Fred Doucette", True)
        ]


if __name__ == "__main__":
    test_legacy_sponsors()
