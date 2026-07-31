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


def _self_check() -> None:
    rates = rolling_error_rate(ENTRIES, window_size=4)
    assert rates == [0.0, 0.0, 0.33, 0.5, 0.5, 0.75, 0.5, 0.25, 0.5, 0.25], f"unexpected rates: {rates}"

    assert first_breach(rates, 0.5) == 3, f"unexpected first_breach(rates, 0.5): {first_breach(rates, 0.5)}"
    assert first_breach(rates, 0.9) is None, (
        f"no rate ever reaches 0.9, expected None, got {first_breach(rates, 0.9)}"
    )

    assert max_window_rate(ENTRIES, window_size=4) == (5, 0.75), (
        f"unexpected max_window_rate: {max_window_rate(ENTRIES, window_size=4)}"
    )

    print("All checks passed.")
    print(f"Rolling rates: {rates}")


if __name__ == "__main__":
    _self_check()
