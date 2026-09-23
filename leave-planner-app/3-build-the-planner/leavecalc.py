"""leavecalc: leave math for office holidays.

Dates are ISO strings "YYYY-MM-DD". Weekends are Saturday and Sunday.
"""
from datetime import date, timedelta


def parse(d):
    """Parse an ISO date string "YYYY-MM-DD" into a date."""
    y, m, dd = d.split("-")
    return date(int(y), int(m), int(dd))


def is_off_day(d, holidays):
    """True if d is a Saturday, Sunday, or a listed holiday."""
    return d.weekday() >= 5 or d.isoformat() in holidays


def leaves_needed(start, end, holidays):
    """Number of working days (leaves to apply) from start to end, inclusive."""
    s, e = parse(start), parse(end)
    if e < s:
        raise ValueError("end before start")
    n = 0
    d = s
    while d <= e:
        if not is_off_day(d, holidays):
            n += 1
        d += timedelta(days=1)
    return n


def days_off_block(start, end, holidays):
    """Extend [start, end] outward over adjacent off days.

    Returns (block_start, block_end, total_days) with ISO strings and the
    inclusive day count of the whole break.
    """
    s, e = parse(start), parse(end)
    while is_off_day(s - timedelta(days=1), holidays):
        s -= timedelta(days=1)
    while is_off_day(e + timedelta(days=1), holidays):
        e += timedelta(days=1)
    return s.isoformat(), e.isoformat(), (e - s).days + 1


def leave_ratio(start, end, holidays):
    """Days off per leave spent, rounded to 2 places. Zero leaves -> None."""
    n = leaves_needed(start, end, holidays)
    if n == 0:
        return None
    _, _, total = days_off_block(start, end, holidays)
    return round(total / n, 2)


def best_single_leaves(holidays, year):
    """Every working day in `year` whose single leave gives the longest break.

    Returns a list of (date, total_days) for the maximum total_days, sorted by
    date ascending.
    """
    best, out = 0, []
    d = date(year, 1, 1)
    while d.year == year:
        if not is_off_day(d, holidays):
            _, _, total = days_off_block(d.isoformat(), d.isoformat(), holidays)
            if total > best:
                best, out = total, [(d.isoformat(), total)]
            elif total == best:
                out.append((d.isoformat(), total))
        d += timedelta(days=1)
    return out
