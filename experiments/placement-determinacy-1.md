# Placement determinacy, first measurements (2026-11-05)

How many facts did the rules decide, and how many did the agent judge? Counted from each run's `placements.md` by the parent (last column). The relation agent's own count is about 17 of 38 by rules; the parent's parse gives 23. The two disagree, so read the figures as a range.

| Page | Kind | Facts | Rules decided | Judged | Other |
|---|---|---|---|---|---|
| `status` (run 2) | non-entity | 13 | 5 | 8 | 0 |
| `constraint` (run 3) | non-entity (keys) | 19 | 3 | 12 | 4 |
| `relation` (run 3) | entity | 38 | 17 to 23 | 14 to 15 | 1 |

Reading: the entity page is decided by the rules about half to three quarters of the time; the two non-entity pages are mostly judged. That is the evidence for Q3: the section grammar fits entity pages and gives no home to a value type, a key list or worker behavior. Agreement between independent runs on the same page is available only for `status`, and only run 2 recorded placements, so no agreement figure exists yet. A second run on `relation` or `constraint` with placements would give one.
