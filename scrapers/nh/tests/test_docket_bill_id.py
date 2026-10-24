"""
Carry-over bills (LSR from the prior year) aren't in LsrsOnly.txt, so their
billinfo.aspx id has to come from the legacy docket page.
testdata/bill_docket_2026_0889.html is
https://gc.nh.gov/bill_status/legacy/bs2016/bill_docket.aspx?lsr=0889&sy=2026&sortoption=&txtsessionyear=2026
(HB 609, LSR 25-0889, billinfo.aspx?id=899).
Run directly: `python3 -m scrapers.nh.tests.test_docket_bill_id`
"""
import os
import tempfile
from types import SimpleNamespace

from openstates.scrape import Bill

from ..bills import NHBillScraper

HERE = os.path.dirname(__file__)


def test_docket_bill_id():
    with open(os.path.join(HERE, "testdata", "bill_docket_2026_0889.html"), "rb") as f:
        content = f.read()
    with tempfile.TemporaryDirectory() as tmp:
        scraper = NHBillScraper({"name": "New Hampshire"}, tmp)
        scraper.get = lambda *args, **kwargs: SimpleNamespace(content=content)
        bill = Bill("HB 609", legislative_session="2026", chamber="lower", title="t")
        assert scraper.scrape_versions_from_docket(bill, "0889", "2026") == "899"
        notes = [v["note"] for v in bill.versions]
        assert notes[:2] == ["Introduced", "Amendment: #2026-0019h"], notes


if __name__ == "__main__":
    test_docket_bill_id()
