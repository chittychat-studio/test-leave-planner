"""A working leave planner -- the reference solution for job 3.

Written by the channel (not by any model in a test) as an exact dynamic
program. It passes all 9 tests in 3-build-the-planner, including the
full-year speed test.

Use it:
    python planner.py --holidays holidays.txt --start 2026-01-01 --end 2026-12-31 --leave 3

holidays.txt is one public holiday per line, YYYY-MM-DD. Weekends are
Saturday and Sunday. It prints the leave days to take and the total days off.
"""
import argparse
import pathlib
import sys
from datetime import timedelta

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "3-build-the-planner"))
from leavecalc import parse, is_off_day  # noqa: E402


def better(a, b):
    # a, b = (score, leaves_tuple): higher score, then fewer leaves, then smaller list
    if b is None:
        return True
    if a[0] != b[0]:
        return a[0] > b[0]
    if len(a[1]) != len(b[1]):
        return len(a[1]) < len(b[1])
    return a[1] < b[1]


def plan_leaves(holidays, start, end, k):
    s, e = parse(start), parse(end)
    states = {(0, 0, False): (0, ())}   # (used, pending off-days, in a break) -> (score, leaves)
    d = s
    while d <= e:
        nxt = {}

        def put(key, val):
            if better(val, nxt.get(key)):
                nxt[key] = val

        for (used, pend, has), (sc, lv) in states.items():
            if is_off_day(d, holidays):
                put((used, 0, True) if has else (used, pend + 1, False), (sc + 1, lv) if has else (sc, lv))
            else:
                put((used, 0, False), (sc, lv))
                if used < k:
                    put((used + 1, 0, True), (sc + (1 if has else pend + 1), lv + (d.isoformat(),)))
        states = nxt
        d += timedelta(days=1)
    best = None
    for v in states.values():
        if better(v, best):
            best = v
    if best is None or best[0] == 0:
        return {"leaves": [], "days_off": 0}
    return {"leaves": list(best[1]), "days_off": best[0]}


def main():
    ap = argparse.ArgumentParser(description="Pick the leave days that give the most days off.")
    ap.add_argument("--holidays", required=True, help="text file, one YYYY-MM-DD per line")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--leave", type=int, required=True, help="how many leave days you can take")
    a = ap.parse_args()
    hol = {line.strip() for line in open(a.holidays, encoding="utf-8") if line.strip()}
    r = plan_leaves(hol, a.start, a.end, a.leave)
    if not r["leaves"]:
        print("No leave day adds a break in this window.")
        return
    print("Take these days off: " + ", ".join(r["leaves"]))
    print(f"Days off in total: {r['days_off']}")


if __name__ == "__main__":
    main()
