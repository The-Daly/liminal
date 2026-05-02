# Level 1 Scale And Faction Layout

This document defines the first spatial plan for `LD_Level1_ServiceHalls_Greybox`. It turns the zone list into scale, travel-time, faction-base spacing, and route rules.

## Current Answer

Before this file, the repo only had a required-zone list. It did not yet define level size, faction-base placement, travel time, or how players get lost. This document is the first locked working layout for V0.1 graybox iteration.

## Scale Target

V0.1 should feel like a large first extraction zone: big enough for players to lose orientation, but still scoped tightly enough to graybox and test before full faction-base gameplay.

| Metric | Target |
|---|---:|
| Playable footprint | about 850m x 650m |
| Critical-path hub gate to stable extraction | 7-10 minutes cautious solo movement |
| Cross-map faction foothold to foothold | 9-14 minutes without shortcuts |
| Fast hidden-route traversal | 4-7 minutes, high disorientation risk |
| Normal run length | 18-32 minutes |
| Lost-player recovery time | 4-8 minutes after finding a landmark |

Use Unreal scale convention: `1 uu = 1 cm`, so `100 uu = 1 m`.

## Spatial Philosophy

- The map should not be a straight line.
- Players should see landmarks often enough to regain orientation, but not enough to fully map the space in one run.
- Faction footholds should sit on different route philosophies, not simply different corners.
- Shortcuts should help experts while making new players feel unsure.
- Loops are better than dead ends, except for loot-risk pockets.

## Faction Footholds

V0.1 does not include full faction bases or raids. It should include small faction-flavored footholds/objective pockets that imply future bases.

| Faction | Foothold | Placement | Function |
|---|---|---|---|
| M.E.G. | Archive Office | west/northwest | scanner clue, map board, safer landmark |
| B.N.T.G. | Broken Trader Kiosk | east/central-east | salvage, trader, crowbar crate |
| Clippers | Crawlspace Route | south/southeast | hidden routes, chalk marks, hidden extraction clue |

Spacing rule: no faction foothold should be reachable from another in under 9 minutes by the main corridor route during first-time navigation. With hidden routes, Clippers can reduce travel time, but only after discovering route language.

## First Layout Topology

```text
                           [M.E.G. Archive Office]
                                  |
        [Fogged Storage Bay] -- [Service Hall North] -- [Flicker Corridor]
                |                         |                    |
[Stable Extraction]              [Main Service Spine]      [Utility Rooms]
                |                         |                    |
        [Hub Arrival Gate] -- [Abandoned Theater Corner] -- [B.N.T.G. Kiosk]
                                          |
                                  [Crawlspace Route]
                                          |
                               [Hidden Ticket Booth Exit]
                                          |
                                [Clippers Route Wall]
```

## Coordinate Plan

Use these as first graybox anchors, not final art positions.

| Zone | Approx Center | Radius / Size Intent |
|---|---:|---|
| Hub Arrival Gate | `(0, 0)` | small sealed-room buffer |
| Main Service Spine | `(220m, 70m)` | long readable artery |
| Service Hall North | `(240m, 270m)` | branching route |
| Fogged Storage Bay | `(-90m, 250m)` | wide loot/tension room |
| M.E.G. Archive Office | `(70m, 470m)` | compact office cluster |
| Flicker Corridor | `(500m, 340m)` | long entity patrol lane |
| Utility Room Cluster | `(620m, 70m)` | dense mechanical rooms |
| B.N.T.G. Kiosk | `(540m, -190m)` | trader/salvage pocket |
| Abandoned Theater Corner | `(140m, -210m)` | ticket/relic flavor pocket |
| Crawlspace Route | `(220m, -420m)` | low/hidden alternate route |
| Clippers Route Wall | `(470m, -520m)` | route landmark |
| Stable Extraction | `(-240m, 90m)` | reliable return path |
| Hidden Ticket Booth Exit | `(40m, -560m)` | conditional hidden exit |

## Route Rules

- Main Service Spine should be wide enough for readable navigation but broken by doors, partial walls, and repeating geometry.
- Fogged Storage Bay should create line-of-sight uncertainty without hiding the only exit.
- Flicker Corridor should be a high-risk connector, not a mandatory route for all extractions.
- Utility Room Cluster should support cabinet/locker/supply-crate placement.
- Crawlspace Route should be easy to miss from the main route and easy to lose once inside.
- Hidden Ticket Booth Exit should require Movie Ticket condition and route knowledge.

## Getting Lost Without Feeling Cheated

Use these tools:

- repeating service doors
- subtle signage contradictions
- flickering lights that change route confidence
- low ceilings/crawlspaces that restrict sightlines
- one-way drops or vents only for shortcuts
- landmarks every 90-150 seconds of walking

Avoid these in V0.1:

- random teleporting
- full procedural reshuffle
- identical hallways with no recovery landmarks
- dead-end mazes that waste time without loot or threat

## Container Placement Rules

- Cabinets: near Fogged Storage Bay, Utility Rooms, Archive Office.
- Lockers: Utility Rooms, Service Hall North, near Flicker Corridor edge.
- Crowbar supply crates: B.N.T.G. Kiosk and one optional side pocket.
- Theater caches: Abandoned Theater Corner and Hidden Ticket Booth route.

## Entity Placement Rules

The Flicker Stalker patrol should start in Flicker Corridor and threaten two adjacent spaces:

- Service Hall North
- Utility Room Cluster

It should not camp the Hub Arrival Gate or Stable Extraction in V0.1.

## Expansion Hooks

Future faction bases can grow outward from the V0.1 footholds:

- M.E.G. expands northwest into archive/survey rooms.
- B.N.T.G. expands east into trader vault/salvage market.
- Clippers expand south into route dens and shortcut networks.

The first full faction-base spacing pass should preserve at least 9 minutes of cautious travel between major base entrances by standard routes.
