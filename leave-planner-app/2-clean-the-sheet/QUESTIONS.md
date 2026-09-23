# Job 2: clean the sheet

`leave_requests.csv` is a made-up team time-off log (no real people). Clean it with exactly these rules, in order:

1. Drop exact duplicate rows, keeping the first.
2. Drop rows whose `approved` field is blank.
3. Team names: trim spaces and use Title Case.
4. `start_date` is either `YYYY-MM-DD` or `DD/MM/YYYY`.

Then answer, as one JSON object with exactly these four keys:

- `q1_clean_rows`: number of rows after cleaning (integer)
- `q2_support_approval_pct`: percent of Support rows with `approved = Y`, rounded to 1 decimal
- `q3_team_most_approved_days`: the team with the highest total `days_requested` over approved rows
- `q4_approved_friday_starts`: number of approved rows whose `start_date` is a Friday

Mark it against `answer_key.json`. Numbers match within 0.05. Don't open the key until your agent has answered.
