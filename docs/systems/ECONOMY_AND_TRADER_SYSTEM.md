# Economy And Trader System

## V0.1 Purpose

Movie Tickets are the prototype currency. The first trader proves buy/sell interaction without building a full economy.

## Data Source

- `data/seed/items.seed.json`
- `data/seed/traders.seed.json`

## V0.1 Trader

The Broken Trader Kiosk sells survival basics:

- Almond Water
- Battery Pack
- Chalk Bundle

The trader can buy simple loot/resources:

- Movie Tickets are currency, not sold back.
- Scrap and batteries can be valued through item `value_tickets`.
- Relics keep high value but full relic economy is deferred.

## Runtime Contract

- Buy price comes from trader stock, not direct item value.
- Player must have enough `currency_old_movie_ticket`.
- Purchase removes tickets and adds the purchased item.
- Sell flow may use item `value_tickets`.
- No dynamic market/inflation in V0.1.

## Prototype

Use `scripts/economy_model.py` for buy checks and transaction simulation.
