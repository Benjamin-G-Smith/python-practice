"""
Real-world scenario
--------------------
A partner sends you a sales export every week. It's never quite clean:
missing quantities, non-numeric prices, the occasional negative quantity
from a data entry error. You need an importer that skips bad rows
without crashing, logs what it skipped, and reports clean totals.

Data file: data/sales.csv (7 rows, 3 of them are bad on purpose)

Skills practiced: file I/O, the csv module, try/except, input validation,
returning multiple pieces of information from one function.

Run this file directly to see your output and self-check results:
    python csv_import.py
"""

import csv
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "sales.csv"


def load_sales(path: Path) -> tuple[list[dict], list[str]]:
    """
    Read the CSV at `path` and return a tuple: (good_rows, skipped_reasons).

    good_rows: list of dicts like
        {"order_id": "1001", "product": "Ceramic mug", "quantity": 3, "unit_price": 12.5}
    quantity and unit_price should be converted to int/float.

    A row is invalid (and should go to skipped_reasons instead, as a
    human-readable string like "row 1004: invalid unit_price 'twenty-two'")
    if:
      - quantity is missing/blank, OR
      - quantity or unit_price can't be converted to a number, OR
      - quantity is <= 0

    TODO: implement this function.
    Hint: csv.DictReader(f) gives you one dict per row (all values are
    strings). Wrap the numeric conversion in try/except ValueError.
    """
    raise NotImplementedError


def total_revenue(rows: list[dict]) -> float:
    """
    Return sum(quantity * unit_price) across all rows, rounded to 2 places.

    TODO: implement this function.
    """
    raise NotImplementedError


def _self_check() -> None:
    good_rows, skipped = load_sales(DATA_PATH)

    assert len(good_rows) == 4, f"expected 4 good rows, got {len(good_rows)}: {good_rows}"
    assert len(skipped) == 3, f"expected 3 skipped rows, got {len(skipped)}: {skipped}"

    order_ids = {row["order_id"] for row in good_rows}
    assert order_ids == {"1001", "1002", "1005", "1007"}, f"unexpected good order_ids: {order_ids}"

    revenue = total_revenue(good_rows)
    assert revenue == 190.50, f"unexpected revenue: {revenue}"

    print("All checks passed.")
    print(f"Imported {len(good_rows)} rows, skipped {len(skipped)}")
    for reason in skipped:
        print(f"  skipped: {reason}")
    print(f"Total revenue: ${revenue:.2f}")


if __name__ == "__main__":
    _self_check()
