"""
Real-world scenario
--------------------
You're building the backend logic for a small shop's inventory system.
Products come in as a list of dicts; you need to answer common business
questions: what's low on stock, what's the total value on hand, and how
to apply a bulk restock.

Skills practiced: dicts, lists, comprehensions, sorting, nested data.

Run this file directly to see your output and self-check results:
    python inventory_manager.py
"""

INVENTORY = [
    {"sku": "A203", "name": "Ceramic mug", "qty": 4, "price": 12.50},
    {"sku": "B117", "name": "Steel water bottle", "qty": 22, "price": 18.00},
    {"sku": "C044", "name": "Canvas tote bag", "qty": 2, "price": 15.00},
    {"sku": "D310", "name": "Wool beanie", "qty": 0, "price": 22.00},
    {"sku": "E501", "name": "Notebook, dot grid", "qty": 40, "price": 9.00},
]


def total_inventory_value(inventory: list[dict]) -> float:
    """
    Return the total value of all stock on hand: sum(qty * price).
    Round to 2 decimal places.

    TODO: implement this function.
    """
    raise NotImplementedError


def low_stock_items(inventory: list[dict], threshold: int = 5) -> list[str]:
    """
    Return a list of product names where qty < threshold,
    sorted alphabetically.

    TODO: implement this function.
    """
    raise NotImplementedError


def restock(inventory: list[dict], restock_map: dict[str, int]) -> list[dict]:
    """
    Given a dict mapping sku -> quantity to add, return a NEW list of
    inventory dicts with updated quantities (don't mutate the input).
    SKUs not present in restock_map are unchanged.

    TODO: implement this function.
    """
    raise NotImplementedError


def _self_check() -> None:
    total = total_inventory_value(INVENTORY)
    assert total == 836.00, f"unexpected total: {total}"

    low = low_stock_items(INVENTORY, threshold=5)
    assert low == ["Canvas tote bag", "Ceramic mug", "Wool beanie"], f"unexpected low stock: {low}"

    updated = restock(INVENTORY, {"A203": 20, "D310": 15})
    updated_by_sku = {item["sku"]: item["qty"] for item in updated}
    assert updated_by_sku["A203"] == 24, f"unexpected qty: {updated_by_sku['A203']}"
    assert updated_by_sku["D310"] == 15, f"unexpected qty: {updated_by_sku['D310']}"
    assert updated_by_sku["B117"] == 22, "unrelated item should be unchanged"
    assert INVENTORY[0]["qty"] == 4, "original inventory should not be mutated"

    print("All checks passed.")
    print(f"Total inventory value: ${total:.2f}")
    print(f"Low stock: {low}")


if __name__ == "__main__":
    _self_check()
