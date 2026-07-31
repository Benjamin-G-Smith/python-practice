"""Solution for exercises/02_data_structures/inventory_manager.py"""

INVENTORY = [
    {"sku": "A203", "name": "Ceramic mug", "qty": 4, "price": 12.50},
    {"sku": "B117", "name": "Steel water bottle", "qty": 22, "price": 18.00},
    {"sku": "C044", "name": "Canvas tote bag", "qty": 2, "price": 15.00},
    {"sku": "D310", "name": "Wool beanie", "qty": 0, "price": 22.00},
    {"sku": "E501", "name": "Notebook, dot grid", "qty": 40, "price": 9.00},
]


def total_inventory_value(inventory: list[dict]) -> float:
    return round(sum(item["qty"] * item["price"] for item in inventory), 2)


def low_stock_items(inventory: list[dict], threshold: int = 5) -> list[str]:
    names = [item["name"] for item in inventory if item["qty"] < threshold]
    return sorted(names)


def restock(inventory: list[dict], restock_map: dict[str, int]) -> list[dict]:
    updated = []
    for item in inventory:
        new_item = dict(item)
        if new_item["sku"] in restock_map:
            new_item["qty"] += restock_map[new_item["sku"]]
        updated.append(new_item)
    return updated


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
