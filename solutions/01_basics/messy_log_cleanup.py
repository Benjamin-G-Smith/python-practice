"""Solution for exercises/01_basics/messy_log_cleanup.py"""

RAW_LOGS = [
    "2026-07-28T09:12:03 | ERROR | payment-service | charge failed: card_declined",
    "2026-07-28T09:12:05  |INFO|  auth-service|user 4471 logged in",
    "2026-07-28T09:13:41 | WARNING |inventory-service|  low stock: sku=A203 qty=2",
    "2026-07-28T09:14:02 | ERROR| payment-service |charge failed: timeout",
    "2026-07-28T09:15:10 | INFO | auth-service | user 8821 logged in",
    "  2026-07-28T09:16:47|ERROR|shipping-service|label print failed  ",
]


def parse_log_line(line: str) -> dict:
    timestamp, level, service, message = line.strip().split("|")
    return {
        "timestamp": timestamp.strip(),
        "level": level.strip(),
        "service": service.strip(),
        "message": message.strip(),
    }


def count_by_level(entries: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for entry in entries:
        level = entry["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def errors_for_service(entries: list[dict], service: str) -> list[str]:
    return [
        entry["message"]
        for entry in entries
        if entry["service"] == service and entry["level"] == "ERROR"
    ]


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

    print("All checks passed.")
    print(f"Level counts: {counts}")


if __name__ == "__main__":
    _self_check()
