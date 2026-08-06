"""
Real-world scenario
--------------------
Ops wants a lightweight in-process monitor that watches a stream of log
lines *as they arrive* and raises an alert the moment a service's rolling
error rate crosses a threshold - instead of waiting for a full batch
report like log_analytics.py (exercises/01_basics/) produces.

This is a project skeleton, not a scaffolded exercise: the signatures and
docstrings below are a starting point, not a fixed contract. Change them
however makes sense. See README.md in this folder for a suggested
approach and stretch goals.

Skills to practice: generators (`yield`), `collections.deque` for a
fixed-size sliding window, maintaining running state across a stream.
"""

from collections import deque

RAW_LOGS = [
    "2026-07-29T09:00:00 | INFO | payment-service | charge succeeded: order=1001",
    "2026-07-29T09:00:05 | INFO | auth-service | user 3310 logged in",
    "2026-07-29T09:00:10 | ERROR | payment-service | charge failed: card_declined",
    "2026-07-29T09:00:15 | INFO | auth-service | user 5521 logged in",
    "2026-07-29T09:00:20 | ERROR | payment-service | charge failed: timeout",
    "2026-07-29T09:00:25 | INFO | auth-service | user 8834 logged in",
    "2026-07-29T09:00:30 | ERROR | payment-service | charge failed: insufficient_funds",
    "2026-07-29T09:00:35 | ERROR | auth-service | login failed: bad_password",
    "2026-07-29T09:00:40 | INFO | payment-service | charge succeeded: order=1002",
    "2026-07-29T09:00:45 | ERROR | auth-service | login failed: bad_password",
    "2026-07-29T09:00:50 | ERROR | auth-service | login failed: account_locked",
]


def parse_line(line: str) -> dict | None:
    """
    Parse one raw "timestamp | level | service | message" line into a
    dict, or None if the line is malformed.

    Already implemented - this bit isn't the point of this project,
    reuse it freely.
    """
    parts = line.strip().split("|", 3)
    if len(parts) != 4:
        return None
    timestamp, level, service, message = (p.strip() for p in parts)
    return {"timestamp": timestamp, "level": level, "service": service, "message": message}


def stream_logs(raw_lines: list[str]):
    """
    A generator that yields parsed log entries one at a time, skipping
    malformed lines.

    This is where "streaming" starts: callers pull entries lazily
    instead of getting a full list up front.
    """


def rolling_error_rate(stream, window_size: int):
    """
    Consume `stream` (an iterable of parsed entries) and yield
    (entry, current_rate) pairs, where current_rate is that entry's
    service's ERROR rate over its most recent `window_size` entries
    for that service (including this one).

    Hint: collections.deque(maxlen=window_size) gives you a fixed-size
    window that automatically drops the oldest item once full. You'll
    want one deque per service.
    """


def find_alerts(stream, window_size: int, threshold: float) -> list[tuple[str, int, float]]:
    """
    Return a list of (service, position, rate) tuples for every entry
    where that service's rolling error rate is >= threshold.
    `position` is the 0-based index of that entry within its own
    service's stream (not the overall stream).
    """


if __name__ == "__main__":
    # Manual demo, not an assert-based self-check. Run this file and
    # compare the printed alerts against what you'd expect from reading
    # RAW_LOGS yourself.
    stream = stream_logs(RAW_LOGS)
    alerts = find_alerts(stream, window_size=3, threshold=0.66)
    for service, position, rate in alerts:
        print(f"ALERT: {service} error rate {rate:.2f} at position {position}")
