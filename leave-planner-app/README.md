# The take-home test: a time-off planner

One small app, three jobs. Give the same jobs, prompts and files to each model you want to compare, and let the tests do the marking.

The idea behind the app: give it your public holidays and it tells you which days to take off. A holiday on a Friday plus one day off on the Thursday makes a four-day weekend.

| Folder | Job | How it's marked |
|---|---|---|
| `1-fix-the-calculator/` | `leavecalc.py` has **5 hidden bugs**. Fix it without touching the tests. | 14 tests: count how many pass |
| `2-clean-the-sheet/` | Clean a messy team time-off log and answer 4 questions. | 4 answers, checked against `answer_key.json` |
| `3-build-the-planner/` | Build `planner.py` from scratch, as `SPEC.md` describes. | 9 tests, including a full year in under 20 seconds |

You need Python 3.10+ and `pip install pytest`.

## How to run it with a coding agent

1. Copy one job's folder into an empty folder and open your agent there (for example, `claude` in Claude Code, or Codex).
2. Paste that job's prompt below, word for word, and use the same prompt for every model you compare.
3. Give each model **two tries**. On the second try, paste back only the failing test output.
4. Mark it: `pytest -q` in folders 1 and 3; compare the JSON with `answer_key.json` in folder 2.

**Job 1 prompt**
> The test suite test_leavecalc.py is failing. Fix leavecalc.py so that every test passes. Do not change the tests.

**Job 2 prompt**
> Clean leave_requests.csv exactly as QUESTIONS.md says and reply with one JSON object containing exactly the four keys it lists.

**Job 3 prompt**
> Build planner.py exactly as SPEC.md describes, using leavecalc.py. test_planner.py must pass, including the full-year speed test. Do not change any given file.

Tell us who won, and on what, in the comments of the Short.

## Just want the planner?

`solutions/planner.py` is a working version (written by the channel, not by a model under test):

```
python solutions/planner.py --holidays my_holidays.txt --start 2026-01-01 --end 2026-12-31 --leave 3
```

`my_holidays.txt` is one date per line, `YYYY-MM-DD`. Weekends are Saturday and Sunday.

`solutions/sheet_answers.py` shows how the job 2 key was computed. Both are spoilers, so look after your agent has answered.

## Notes

- This is a small, fixed test, not a benchmark. One run tells you about your task, not about the model in general.
- If you call models through an API, you pay for it with your own keys.
- The example dates are 2026, and the holiday list is only sample data. Swap in your own.
