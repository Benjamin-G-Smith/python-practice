"""Solution for exercises/04_files_and_errors/csv_import.py"""

import csv
from pathlib import Path

DATA_PATH = (
    Path(__file__).parent.parent.parent / "exercises" / "04_files_and_errors" / "data" / "sales.csv"
)


def load_sales(path: Path) -> tuple[list[dict], list[str]]:
    good_rows = []
    skipped_reasons = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id = row["order_id"]
            raw_qty = row["quantity"]
            raw_price = row["unit_price"]

            if not raw_qty.strip():
                skipped_reasons.append(f"row {order_id}: missing quantity")
                continue

            try:
                quantity = int(raw_qty)
            except ValueError:
                skipped_reasons.append(f"row {order_id}: invalid quantity {raw_qty!r}")
                continue

            try:
                unit_price = float(raw_price)
            except ValueError:
                skipped_reasons.append(f"row {order_id}: invalid unit_price {raw_price!r}")
                continue

            if quantity <= 0:
                skipped_reasons.append(f"row {order_id}: non-positive quantity {quantity}")
                continue

            good_rows.append({
                "order_id": order_id,
                "product": row["product"],
                "quantity": quantity,
                "unit_price": unit_price,
            })

    return good_rows, skipped_reasons


def total_revenue(rows: list[dict]) -> float:
    return round(sum(row["quantity"] * row["unit_price"] for row in rows), 2)


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
