# Master NPC Roster

This document tracks memorable NPCs for Liminal Dominion. It connects the roster to Backrooms-style lore patterns while keeping all names, personalities, services, quests, and dialogue original.

## Lore Boundary

Use public Backrooms wiki ideas only as high-level inspiration:

- faction survival culture: M.E.G. archive/research, B.N.T.G. trade/supply, and route-runner/scout culture
- liminal survival staples: Almond Water, unsafe transitions, service corridors, entity documentation, and outpost life
- level structure inspiration: Level 1-style service/utility spaces, storage corridors, supply points, and unstable routes

Do not copy canon NPCs, canon questlines, exact outpost names, wiki prose, logos, or protected fan-specific details. Liminal Dominion NPCs should feel like they belong in our world first.

Reference pages checked for high-level lore alignment:

- Backrooms Wikidot Level 1: https://backrooms-wiki.wikidot.com/level-1
- Official Backrooms Wiki Level 1 overview: https://the-official-backrooms.fandom.com/wiki/Level_1
- Archived B.N.T.G. overview: https://backrooms-wiki.wikidot.com/archived%3Ab-n-t-g

## Roster Rules

- Every NPC needs a name players can remember after one meeting.
- Every trader needs a reason to exist in the economy.
- Every quest giver should teach a system or reveal a route.
- Security NPCs must respect the no-team-kill rule.
- Security hiring is faction-safe: hired guards do not enable same-faction griefing.
- Squads are smaller groups inside a faction; NPC radio services should reinforce squad identity.

## V0.1 Anchors

| NPC | Role | Purpose |
|---|---|---|
| Marrow Vell | Quartermaster / quest giver | First five quests and survival onboarding |
| The Turnstile | Ticket trader | Movie Ticket economy and survival purchases |
| Rook Twine | Clippers route mentor | Trail String and hidden route language |
| Milo Pawnlight | Security broker | Future paid guard contracts |
| Maud Static | Radio technician | Squad radio identity and interference quests |

## Master Roster

| # | Name | Faction | Primary Function | Services | Security Function | Lore Connection |
|---:|---|---|---|---|---|---|
| 1 | Marrow Vell | M.E.G. | Quest giver | quests, storage, mapping | can hire security | M.E.G. archive culture, Almond Water survival, Level 1 corridors |
| 2 | The Turnstile | B.N.T.G. | Trader | buy, sell, repair | can hire security | Movie Tickets, trade culture, supply outposts |
| 3 | Sera Latch | M.E.G. | Hybrid | quests, medical, training | can fight | sanity, Almond Water, entity documentation |
| 4 | Orin Mapwake | M.E.G. | Quest giver | quests, mapping, radio | non-combat | no-clip transitions, route logging |
| 5 | June Brightwire | M.E.G. | Trader | radio, repair, buy/sell | non-combat | comms, scanners, entity reports |
| 6 | Voss Halden | M.E.G. | Security | patrol, training | hireable guard | hub defense, entity drills |
| 7 | Cass Bracket | B.N.T.G. | Trader | crafting, buy/sell | non-combat | scrap, ammo parts, supply corridors |
| 8 | Iva Lockgrail | B.N.T.G. | Quest giver | quests, storage, security hire | can hire security | locked crates, supply recovery |
| 9 | Bram Fusewick | B.N.T.G. | Hybrid | ammo crafting, repair, trader | can fight | crude ammo and noisy weapons |
| 10 | Milo Pawnlight | B.N.T.G. | Security broker | security hire, buy/sell | can hire security | Movie Ticket contracts |
| 11 | Tessa Rivet | B.N.T.G. | Security | patrol, hire, training | hireable guard | market gate defense |
| 12 | Rook Twine | Clippers | Quest giver | quests, mapping, training | can fight | Trail String, shortcuts, route walls |
| 13 | Veya Skipjack | Clippers | Trader | navigation buy/sell | non-combat | route tools and expiring maps |
| 14 | Hollis Camber | Clippers | Hybrid | quests, radio, training | hireable scout | camcorder proof and return routes |
| 15 | Dax Understep | Clippers | Security | patrol, hire | hireable guard | shortcut overwatch |
| 16 | Noma Reel | Clippers | Trader | repair, buy/sell | non-combat | camcorder repair and battery supply |
| 17 | Harlan Nightdesk | Neutral | Security broker | security hire, storage | can hire security | safe-room settlement contracts |
| 18 | Maud Static | Neutral | Hybrid | radio, quests, repair | non-combat | squad comms and interference |
| 19 | Ozra Candle | Neutral | Trader | medical, buy/sell | non-combat | Almond Water and emergency supplies |
| 20 | Calder Bellmark | Neutral | Security | patrol, hire, training | hireable guard | close-quarters survival |
| 21 | Elian Palecheck | Neutral | Quest giver | quests, mapping, storage | can hire security | lost items and return paths |

## Security And Hiring Notes

Security NPCs should not become disposable weapons for griefing. When implemented:

- A hired guard follows the hirer's squad rules.
- A hired guard cannot damage same-faction players.
- A hired guard prioritizes entities, opposing faction threats, and escort objectives.
- Security brokers sell contracts, not permanent NPC ownership.
- Security should be expensive enough that stealth remains the early-game default.

## Data Source

- `data/seed/npc_roster.seed.json`
- `data/schemas/npc_roster.schema.json`
- `scripts/npc_roster_model.py`
