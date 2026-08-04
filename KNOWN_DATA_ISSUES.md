# Known upstream data-quality issues, by jurisdiction

Every issue below was confirmed present in the OpenStates bulk archive
itself — not an artifact of our download/parse step — by pulling the raw
record straight out of a run's `worker-outputs/openstates-json-archive/
<timestamp>/debug/debug-<jurisdiction>-<session>.jsonl` file (see the
"debug" section of the main [README](./README.md)). We normalize around
these where we safely can and preserve the source's own `counts` rather
than guessing; a "Vote count mismatch" warning means we couldn't reconcile
and kept the source's numbers. A "Duplicate vote event" warning means the
same vote event (by derived id) appeared twice — see each jurisdiction
below for what caused the collision.

This file exists to make filing upstream OpenStates issues easy: every
example is a real excerpt, trimmed but otherwise verbatim.

## Summary table

| Jurisdiction | Issue(s) |
| --- | --- |
| AZ | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| CO | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| CT | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| DE | declared counts vs. roll disagree (small) |
| FL | declared counts vs. roll disagree (small) |
| GA | declared counts vs. roll disagree (small) |
| HI | garbled placeholder name; split-off initial fragment |
| IA | declared counts vs. roll disagree (small) |
| ID | partial (exceptions-only) roll; two legislators share a bare surname |
| IL | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| KY | declared counts vs. roll disagree (small) |
| MA | declared counts vs. roll disagree (small) |
| ME | literal duplicate vote-event record |
| MI | partial (exceptions-only) roll; whole roll duplicated within one record |
| MN | literal duplicate vote-event record |
| MT | whole roll duplicated within one record |
| NC | declared counts vs. roll disagree (small) |
| NH | declared counts vs. roll disagree; literal duplicate vote-event record |
| NJ | whole roll duplicated within one record |
| NM | literal duplicate vote-event record |
| NY | whole roll duplicated within one record; duplicate/conflicting per-voter rows |
| OK | declared counts vs. roll disagree (small) |
| OR | whole roll duplicated within one record |
| PA | declared counts vs. roll disagree; literal duplicate vote-event record |
| RI | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| SC | declared counts vs. roll disagree (small) |
| SD | literal duplicate vote-event record |
| TN | partial (exceptions-only) roll |
| TX | partial (exceptions-only) roll; garbled/truncated voter names; literal duplicate vote-event record |
| VA | literal duplicate vote-event record |
| VT | declared counts vs. roll disagree (small); same vote republished under two roll-call reference numbers |
| WA | declared counts vs. roll disagree (large, 18 voters) |
| WI | declared counts vs. roll disagree (small); literal duplicate vote-event record |
| WY | split-off initial fragment |

## AZ

Declared `counts` don't reconcile with the itemized roll, off by a
handful. From `AZ/57th-1st-regular/AZ_57th-1st-regular_bills.json`, a
vote declares 2 "not voting" but the roll itemizes 3 "other"-labeled
entries with no "not voting" bucket at all — the two fields use different
category labels for what's presumably the same non-voters:

```json
{
  "counts": [
    { "option": "not voting", "value": 2 },
    { "option": "no", "value": 11 },
    { "option": "yes", "value": 16 }
  ]
  // votes: 16 yes, 11 no, 3 "other" — no "not voting" option appears in the roll at all
}
```

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## CO

Declared `counts` vs. roll disagree by 1. From
`CO/2025A/CO_2025A_bills.json`: declared 35 total, roll has 34 (`other`
0 declared vs. 1 in the roll).

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## CT

Declared `counts` vs. roll disagree by 1. From
`CT/2025/CT_2025_bills.json`: declared 106 yes, roll itemizes 107.

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## DE

Declared `counts` vs. roll disagree by 1. From
`DE/153/DE_153_bills.json`: declared 41 total, roll has 40 (`other` 2
declared vs. 1 in the roll).

## FL

Declared `counts` vs. roll disagree by 3. From
`FL/2025/FL_2025_bills.json`: declared 18 total, roll has 15 (`other` 3
declared vs. 0 in the roll — the source's own "other" voters aren't
itemized in this record at all).

## GA

Declared `counts` vs. roll disagree by 2. From
`GA/2025_26/GA_2025_26_bills.json`: declared 56 total, roll has 54
(`other` 7 declared vs. 5 in the roll).

(A GA roll also contains the voter name `"AU"` — that looked like a
split-initial fragment at first glance, matching the WY/HI pattern below,
but Georgia's House does have a member surnamed Au — ruled out as a false
positive, not a data-quality issue.)

## HI — PARTIALLY FIXED

Two distinct issues, both in voter-identity fields:

**A garbled placeholder name.** From `HI/2025/HI_2025_bills.json`, one
Senate vote event's *only* roll entry, standing in for a declared
24-yes/1-not-voting vote, is:

```json
{
  "motion_text": "Confirmed.",
  "start_date": "2025-04-25",
  "counts": [
    { "option": "not voting", "value": 1 },
    { "option": "no", "value": 0 },
    { "option": "yes", "value": 24 }
  ],
  "votes": [{ "option": "not voting", "voter_name": "Senator(s" }]
}
```

`"Senator(s"` reads like an unrendered template placeholder (likely meant
to introduce a list, e.g. "Senator(s) X, Y voting no"), not a name.

**A legislator's initial split into its own roll entry.** From
`HI/2026/HI_2026_bills.json`:

```json
{ "option": "yes", "voter_name": "Lee" },
{ "option": "yes", "voter_name": "C" },
{ "option": "yes", "voter_name": "Inouye" }
```

`"C"` is almost certainly the middle initial of the "Lee" entry
immediately before it, landed in its own roll entry instead of the name.
See WY below for the same pattern at larger scale.

**Fixed** (initial-fragmentation issue only; the garbled `"Senator(s"`
placeholder is a source-data gap with no way to reconstruct the intended
name, and is left as-is). `split_specific_votes` in `scrapers/hi/bills.py`
now merges any comma-split fragment matching a bare initial (`^[A-Z]\.?$`)
into the name before it, since such a fragment can never legitimately be a
standalone surname. Verified with a standalone script
(`split_specific_votes` copied out, no repo deps needed) against the exact
documented input `"Lee, C., Inouye"`, which now correctly produces
`["Lee, C.", "Inouye"]` instead of `["Lee", "C", "Inouye"]`; a normal
multi-name string is unaffected.

## IA

Declared `counts` vs. roll disagree, in both directions across different
records. From `IA/2025-2026/IA_2025-2026_bills.json`: one vote declares
100 (90 yes / 10 other), roll itemizes 103 (92 yes / 11 other); another
declares 50 (34 yes / 13 no over two records), roll itemizes the same
total but split 33 yes / 14 no.

## ID

Two distinct issues:

**Partial (exceptions-only) roll.** From `ID/2026/ID_2026_bills.json`, a
vote declaring 17 yes / 17 no / 1 absent has an 18-row `votes` array
containing only the 17 "no" voters plus the absentee — the winning "yes"
side is never itemized.

**Two legislators share a bare surname with nothing to tell them apart.**
ID's votes carry no first name or id, only a surname — and the Idaho
House has two members surnamed "Crane" and two surnamed "Tanner". From
the same archive, one roll legitimately contains both:

```json
{ "option": "yes", "voter_name": "Tanner" }, ... { "option": "yes", "voter_name": "Tanner" },
{ "option": "no", "voter_name": "Crane" }, ... { "option": "no", "voter_name": "Crane" }
```

Two rows each, same option both times. See `dedupeVoteByPerson` in
`normalize.ts`: it only dedupes votes sharing a stable
`openstatesPersonId`, never by bare `voter_name`, specifically because of
this case — deduping by name alone was silently dropping one of the two
real votes.

## IL

Declared `counts` vs. roll disagree by 1. From
`IL/104th/IL_104th_bills.json`: declared 59 yes, roll itemizes 58.

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## KY

Declared `counts` vs. roll disagree by 1. From
`KY/2026RS/KY_2026RS_bills.json`: declared 5 "other", roll itemizes 6.

## MA

Declared `counts` vs. roll disagree by 7. From
`MA/194th/MA_194th_bills.json`: declares zero "other" votes, roll
itemizes 7 (labeled "not voting" in the roll, a category the declared
`counts` omits entirely).

## ME

Produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## MI — PARTIALLY FIXED

Two distinct issues:

**Partial (exceptions-only) roll.** From
`MI/2025-2026/MI_2025-2026_bills.json`, a vote declaring 4 yes / 5 no has
a `votes` array containing only the 5 "no" voters — the winning "yes"
side is never itemized:

```json
{
  "motion_text": "PASSED; GIVEN IMMEDIATE EFFECT ROLL CALL # 198 YEAS 33 NAYS 3 EXCUSED 2 NOT VOTING 0",
  "start_date": "2026-07-03",
  "counts": [{ "option": "no", "value": 5 }, { "option": "yes", "value": 4 }],
  "votes": [
    { "option": "no", "voter_name": "Greene" },
    { "option": "no", "voter_name": "Irwin" },
    { "option": "no", "voter_name": "Runestad" },
    { "option": "no", "voter_name": "Lauwers" },
    { "option": "no", "voter_name": "Santana" }
  ]
}
```

(`motion_text` here is also its own separately-sourced summary line —
"YEAS 33 NAYS 3" — that disagrees with the record's own `counts` of 4
yes / 5 no on the same vote.)

**Whole roll duplicated within one record.** A different MI record
declares 195 yes / 27 no (222 total) with a 210-entry roll where every
name appears exactly twice (105 distinct legislators):

```json
{
  "counts": [{ "option": "no", "value": 27 }, { "option": "yes", "value": 195 }],
  "votes": [
    { "option": "yes", "voter_name": "Alexander" },
    { "option": "yes", "voter_name": "Fitzgerald" },
    { "option": "yes", "voter_name": "Markkanen" },
    { "option": "yes", "voter_name": "Rogers" },
    { "option": "yes", "voter_name": "Andrews" },
    { "option": "yes", "voter_name": "Foreman" }
    /* ... 204 more entries; the same 105 names each recur once more later */
  ]
}
```

Same pattern as NY, MT, NJ, and OR below.

**Fixed** (whole-roll-duplication issue only; the partial-roll issue is a
source-data gap and left as-is, same as the analogous TX/ID/TN cases).
`parse_roll_call` in `scrapers/mi/bills.py` now skips a name if it's
already been recorded for the current vote type within the current roll
call, first occurrence wins. Verified with a standalone script
reproducing the documented shape (105 distinct legislators each appearing
twice within one "Yeas" journal line) and confirming the dedupe collapses
it to 105.

## MN

Produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## MT — FIXED

**Whole roll duplicated within one record.** From
`MT/2025/MT_2025_bills.json`, a vote declares 42 yes with a 42-entry roll
where every name appears exactly twice (21 distinct legislators):

```json
{
  "motion_text": "be_concurred_in_as_amended",
  "start_date": "2025-03-19T22:44:42+00:00",
  "counts": [
    { "option": "abstain", "value": 0 },
    { "option": "excused", "value": 0 },
    { "option": "absent", "value": 0 },
    { "option": "no", "value": 0 },
    { "option": "yes", "value": 42 }
  ],
  "votes": [
    { "option": "yes", "voter_name": "SJ Howell" },
    { "option": "yes", "voter_name": "Lyn Bennett" },
    { "option": "yes", "voter_name": "Ed Buttrey" },
    { "option": "yes", "voter_name": "Brian Close" },
    { "option": "yes", "voter_name": "Melody Cunningham" },
    { "option": "yes", "voter_name": "Scott DeMarois" }
    /* ... 36 more entries; the same 21 names each recur once more later */
  ]
}
```

Note this record's own `counts` (42) already reflects the doubled total,
not the real headcount — the duplication runs through both fields
consistently, which is why it doesn't surface as a "Vote count mismatch"
(both sides of the comparison are doubled by the same amount).

**Fixed.** `scrape_votes_page` in `scrapers/mt/bills.py` now dedupes
`row["legislatorVotes"]` by legislator id before either tallying `counts`
or building the roll, so a legislator can't be counted or voted twice for
the same record regardless of whether the duplication originates from the
API. This is a same-value dedup, not a blind first-wins: if the two rows
for one legislator disagree on the vote cast, that's a genuine source
conflict we can't silently resolve, so the scraper logs a warning and
keeps the first instead of picking one arbitrarily with no record of the
disagreement. Live queries against
`api.legmt.gov/bills/v1/votes/findByBillId` for bill ids 1-2500 didn't
currently reproduce a doubled roll (upstream may have since deduped, or
the archived example is from an older session range), so this was
verified with a standalone script constructing the documented shape by
hand — 21 distinct legislators each appearing twice (42 entries) — and
confirming the dedupe collapses it back to 21 with no conflict warnings
(true duplicates, not disagreements), plus a synthetic case confirming a
genuine option conflict is warned about rather than silently dropped.

## NC

Declared `counts` vs. roll disagree by 1. From
`NC/2025/NC_2025_bills.json`: declared 14 "other", roll itemizes 13.

## NH

Two distinct issues:

**Declared counts vs. roll disagree.** From
`NH/2026/NH_2026_bills.json`, a House vote declares 180 yes / 157 no / 54
other but its 384-entry roll itemizes only 179 yes / 151 no / 54 other:

```json
{
  "motion_text": "Table",
  "start_date": "2026-03-05T15:25:17-05:00",
  "counts": [
    { "option": "other", "value": 54 },
    { "option": "no", "value": 157 },
    { "option": "yes", "value": 180 }
  ]
  // votes.length === 384, but only 179 are "yes" and 151 are "no"
}
```

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## NJ

**Whole roll duplicated within one record.** From
`NJ/221/NJ_221_bills.json`, a vote declares 49 yes / 29 no / 2 other (80
total) with an 80-entry roll where every name appears exactly twice (40
distinct legislators):

```json
{
  "counts": [
    { "option": "other", "value": 2 },
    { "option": "no", "value": 29 },
    { "option": "yes", "value": 49 }
  ],
  "votes": [
    { "option": "yes", "voter_name": "Amato, Carmen F." },
    { "option": "yes", "voter_name": "Beach, James" },
    { "option": "no", "voter_name": "Bramnick, Jon M." },
    { "option": "no", "voter_name": "Bucco, Anthony M." },
    { "option": "yes", "voter_name": "Burgess, Renee C." },
    { "option": "yes", "voter_name": "Burzichelli, John J." }
    /* ... 74 more entries; the same 40 names each recur once more later */
  ]
}
```

## NM

Produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## NY — FIXED

Two distinct issues, both caused by the same scraper bug (not the
source site):

**Duplicate/conflicting per-voter rows**, and **the entire roll listed
twice (or more) in one vote event.** Root cause: `scrape_assembly_votes`
in `scrapers/ny/bills.py` matched vote rows with
`table.xpath('//div[@class="vote-name"]')` — a `//`-prefixed XPath is
absolute, so it matched every `vote-name` div on the whole page, not just
the ones belonging to the current vote's table. A bill page with 3 floor
votes on it fed all 3 tables' rows into every VoteEvent. Fixed (commit
`4003690aa`, cherry-picked onto this branch) by walking `table.itersiblings()`
and stopping at the next `table`, since the vote-name divs are siblings of
the table rather than children of it.

**Verification.** `_verify/verify_ny.py` parses a cached bill page with 3
floor-vote tables (`bn=A00056`, `_cache/nyassembly.gov,leg,bn=A00056*`)
with both the old unscoped XPath and the new sibling-walk, no live
request needed:

```
BEFORE (unscoped //div, bug):
  table#1: 450 vote-name divs matched
  table#2: 450 vote-name divs matched
  table#3: 450 vote-name divs matched
AFTER (scoped to table siblings, fix):
  table#1: 150 vote-name divs matched
  table#2: 150 vote-name divs matched
  table#3: 150 vote-name divs matched
```

150 is the real per-table roll size (matches Assembly membership); 450 is
3× that — the whole-page bleed. Filed upstream as
[openstates-scrapers#5748](https://github.com/openstates/openstates-scrapers/issues/5748).

A sampled NY
Assembly vote event declared 154 votes (144 yes, 10 excused) but its
`votes` array had 298 entries — 147 of 149 distinct names appeared
exactly twice each. This is cosmetic, not data loss: `load.ts` writes
`LegislativeVote` rows keyed by resolved person id (first occurrence
wins, see `personVotes` in `load.ts`), so the duplication never reaches
the database. It still trips the normalize-stage "Vote count mismatch"
warning, which is otherwise accurate here — the source record really is
internally inconsistent. From `NY/2025-2026/NY_2025-2026_bills.json`:

```json
{
  "motion_text": "Assembly Vote",
  "start_date": "2025-06-09T00:00:00-04:00",
  "organization__classification": "lower",
  "counts": [{ "option": "excused", "value": 10 }, { "option": "yes", "value": 144 }],
  "votes": [
    { "option": "yes", "voter_name": "Alvarez" },
    { "option": "yes", "voter_name": "Carroll P" },
    { "option": "yes", "voter_name": "Friend" },
    { "option": "yes", "voter_name": "Lee" },
    { "option": "yes", "voter_name": "Peoples-Stokes" },
    { "option": "yes", "voter_name": "Slater" }
    /* ... 292 more entries; "Alvarez", "Carroll P", "Friend", "Lee",
       "Peoples-Stokes", and "Slater" each recur later in the same array,
       each time with the same option ... */
  ]
}
```

Same whole-roll-duplication pattern as MI, MT, NJ, and OR.

## OK

Declared `counts` vs. roll disagree by 1. From
`OK/2025/OK_2025_bills.json`: declares zero "other" votes, roll itemizes
1.

## OR — FIXED

**Whole roll duplicated within one record.** Every sampled OR mismatch in
this run (242 of 242) showed this pattern. From
`OR/2025R1/OR_2025R1_bills.json`, a vote declares 42 yes / 4 absent (46
total) with a 46-entry roll where every name appears exactly twice (23
distinct legislators):

```json
{
  "counts": [{ "option": "absent", "value": 4 }, { "option": "no", "value": 0 }, { "option": "yes", "value": 42 }],
  "votes": [
    { "option": "yes", "voter_name": "Ben Bowman" },
    { "option": "yes", "voter_name": "Vikki Breese-Iverson" },
    { "option": "yes", "voter_name": "Jami Cate" },
    { "option": "absent", "voter_name": "Christine Drazan" },
    { "option": "yes", "voter_name": "Paul Evans" },
    { "option": "yes", "voter_name": "David Gomberg" }
    /* ... 40 more entries; the same 23 names each recur once more later */
  ]
}
```

**Fixed.** Both `add_individual_votes` and `tally_votes` in
`scrapers/or/votes.py` consumed `event["MeasureVotes"]` /
`event["CommitteeVotes"]` directly from the OData `$expand` response;
added a `dedupe_votes` helper (by `VoteName`) called once on that list
before either function reads it, so both the tally and the roll agree.
The dedup checks the vote option (`Vote` for measures, `Meaning` for
committee actions), not just the name: a true duplicate row (same
legislator, same option) is silently collapsed, but if the two rows
disagree on the vote cast, that's a genuine source conflict, so it's
logged as a warning and the first is kept rather than picking one with no
record of the disagreement. Live queries against
`api.oregonlegislature.gov`'s OData endpoint for a small sample of
2025R1 measures didn't currently reproduce a doubled roll, so this was
verified with a standalone script constructing the documented shape by
hand (23 distinct legislators each appearing twice, 46 entries),
confirming the dedupe collapses it back to 23 with no conflict warnings,
plus a synthetic case confirming a genuine option conflict is warned
about rather than silently dropped.

## PA

Two distinct issues:

**Declared counts vs. roll disagree.** From
`PA/2025-2026/PA_2025-2026_bills.json`, a Senate vote declares zero
`"other"` votes while its own roll lists one:

```json
{
  "motion_text": "FINAL PASSAGE",
  "start_date": "2025-11-18T20:52:00+00:00",
  "counts": [
    { "option": "other", "value": 0 },
    { "option": "no", "value": 0 },
    { "option": "yes", "value": 49 }
  ],
  "votes": [
    ...
    { "option": "other", "voter_name": "Art Haywood" },
    ...
  ]
}
```

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## RI

Declared `counts` vs. roll disagree by 1. From
`RI/2025/RI_2025_bills.json`: declared 3 "other", roll itemizes 4.

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## SC

Declared `counts` vs. roll disagree by 2. From
`SC/2025-2026/SC_2025-2026_bills.json`: declared 6 "other", roll
itemizes 4.

## SD

Produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section
(the smallest, fully-shown example lives there).

## TN

**Partial (exceptions-only) roll.** From `TN/114/TN_114_bills.json`, a
vote declaring 79 yes / 17 no / 1 not voting (97 total) has a `votes`
array with exactly one entry — the single "not voting" member:

```json
{
  "motion_text": "FLOOR VOTE: REGULAR CALENDAR    PASSAGE ON THIRD CONSIDERATION  4/22/2025  Passed (1)",
  "start_date": "2025-04-22",
  "counts": [
    { "option": "not voting", "value": 1 },
    { "option": "no", "value": 17 },
    { "option": "yes", "value": 79 }
  ],
  "votes": [{ "option": "not voting", "voter_name": "Pearson" }]
}
```

No yes/no voters are ever itemized in TN, only exceptions. Every TN
mismatch we sampled followed this same pattern.

## TX — PARTIALLY FIXED

Three distinct issues:

**Partial (exceptions-only) roll.** From `TX/89R/TX_89R_bills.json`, a
vote declaring 30 yes has a `votes` array with one entry, the lone
"absent" member:

```json
{
  "motion_text": "passage",
  "start_date": "2025-02-25",
  "counts": [
    { "option": "not voting", "value": 0 },
    { "option": "no", "value": 0 },
    { "option": "yes", "value": 30 }
  ],
  "votes": [{ "option": "absent", "voter_name": "West" }]
}
```

**Garbled/truncated voter-name strings.** From the same archive, one
House roll's tail contains:

```json
{ "option": "not voting", "voter_name": "Present" },
{ "option": "not voting", "voter_name": "Speaker" },
{ "option": "not voting", "voter_name": "Harris(C" },
{ "option": "absent", "voter_name": "Lopez" },
{ "option": "absent", "voter_name": "J" }
```

TX has multiple Representatives surnamed Harris, disambiguated with a
parenthetical first name elsewhere in the archive (e.g. `"Bell, C."`) —
here `"Harris(C"` is truncated mid-parenthesis, and `"Lopez"` / `"J"`
look like the same truncation splitting a `"Lopez, J."` entry in two.

**Fixed** (garbled/truncated names issue only; the partial-roll issue is a
source-data gap — the site itself never furnishes the winning side, so
there's nothing to fix in the scraper). Two bugs in `names()` in
`scrapers/tx/votes.py`: (1) it blindly sliced off the last character of
the final name in a roll assuming it was always a trailing `"."`, which
truncated names ending in anything else, e.g. `"Harris(C)"` ->
`"Harris(C"`; now it only strips a trailing `"."`. (2) the comma-fallback
split (used when a roll has fewer than 7 semicolon-separated entries)
fragmented a middle initial into its own entry, e.g. `"Lopez, J."` ->
`"Lopez"`, `"J"`; now, as in HI above, a bare-initial fragment is merged
back into the preceding name. Verified with a standalone script (`names()`
copied out, no repo deps needed) against both the semicolon and
comma-fallback code paths using the documented `"Bell, C.; Harris(C);
Lopez, J."`-style input: output is now `["Bell, C", "Harris(C)", "Lopez,
J"]` in both paths, with no bare `"J"` or truncated `"Harris(C"` entries.

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## VA

Produces literal duplicate vote-event records — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.
Also the reason `derivedVoteEventId` in `normalize.ts` folds in a
fingerprint of the actual roll call, not just motion text: VA's budget
bill (HB 30) racks up dozens of floor votes a day, and VA gives every one
of them the same generic motion text (`"H VOTE:"`) — without the roll
fingerprint, same-day/same-chamber votes on that bill collided into one
record and silently dropped the rest.

## VT

Two distinct issues:

**Declared counts vs. roll disagree** by 1. From
`VT/2025-2026/VT_2025-2026_bills.json`: declared 16 no, roll itemizes 15.

**The same vote republished under two different roll-call reference
numbers.** From the same archive, two vote events have byte-identical
`motion_text`, `start_date`, `counts`, and full 30-member roll, differing
only in the roll-call id embedded in `identifier`'s URL:

```
.../loadBillRollCallDetails/2026/161
.../loadBillRollCallDetails/2026/157
```

Unlike most jurisdictions in the
[Duplicate vote-event records](#duplicate-vote-event-records) section,
this isn't caught by our roll-fingerprint dedup because the two records
are genuinely identical in every field we hash — they collapse into one
vote event anyway (correct outcome, no data loss), but it means VT's site
assigned two different roll-call reference numbers to what appears to be
the same recorded vote.

## WA

Declared `counts` vs. roll disagree by 18 — the largest gap we found in
this run. From `WA/2025-2026/WA_2025-2026_bills.json`, a vote titled
"3rd Reading & Final Passage (#7)" declares 98 yes (WA's House has 98
seats — this reads like a unanimous roll-call vote), but the roll
itemizes only 80:

```json
{
  "motion_text": "3rd Reading & Final Passage (#7)",
  "counts": [
    { "option": "other", "value": 0 },
    { "option": "no", "value": 0 },
    { "option": "yes", "value": 98 }
  ]
  // votes.length === 80
}
```

## WI

Declared `counts` vs. roll disagree by 2. From
`WI/2025/WI_2025_bills.json`: declared 2 "other", roll itemizes 0.

Also produces a literal duplicate vote-event record — see the
[Duplicate vote-event records](#duplicate-vote-event-records) section.

## WY

**A legislator's middle initial split into its own roll entry.** From
`WY/2026/WY_2026_bills.json`, a House roll for the FY26 budget bill (HB
30) contains, among 68 entries for a 62-seat chamber:

```json
{ "option": "no", "voter_name": "Brown" },
{ "option": "no", "voter_name": "G" },
{ "option": "no", "voter_name": "Brown" },
{ "option": "no", "voter_name": "L" },
...
{ "option": "yes", "voter_name": "Campbell" },
{ "option": "yes", "voter_name": "E" },
...
{ "option": "no", "voter_name": "Campbell" },
{ "option": "no", "voter_name": "K" }
```

Evidently meant to be one legislator each — `"Brown, G."`, `"Brown, L."`,
`"Campbell, E."`, `"Campbell, K."` — distinguishing multiple
representatives who share a surname, but the initial lands in its own
roll entry instead of the name. This inflates the roll past both the
chamber's real seat count and the vote event's own declared `counts`. We
don't try to merge these fragments back into the preceding name —
guessing which stray token belongs to which neighbor risks silently
fabricating or misattributing a vote, which is worse than the mismatch
warning.

## Duplicate vote-event records

AZ, CO, CT, IL, ME, MN, NH, NM, PA, RI, SD, TX, VA, and WI produce
"Duplicate vote event" warnings because the archive contains a literal
duplicate vote-event record — same bill, date, chamber, motion text, and
roll (occasionally reordered), appearing twice. This is harmless:
`load.ts` writes `LegislativeVote` rows keyed by resolved person id
regardless of how many times a vote event's raw record recurs, and
`derivedVoteEventId`'s roll fingerprint correctly recognizes these as the
same vote, so the second copy is dropped rather than double-counted.
Every sampled pair we checked across these 14 jurisdictions was identical
once each roll was compared as a set rather than an ordered array.
Smallest complete example, from `SD/2026/SD_2026_bills.json` (13-entry
roll, appears twice verbatim):

```json
{
  "motion_text": "Deferred to the 41st legislative day",
  "start_date": "2026-02-26",
  "organization__classification": "lower",
  "counts": [
    { "option": "excused", "value": 1 },
    { "option": "no", "value": 2 },
    { "option": "yes", "value": 10 }
  ],
  "votes": [
    { "option": "no", "voter_name": "Goodwin" },
    { "option": "yes", "voter_name": "Hunt" },
    { "option": "yes", "voter_name": "Ismay" },
    { "option": "yes", "voter_name": "Ladner" },
    { "option": "yes", "voter_name": "May" },
    { "option": "yes", "voter_name": "Nolz" },
    { "option": "excused", "voter_name": "Peterson (Drew)" },
    { "option": "no", "voter_name": "Rice" },
    { "option": "yes", "voter_name": "Van Diepen" },
    { "option": "yes", "voter_name": "Wittman" },
    { "option": "yes", "voter_name": "Shubeck" },
    { "option": "yes", "voter_name": "Gosch" },
    { "option": "yes", "voter_name": "Overweg" }
  ]
}
```

VT produces the same warning for a different reason — see the VT section
above.
