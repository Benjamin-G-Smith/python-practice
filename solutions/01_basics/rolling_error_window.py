"""
Real-world scenario
--------------------
Ops wants to know how a service's error rate has moved over time, not
just its overall total (which is what error_rate_by_service in
log_analytics.py computes). Specifically: at each point in the log,
what was the error rate over just the last N entries? That "rolling"
view is what eventually flags a service that's currently having a bad
stretch, even if its all-time rate still looks fine.

This works on a flat, already-parsed list of entries - one service at a
time. Handling multiple services with independent windows at once comes
later; the point here is the sliding-window mechanic itself.

Skills practiced: collections.deque with maxlen for a fixed-size
sliding window, enumerate, finding a max with a key function.

Run this file directly to see your output and self-check results:
    python rolling_error_window.py
"""

from collections import deque

LEVELS = ["INFO", "INFO", "ERROR", "ERROR", "INFO", "ERROR", "INFO", "INFO", "ERROR", "INFO"]
ENTRIES = [{"level": level} for level in LEVELS]


def rolling_error_rate(entries: list[dict], window_size: int) -> list[float]:
    """
    Return a list `rates` the same length as `entries`, where rates[i]
    is the fraction of ERROR-level entries among the last `window_size`
    entries ending at position i (inclusive). Near the start of the
    list, before a full window exists yet, use however many entries are
    actually available.

    Round each rate to 2 decimal places.
    """
    window = deque(maxlen=window_size)
    rates = []
    for entry in entries:
        window.append(entry["level"] == "ERROR")
        rates.append(round(sum(window) / len(window), 2))
    return rates


def first_breach(rates: list[float], threshold: float) -> int | None:
    """
    Return the index of the first value in `rates` that is >= threshold,
    or None if no value ever reaches it.
    """
    for i, rate in enumerate(rates):
        if rate >= threshold:
            return i
    return None


def max_window_rate(entries: list[dict], window_size: int) -> tuple[int, float]:
    """
    Return (index, rate) for the single highest value produced by
    rolling_error_rate(entries, window_size). If multiple positions tie
    for the highest rate, return the earliest (smallest index) one.
    """
    rates = rolling_error_rate(entries, window_size)
    best_index = max(range(len(rates)), key=lambda i: rates[i])
    return best_index, rates[best_index]


# Known-correct rates, used to test first_breach independently of
# whether rolling_error_rate is actually right - so a bug in one
# function doesn't make an unrelated function's checks look broken too.
EXPECTED_RATES = [0.0, 0.0, 0.33, 0.5, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25]

ALL_INFO = [{"level": "INFO"}] * 3
ALL_ERROR = [{"level": "ERROR"}] * 3

# Three-way tie (indices 2, 3, 4 all land on the same rate) - the real
# test of "earliest index wins," since a window_size=1 or all-one-level
# dataset would let a bug default to the right answer by accident.
TIE_ENTRIES = [{"level": lvl} for lvl in ["INFO", "ERROR", "ERROR", "INFO", "ERROR", "INFO"]]


def _self_check() -> None:
    """
    Reports a pass/fail count per function instead of stopping at the
    first failure, so you can tell "rolling_error_rate is solid, 0/2 on
    first_breach" apart from "everything's broken." Still no pytest -
    just a small tally on top of plain checks.
    """
    results: dict[str, list[bool]] = {}

    def check(func_name: str, condition: bool, message: str) -> None:
        results.setdefault(func_name, []).append(condition)
        if not condition:
            print(f"  FAILED [{func_name}]: {message}")

    def not_implemented(func_name: str, count: int) -> None:
        results.setdefault(func_name, []).extend([False] * count)
        print(f"  FAILED [{func_name}]: not implemented (raises NotImplementedError)")

    rates = None
    try:
        rates = rolling_error_rate(ENTRIES, window_size=4)
        check("rolling_error_rate", rates == EXPECTED_RATES, f"unexpected rates: {rates}")

        r = rolling_error_rate(ALL_INFO, window_size=2)
        check("rolling_error_rate", r == [0.0, 0.0, 0.0], f"all-INFO should be all 0.0, got {r}")

        r = rolling_error_rate(ALL_ERROR, window_size=2)
        check("rolling_error_rate", r == [1.0, 1.0, 1.0], f"all-ERROR should be all 1.0, got {r}")

        r = rolling_error_rate(ENTRIES, window_size=1)
        check(
            "rolling_error_rate",
            r == [0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0],
            f"window_size=1 should be each entry's own level as 0.0/1.0, got {r}",
        )

        r = rolling_error_rate(ENTRIES, window_size=100)
        check(
            "rolling_error_rate",
            r == [0.0, 0.0, 0.33, 0.5, 0.4, 0.5, 0.43, 0.38, 0.44, 0.4],
            f"window larger than the list should use however many entries exist so far, got {r}",
        )

        r = rolling_error_rate([], window_size=4)
        check("rolling_error_rate", r == [], f"empty input should return [], got {r}")
    except NotImplementedError:
        not_implemented("rolling_error_rate", 6)

    try:
        check(
            "first_breach",
            first_breach(EXPECTED_RATES, 0.5) == 3,
            f"unexpected first_breach(rates, 0.5): {first_breach(EXPECTED_RATES, 0.5)}",
        )
        check(
            "first_breach",
            first_breach(EXPECTED_RATES, 0.9) is None,
            f"no rate ever reaches 0.9, expected None, got {first_breach(EXPECTED_RATES, 0.9)}",
        )
        b = first_breach(EXPECTED_RATES, 0.75)
        check("first_breach", b == 5, f"exact-match threshold should still count (>=), got {b}")

        b = first_breach(EXPECTED_RATES, 0.0)
        check("first_breach", b == 0, f"threshold 0.0 should match immediately at index 0, got {b}")

        b = first_breach([], 0.5)
        check("first_breach", b is None, f"empty rates list should return None, got {b}")
        check(
            "first_breach",
            first_breach(EXPECTED_RATES, 1.0) is None,
            f"no rate reaches 1.0, expected None, got {first_breach(EXPECTED_RATES, 1.0)}",
        )
    except NotImplementedError:
        not_implemented("first_breach", 6)

    try:
        check(
            "max_window_rate",
            max_window_rate(ENTRIES, window_size=4) == (5, 0.75),
            f"unexpected max_window_rate: {max_window_rate(ENTRIES, window_size=4)}",
        )
        m = max_window_rate(ENTRIES, window_size=1)
        check("max_window_rate", m == (2, 1.0), f"window_size=1 should find first error, got {m}")

        m = max_window_rate(ALL_ERROR, window_size=2)
        check("max_window_rate", m == (0, 1.0), f"unexpected max_window_rate on all-ERROR: {m}")

        m = max_window_rate(TIE_ENTRIES, window_size=3)
        check("max_window_rate", m == (2, 0.67), f"three-way tie should resolve earliest, got {m}")

        m = max_window_rate(ALL_INFO, window_size=2)
        check("max_window_rate", m == (0, 0.0), f"unexpected max_window_rate on all-INFO: {m}")

        m = max_window_rate(ENTRIES, window_size=100)
        check("max_window_rate", m == (3, 0.5), f"oversized window: {m}")
    except NotImplementedError:
        not_implemented("max_window_rate", 6)

    print()
    all_passed = True
    for func_name, checks in results.items():
        passed = sum(checks)
        total = len(checks)
        print(f"{func_name}: {passed}/{total} passed")
        if passed < total:
            all_passed = False

    if not all_passed:
        print()
        raise AssertionError("Some checks failed - see FAILED lines above for details.")

    print()
    print("All checks passed.")
    print(f"Rolling rates: {rates}")


if __name__ == "__main__":
    _self_check()
