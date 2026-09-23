import json, pathlib, pytest
from planner import plan_leaves

CASES = json.loads((pathlib.Path(__file__).parent / "cases.json").read_text())


@pytest.mark.parametrize("case", CASES, ids=[f"{c['args'][1]}_{c['args'][2]}_k{c['args'][3]}" for c in CASES])
def test_plan(case):
    hol, start, end, k = case["args"]
    assert plan_leaves(set(hol), start, end, k) == case["expect"]


def test_full_year_k3_is_fast():
    # A senior-level job: must finish a whole year with 3 leaves in under 20 seconds.
    import time
    hol = set(CASES[0]["args"][0])
    t = time.time()
    r = plan_leaves(hol, "2026-01-01", "2026-12-31", 3)
    assert time.time() - t < 20
    # Verified by two independent reference solutions (brute force agrees on every
    # small case; exact DP gives this): 12 days off.
    assert r == {"leaves": ["2026-01-23", "2026-10-01", "2026-10-19"], "days_off": 12}
