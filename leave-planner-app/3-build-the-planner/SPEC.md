# Task: build `planner.py`

`leavecalc.py` (given, correct, do not edit) has the leave math. Build
`planner.py` with one function:

    plan_leaves(holidays, start, end, k) -> dict

- `holidays`: set of ISO date strings. Weekends are Saturday and Sunday.
- `start`, `end`: ISO date strings, the planning window, inclusive.
- `k`: the maximum number of leave days you may take (0 or more).

Choose at most `k` leave dates, each a working day inside the window.
A day is OFF if it is a weekend, a holiday or a chosen leave date. A
**break** is a maximal run of consecutive OFF days inside the window that
contains at least one chosen leave date. **Score** = total days in all breaks.

Return `{"leaves": [...ISO dates, ascending], "days_off": score}` for the plan
with the highest score. Ties: fewer leaves wins; then the plan whose sorted
leave list is smallest in plain string comparison. If no plan scores above 0
(k is 0, or no working days), return `{"leaves": [], "days_off": 0}`.

Runs of OFF days are only counted inside the window: do not extend past
`start` or `end`.
