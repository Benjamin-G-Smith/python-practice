"""
Real-world scenario
--------------------
You've inherited a server that writes messy, inconsistent log lines.
Ops wants a script that turns them into clean, structured summaries
before they get shipped to a monitoring dashboard.

Skills practiced: strings, slicing, split/strip, f-strings, conditionals,
loops, basic aggregation.

Run this file directly to see your output and self-check results:
    python messy_log_cleanup.py
"""

RAW_LOGS = [
    "2026-07-28T09:12:03 | ERROR | payment-service | charge failed: card_declined",
    "2026-07-28T09:12:05  |INFO|  auth-service|user 4471 logged in",
    "2026-07-28T09:13:41 | WARNING |inventory-service|  low stock: sku=A203 qty=2",
    "2026-07-28T09:14:02 | ERROR| payment-service |charge failed: timeout",
    "2026-07-28T09:15:10 | INFO | auth-service | user 8821 logged in",
    "  2026-07-28T09:16:47|ERROR|shipping-service|label print failed  ",
]


def parse_log_line(line: str) -> dict:
    """
    Parse one raw log line into a dict with keys:
    "timestamp", "level", "service", "message".

    The raw lines are inconsistently spaced around the "|" separators
    and may have leading/trailing whitespace. Your parsed values should
    be clean (no extra spaces).

    TODO: implement this function.
    Hint: line.strip().split("|"), then .strip() each piece.

    ParsedLogs = [
        log1 = {
            "timestamp" : "2026-07-28T09:12:03",
            "level" : "ERROR",
            "service" : "payment-service",
            "message" : "charge failed: card_declined"
        }
    
    ]
    """
    parsed_log = {}
    if line == None:
        return {}
    
    keys = ["timestamp","level","service","message"]
    linesplits = line.strip().split("|")

    # assumes that there are always 4 components 
    
    parsed_log["timestamp"] = linesplits[0].strip()
    parsed_log["level"] = linesplits[1].strip()
    parsed_log["service"] = linesplits[2].strip()
    parsed_log["message"] = linesplits[3].strip()
    return parsed_log



def count_by_level(entries: list[dict]) -> dict:
    """
    Given a list of parsed entries, return a dict mapping
    level -> count, e.g. {"ERROR": 3, "INFO": 2, "WARNING": 1}.

    TODO: implement this function.
    """
    levelCounts = {}

    for log in entries:
        levelCounts[log["level"]] = levelCounts.get(log["level"],0) + 1

    return levelCounts



def errors_for_service(entries: list[dict], service: str) -> list[str]:
    """
    Return the list of error messages (just the "message" field)
    for the given service, level == "ERROR" only.

    TODO: implement this function.
    """
    error_messages = []
    for log in entries:
        if log["service"] == service and log["level"] == "ERROR":
            error_messages.append(log["message"])
    return error_messages


def _self_check() -> None:
    entries = [parse_log_line(line) for line in RAW_LOGS]

    assert entries[0] == {
        "timestamp": "2026-07-28T09:12:03",
        "level": "ERROR",
        "service": "payment-service",
        "message": "charge failed: card_declined",
    }, f"unexpected parse: {entries[0]}"

    counts = count_by_level(entries)
    assert counts == {"ERROR": 3, "INFO": 2, "WARNING": 1}, f"unexpected counts: {counts}"

    payment_errors = errors_for_service(entries, "payment-service")
    assert payment_errors == [
        "charge failed: card_declined",
        "charge failed: timeout",
    ], f"unexpected errors: {payment_errors}"

    # Edge case: empty input
    assert count_by_level([]) == {}, "count_by_level should return {} for no entries"
    assert errors_for_service([], "payment-service") == [], (
        "errors_for_service should return [] for no entries"
    )

    # Edge case: service exists but has zero ERROR entries
    assert errors_for_service(entries, "auth-service") == [], (
        "auth-service has no ERROR-level entries, should return []"
    )

    # Edge case: service that never appears in the data at all
    assert errors_for_service(entries, "nonexistent-service") == [], (
        "unknown service should return [], not raise"
    )

    # Edge case: message field itself contains a "|" character.
    # Naive line.split("|") will produce MORE than 4 pieces here, so
    # this checks whether parse_log_line still isolates the message
    # correctly instead of silently truncating it.
    tricky = parse_log_line(
        "2026-07-28T09:20:00 | ERROR | billing-service | rate limit exceeded | retry_after=30"
    )
    print(f"Tricky pipe-in-message parse: {tricky}")

    print("All checks passed.")
    print(f"Level counts: {counts}")


if __name__ == "__main__":
    _self_check()
