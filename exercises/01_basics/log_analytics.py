"""
Real-world scenario
--------------------
Part II of the log cleanup job. Ops liked the structured summaries from
messy_log_cleanup.py enough that they now want a small analytics layer on
top: parse a whole batch of raw lines at once (tolerating malformed ones
instead of crashing), group entries by service, and surface which
services are having the worst day.

This builds directly on 01_basics/messy_log_cleanup.py, but instead of
one clean line at a time, the input batch is realistically messy: some
lines are missing fields, some are blank, and at least one message
contains the "|" delimiter character itself.

Skills practiced: dict/list comprehensions, grouping into nested
structures, defensive parsing with str.split(maxsplit=...), sorting with
a custom key function.

Run this file directly to see your output and self-check results:
    python log_analytics.py
"""

RAW_LOGS_V2 = [
    "2026-07-29T08:01:00 | ERROR | payment-service | charge failed: card_declined",
    "2026-07-29T08:01:15 | ERROR | payment-service | charge failed: insufficient_funds",
    "2026-07-29T08:02:00 | INFO | payment-service | charge succeeded: order=5521",
    "2026-07-29T08:03:00 | ERROR | auth-service | login failed: bad_password",
    "2026-07-29T08:03:30 | INFO | auth-service | user 7734 logged in",
    "2026-07-29T08:04:00 | INFO | auth-service | user 9981 logged in",
    "2026-07-29T08:05:00 | WARNING | inventory-service | low stock: sku=B110 qty=1",
    "2026-07-29T08:05:45 | ERROR | inventory-service | sync failed: timeout | retry_count=3",
    "2026-07-29T08:06:00 | ERROR | shipping-service",
    "   ",
    "2026-07-29T08:07:00 | INFO | billing-service | invoice sent: inv_2201",
]


def parse_logs(raw_lines: list[str]) -> list[dict]:
    """
    Parse a batch of raw log lines into a list of parsed dicts, each with
    keys "timestamp", "level", "service", "message" (same shape as
    Part I).

    Two things Part I's single-line parser didn't have to handle:

    1. A line's message may itself contain a "|" character (see the
       inventory-service ERROR line above). Splitting naively would chop
       the message short. Look at the `maxsplit` argument to str.split().

    2. Some lines are malformed: missing one or more fields, or blank/
       whitespace-only. These should be silently skipped, not raise an
       error and not appear in the returned list.

    TODO: implement this function.
    """
    keys = ["timestamp", "level", "service", "message"]
    parsedLogs = []

    for line in raw_lines:
        log = {}
        lineSplits = line.strip().split("|",3)
        if len(lineSplits) == 4:
            for i in range(0,len(lineSplits)):
                log[keys[i]] = lineSplits[i].strip()
            parsedLogs.append(log)

    return parsedLogs


def group_by_service(entries: list[dict]) -> dict[str, list[dict]]:
    """
    Group parsed entries by their "service" field.

    Returns a dict mapping service name -> list of that service's entries
    (in their original relative order), e.g.:
        {"payment-service": [entry, entry, ...], "auth-service": [...]}

    TODO: implement this function.
    """
    groupedEntries = {}

    for entry in entries:
        if entry['service'] not in groupedEntries:
            groupedEntries[entry['service']] = [entry]
        else:
            groupedEntries[entry['service']].append(entry)

    return groupedEntries


def error_rate_by_service(entries: list[dict]) -> dict[str, float]:
    """
    For each service, compute the fraction of its entries that are
    level == "ERROR", rounded to 2 decimal places.

    e.g. {"payment-service": 0.67, "auth-service": 0.33, ...}

    TODO: implement this function.
    """
    serviceCount = {}


    #



    # service count , error count 
    # count the errors for each service and divide by total number of ERROR logs 
    for entry in entries:
        if entry["service"] not in serviceCount:
            count = { "errors" : 0 , "total" : 0}
            serviceCount[entry["service"]] = count
            if entry["level"] == "ERROR":
                serviceCount[entry["service"]]['errors'] = 1
            
            serviceCount[entry["service"]]['total']  = 1
        else:
            if entry["level"] == "ERROR":
                serviceCount[entry["service"]]['errors'] += 1
                serviceCount[entry["service"]]['total']  += 1
            else:
                serviceCount[entry["service"]]['total']  += 1

    error_percentage = {}

    for service in serviceCount:
        error_percentage[service] = round(serviceCount[service]['errors'] / serviceCount[service]['total'],2)

    return error_percentage

def error_by_service(entries: list[dict]) -> dict:
    serviceCount = {}

    for entry in entries:
        if entry["service"] not in serviceCount:
            count = { "errors" : 0 , "total" : 0}
            serviceCount[entry["service"]] = count
            if entry["level"] == "ERROR":
                serviceCount[entry["service"]]['errors'] = 1
            
            serviceCount[entry["service"]]['total']  = 1
        else:
            if entry["level"] == "ERROR":
                serviceCount[entry["service"]]['errors'] += 1
                serviceCount[entry["service"]]['total']  += 1
            else:
                serviceCount[entry["service"]]['total']  += 1
    return serviceCount

def top_error_services(entries: list[dict], n: int) -> list[str]:
    """
    Return the names of the n services with the most ERROR-level entries,
    ordered by error count descending. Break ties alphabetically by
    service name. Services with zero errors are never included, even if
    that means returning fewer than n names.

    TODO: implement this function.
    """
    counts = error_by_service(entries)
    errorcounts = {}

    for count in counts:
        if counts[count]['errors'] != 0:
            errorcounts[count] = counts[count]['errors']

    soredErrorServices = sorted(errorcounts, key=lambda k: (-errorcounts[k],k))

    return soredErrorServices[:n]


def _self_check() -> None:
    entries = parse_logs(RAW_LOGS_V2)

    assert len(entries) == 9, (
        f"expected 9 valid entries (2 of the 11 raw lines are malformed), got {len(entries)}"
    )

    tricky = next(
        e for e in entries if e["service"] == "inventory-service" and e["level"] == "ERROR"
    )
    assert tricky["message"] == "sync failed: timeout | retry_count=3", (
        f"message containing '|' should stay intact, got: {tricky['message']!r}"
    )

    groups = group_by_service(entries)
    assert {k: len(v) for k, v in groups.items()} == {
        "payment-service": 3,
        "auth-service": 3,
        "inventory-service": 2,
        "billing-service": 1,
    }, "unexpected group sizes: {k: len(v) for k, v in groups.items()}"

    rates = error_rate_by_service(entries)
    assert rates == {
        "payment-service": 0.67,
        "auth-service": 0.33,
        "inventory-service": 0.5,
        "billing-service": 0.0,
    }, f"unexpected error rates: {rates}"

    assert top_error_services(entries, 2) == ["payment-service", "auth-service"], (
        f"unexpected top 2: {top_error_services(entries, 2)}"
    )
    top_5 = top_error_services(entries, 5)
    assert top_5 == ["payment-service", "auth-service", "inventory-service"], (
        f"unexpected top 5 (billing-service has 0 errors, should be excluded): {top_5}"
    )

    print("All checks passed.")
    print(f"Error rates: {rates}")


if __name__ == "__main__":
    _self_check()
