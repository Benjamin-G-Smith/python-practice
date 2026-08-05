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

    Use collections.deque(maxlen=window_size) to hold the window instead
    of re-slicing entries[...] on every iteration - the deque
    automatically drops the oldest item once it's full.

    TODO: implement this function.
    """
    raise NotImplementedError


def first_breach(rates: list[float], threshold: float) -> int | None:
    """
    Return the index of the first value in `rates` that is >= threshold,
    or None if no value ever reaches it.

    TODO: implement this function.
    """
    raise NotImplementedError


def max_window_rate(entries: list[dict], window_size: int) -> tuple[int, float]:
    """
    Return (index, rate) for the single highest value produced by
    rolling_error_rate(entries, window_size). If multiple positions tie
    for the highest rate, return the earliest (smallest index) one.

    TODO: implement this function.
    """
    raise NotImplementedError


# Known-correct rates, used to test first_breach independently of
# whether rolling_error_rate is actually right - so a bug in one
# function doesn't make an unrelated function's checks look broken too.
EXPECTED_RATES = [0.0, 0.0, 0.33, 0.5, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25]


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
    except NotImplementedError:
        not_implemented("rolling_error_rate", 1)

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
    except NotImplementedError:
        not_implemented("first_breach", 2)

    try:
        check(
            "max_window_rate",
            max_window_rate(ENTRIES, window_size=4) == (5, 0.75),
            f"unexpected max_window_rate: {max_window_rate(ENTRIES, window_size=4)}",
        )
    except NotImplementedError:
        not_implemented("max_window_rate", 1)

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
