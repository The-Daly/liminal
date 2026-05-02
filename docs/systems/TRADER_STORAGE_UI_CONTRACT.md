# Trader And Storage UI Contract

This defines the extraction-style inventory UX for V0.1. It should feel familiar to extraction-game players without copying Tarkov visuals or exact layout.

## Trader UI

Layout:

- Left panel: trader identity, stock list, item details.
- Center/action area: selected item, quantity stepper, buy/sell/inspect controls.
- Right panel: player carried inventory and personal storage tabs.
- Header: Movie Ticket balance, trader name, current location.

Required actions:

- Buy item.
- Sell item.
- Inspect item.
- Split stack.
- Quick-transfer between carried inventory and storage.

V0.1 trader:

- **The Turnstile** sells survival basics and expensive rare early combat gear.
- Weapons and armor are not starter defaults; the trader can sell them only after the player finds tickets.

## Storage UI

Layout:

- Left panel: personal storage grid.
- Right panel: carried inventory grid.
- Bottom/details area: selected item stats, weight, value, category, rarity.
- Top filters: All, Consumable, Tool, Resource, Ammo, Weapon, Armor, Relic.

Required actions:

- Move item.
- Quick-transfer.
- Split/merge stack.
- Inspect item.
- Sort by category/value/weight.

## Visual Direction

- Dense, utilitarian, readable.
- Worn ticket-machine UI language.
- No direct Tarkov visual copying.
- No oversized marketing-style panels.
- The UI should support repeated actions quickly.
