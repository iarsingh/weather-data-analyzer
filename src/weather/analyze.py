import math
from statistics import pstdev

MAX_ROWS = 10000


class InputError(ValueError):
    pass


def analyze(rows):
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) for r in rows):
        raise InputError("rows must be a non-empty list of objects")
    if len(rows) > MAX_ROWS:
        raise InputError(f"at most {MAX_ROWS} rows are allowed")
    values, groups = [], {}
    skipped = 0
    for row in rows:
        raw = row.get("temp_c")
        try:
            if isinstance(raw, bool):
                raise ValueError("boolean temperature")
            number = float(raw)
            if not math.isfinite(number) or not -100 <= number <= 100:
                raise ValueError("temperature outside supported range")
        except (TypeError, ValueError, OverflowError):
            skipped += 1
            continue
        values.append(number)
        city = row.get("city")
        key = str(city).strip() if city is not None else "unknown"
        groups.setdefault(key or "unknown", []).append(number)
    if not values:
        raise InputError("no valid finite temp_c values in [-100, 100]")
    values.sort()
    mid = len(values) // 2
    median = values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
    return {
        "rows": len(rows), "valid_rows": len(values), "skipped": skipped,
        "mean": round(sum(values) / len(values), 4), "median": median,
        "min": values[0], "max": values[-1], "stddev": round(pstdev(values), 4),
        "by_city": {name: round(sum(nums) / len(nums), 4) for name, nums in sorted(groups.items())},
        "city_counts": {name: len(nums) for name, nums in sorted(groups.items())},
    }
