from leavecalc import (parse, is_off_day, leaves_needed, days_off_block,
                       leave_ratio, best_single_leaves)
import pytest

# 2026 examples. 2026-10-02 (a public holiday) is a Friday.
# 2026-01-26 (a public holiday) is a Monday. 2026-08-15 (a public holiday) is a Saturday.
H = {"2026-01-26", "2026-08-15", "2026-10-02", "2026-12-25"}


def test_parse():
    assert parse("2026-10-02").month == 10
    assert parse("2026-10-02").day == 2


def test_saturday_is_off():
    assert is_off_day(parse("2026-10-03"), H)


def test_sunday_is_off():
    assert is_off_day(parse("2026-10-04"), H)


def test_holiday_is_off():
    assert is_off_day(parse("2026-10-02"), H)


def test_monday_is_working():
    assert not is_off_day(parse("2026-10-05"), H)


def test_leaves_single_day():
    assert leaves_needed("2026-10-05", "2026-10-05", H) == 1


def test_leaves_full_week_is_inclusive():
    # Mon 5 Oct to Fri 9 Oct: five working days.
    assert leaves_needed("2026-10-05", "2026-10-09", H) == 5


def test_leaves_skip_weekend_holiday():
    # Thu 1 Oct to Mon 5 Oct: Fri 2 is a holiday, Sat and Sun are off.
    assert leaves_needed("2026-10-01", "2026-10-05", H) == 2


def test_leaves_end_before_start():
    with pytest.raises(ValueError):
        leaves_needed("2026-10-05", "2026-10-01", H)


def test_block_thursday_leave():
    # Leave Thu 1 Oct: Thu + Fri holiday + Sat + Sun = 4 days off.
    assert days_off_block("2026-10-01", "2026-10-01", H) == ("2026-10-01", "2026-10-04", 4)


def test_block_extends_backwards():
    # Leave Tue 27 Jan: Sat 24, Sun 25, Mon 26 holiday, Tue 27 = 4 days.
    assert days_off_block("2026-01-27", "2026-01-27", H) == ("2026-01-24", "2026-01-27", 4)


def test_ratio_one_leave_four_days():
    assert leave_ratio("2026-10-01", "2026-10-01", H) == 4.0


def test_ratio_no_leave_needed():
    assert leave_ratio("2026-10-03", "2026-10-04", H) is None


def test_best_single_leaves_2026():
    best = best_single_leaves(H, 2026)
    assert [d for d, _ in best] == [
        "2026-01-23", "2026-01-27", "2026-10-01",
        "2026-10-05", "2026-12-24", "2026-12-28",
    ]
    assert all(t == 4 for _, t in best)
