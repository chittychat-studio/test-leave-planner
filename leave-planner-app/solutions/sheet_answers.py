"""How the job 2 answer key was computed, using the same four cleaning rules. Spoiler."""
import csv, json
from datetime import date, datetime
import pathlib
rows = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parent.parent / "2-clean-the-sheet" / "leave_requests.csv")))
seen, clean = set(), []
for r in rows:
    k = tuple(r.values())
    if k in seen:            # rule 1: drop exact duplicate rows
        continue
    seen.add(k)
    if r["approved"].strip() == "":   # rule 2: drop rows with blank approval
        continue
    r["team"] = r["team"].strip().title()   # rule 3: normalise team names
    s = r["start_date"]
    r["start"] = datetime.strptime(s, "%d/%m/%Y").date() if "/" in s else date.fromisoformat(s)  # rule 4
    r["days"] = int(r["days_requested"])
    clean.append(r)
q1 = len(clean)
sup = [r for r in clean if r["team"] == "Support"]
q2 = round(100 * sum(r["approved"] == "Y" for r in sup) / len(sup), 1)
teams = sorted({r["team"] for r in clean})
tot = {t: sum(r["days"] for r in clean if r["team"] == t and r["approved"] == "Y") for t in teams}
q3 = max(teams, key=lambda t: (tot[t], t))
q4 = sum(1 for r in clean if r["approved"] == "Y" and r["start"].weekday() == 4)
ans = {"q1_clean_rows": q1, "q2_support_approval_pct": q2, "q3_team_most_approved_days": q3, "q4_approved_friday_starts": q4}
print(json.dumps(ans, indent=2))
