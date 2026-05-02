#!/usr/bin/env python3
from inventory_model import InventoryContainer, InventoryError
from item_registry import DataRegistry, RegistryError, load_registry

CURRENCY_ITEM_ID = "currency_old_movie_ticket"


def find_stock(registry: DataRegistry, trader_id: str, item_id: str) -> dict:
    trader = registry.traders.get(trader_id)
    if trader is None:
        raise RegistryError(f"Unknown trader_id: {trader_id}")
    for stock in trader.get("stock", []):
        if stock["item_id"] == item_id:
            return stock
    raise RegistryError(f"Trader {trader_id} does not stock {item_id}")


def can_buy(registry: DataRegistry, trader_id: str, item_id: str, quantity: int, inventory: InventoryContainer) -> bool:
    if quantity <= 0:
        return False
    stock = find_stock(registry, trader_id, item_id)
    if quantity > stock.get("max_quantity", quantity):
        return False
    return inventory.quantity(CURRENCY_ITEM_ID) >= stock["price_tickets"] * quantity


def buy_item(registry: DataRegistry, trader_id: str, item_id: str, quantity: int, inventory: InventoryContainer) -> None:
    if not can_buy(registry, trader_id, item_id, quantity, inventory):
        raise InventoryError("Cannot complete purchase")
    stock = find_stock(registry, trader_id, item_id)
    inventory.remove_item(CURRENCY_ITEM_ID, stock["price_tickets"] * quantity)
    inventory.add_item(registry, item_id, quantity)


def sell_preview(registry: DataRegistry, item_id: str, quantity: int) -> int:
    if quantity <= 0:
        return 0
    item = registry.item(item_id)
    if item_id == CURRENCY_ITEM_ID:
        return 0
    return int(item.get("value_tickets", 0)) * quantity


def main() -> None:
    registry = load_registry()
    trader_id = "trader_the_turnstile_v0"
    print(f"{trader_id}: {len(registry.traders[trader_id]['stock'])} stock entries")


if __name__ == "__main__":
    main()
