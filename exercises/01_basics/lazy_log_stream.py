"""
Real-world scenario
--------------------
log_analytics.py (Part II) reads a whole batch of log lines into memory
before doing anything with them. That's fine for a small batch, but ops
now has a log source that's effectively endless (a live tail, or a file
too big to load at once). They want processing that pulls lines one at a
time and can stop early - never materializing more of the stream than it
actually needs.

Skills practiced: generators (`yield`), lazy iteration, composing
generators, stopping consumption early.

Run this file directly to see your output and self-check results:
    python lazy_log_stream.py
"""

RAW_LOGS_LARGE = [
    "2026-07-29T10:00:00 | INFO | payment-service | charge succeeded: order=2001",
    "2026-07-29T10:00:05 | INFO | auth-service | user 1123 logged in",
    "2026-07-29T10:00:10 | ERROR | payment-service | charge failed: card_declined",
    "2026-07-29T10:00:15 | INFO | auth-service | user 4471 logged in",
    "2026-07-29T10:00:20 | ERROR | inventory-service | sync failed: timeout",
    "2026-07-29T10:00:25 | INFO | payment-service | charge succeeded: order=2002",
    "2026-07-29T10:00:30 | WARNING | inventory-service | low stock: sku=C220 qty=4",
    "2026-07-29T10:00:35 | INFO | auth-service | user 8821 logged in",
    "2026-07-29T10:00:40 | ERROR | shipping-service | label print failed",
    "2026-07-29T10:00:45 | INFO | billing-service | invoice sent: inv_3301",
    "2026-07-29T10:00:50 | ERROR | payment-service | charge failed: timeout",
    "2026-07-29T10:00:55 | INFO | auth-service | user 9981 logged in",
]


def parse_line(line: str) -> dict | None:
    """
    Parse one raw "timestamp | level | service | message" line into a
    dict, or None if the line doesn't have all 4 fields.

    Already implemented - reuse it, parsing isn't the point of this one.
    """
    parts = line.strip().split("|", 3)
    if len(parts) != 4:
        return None
    timestamp, level, service, message = (p.strip() for p in parts)
    return {"timestamp": timestamp, "level": level, "service": service, "message": message}


def stream_entries(raw_lines):
    """
    A generator that yields parsed entries one at a time from
    `raw_lines`, skipping any line that fails to parse.

    The important part: this must be a generator (use `yield`), not a
    function that builds a list internally and returns it. A caller
    should be able to pull just the first few items without this
    function having processed the rest of `raw_lines` yet.

    TODO: implement this function.
    """
    raise NotImplementedError


def filter_by_level(stream, level: str):
    """
    A generator that yields only the entries from `stream` whose
    "level" matches `level`, preserving order.

    `stream` is any iterable (e.g. the output of stream_entries) - don't
    assume it's a list, and don't convert it to one.

    TODO: implement this function.
    """
    raise NotImplementedError


def take(stream, n: int) -> list:
    """
    Pull at most `n` items from `stream` and return them as a list. If
    the stream has fewer than `n` items, return however many there are.

    Must not pull more than `n` items from `stream` - anything after the
    nth item should remain unconsumed.

    TODO: implement this function.
    """
    raise NotImplementedError


def _self_check() -> None:
    entries = list(stream_entries(RAW_LOGS_LARGE))
    assert len(entries) == 12, f"expected all 12 well-formed lines to parse, got {len(entries)}"
    assert entries[0]["service"] == "payment-service", f"unexpected first entry: {entries[0]}"

    errors_only = list(filter_by_level(stream_entries(RAW_LOGS_LARGE), "ERROR"))
    assert len(errors_only) == 4, f"expected 4 ERROR entries, got {len(errors_only)}"
    assert all(e["level"] == "ERROR" for e in errors_only), "filter_by_level let a non-ERROR entry through"

    first_two_errors = take(filter_by_level(stream_entries(RAW_LOGS_LARGE), "ERROR"), 2)
    assert [e["service"] for e in first_two_errors] == ["payment-service", "inventory-service"], (
        f"unexpected first two errors: {first_two_errors}"
    )

    # The real point of this exercise: laziness. If stream_entries or
    # filter_by_level secretly build a full list before yielding
    # anything, `take(..., 2)` will have pulled every line from the raw
    # source even though it only needed the first few.
    pull_count = {"n": 0}

    def counting_lines():
        for line in RAW_LOGS_LARGE:
            pull_count["n"] += 1
            yield line

    lazy_errors = filter_by_level(stream_entries(counting_lines()), "ERROR")
    take(lazy_errors, 2)
    assert pull_count["n"] < len(RAW_LOGS_LARGE), (
        f"take(stream, 2) pulled all {pull_count['n']} lines from the source - "
        "stream_entries/filter_by_level must be lazy generators, not list-builders"
    )

    print("All checks passed.")
    print(f"Pulled only {pull_count['n']} of {len(RAW_LOGS_LARGE)} lines to find the first 2 errors.")


if __name__ == "__main__":
    _self_check()
