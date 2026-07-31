"""
Real-world scenario
--------------------
Finance handed you a raw list of expense transactions and wants a
monthly report: totals by category, a flagged list of large purchases,
and a reusable tax calculator for reimbursements.

Skills practiced: functions, default args, *args/**kwargs, filtering,
aggregation with functions instead of top-level scripts.

Run this file directly to see your output and self-check results:
    python expense_report.py
"""

TRANSACTIONS = [
    {"category": "travel", "amount": 412.50, "vendor": "Delta"},
    {"category": "meals", "amount": 38.20, "vendor": "Cafe Luna"},
    {"category": "software", "amount": 29.00, "vendor": "Figma"},
    {"category": "travel", "amount": 156.00, "vendor": "Marriott"},
    {"category": "meals", "amount": 12.75, "vendor": "Subway"},
    {"category": "software", "amount": 1200.00, "vendor": "Adobe"},
    {"category": "office", "amount": 64.99, "vendor": "Staples"},
]


def total_by_category(transactions: list[dict]) -> dict:
    """
    Return a dict mapping category -> total amount spent, rounded to 2
    decimal places.

    TODO: implement this function.
    """
    raise NotImplementedError


def flag_large_purchases(transactions: list[dict], *, threshold: float = 200.0) -> list[dict]:
    """
    Return the transactions with amount > threshold. `threshold` must be
    a keyword-only argument (note the `*` in the signature) so callers
    can't pass it positionally by mistake.

    TODO: implement this function.
    """
    raise NotImplementedError


def apply_tax(amount: float, *, rate: float = 0.0, **fees) -> float:
    """
    Return amount * (1 + rate) + sum(fees.values()), rounded to 2 decimals.
    `fees` lets callers pass arbitrary named surcharges, e.g.
    apply_tax(100, rate=0.08, service_fee=5, processing_fee=2.5)

    TODO: implement this function.
    """
    raise NotImplementedError


def _self_check() -> None:
    totals = total_by_category(TRANSACTIONS)
    assert totals == {
        "travel": 568.50,
        "meals": 50.95,
        "software": 1229.00,
        "office": 64.99,
    }, f"unexpected totals: {totals}"

    large = flag_large_purchases(TRANSACTIONS, threshold=200.0)
    vendors = sorted(t["vendor"] for t in large)
    assert vendors == ["Adobe", "Delta"], f"unexpected flagged vendors: {vendors}"

    taxed = apply_tax(100, rate=0.08, service_fee=5, processing_fee=2.5)
    assert taxed == 115.50, f"unexpected taxed amount: {taxed}"

    plain = apply_tax(50)
    assert plain == 50.00, f"unexpected plain amount: {plain}"

    print("All checks passed.")
    print(f"Totals by category: {totals}")
    print(f"Large purchases: {vendors}")


if __name__ == "__main__":
    _self_check()
