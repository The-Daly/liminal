# Operations Hub Layout Spec

## Goal

The main player menu should now aim for a restrained operations-console composition:

- left rail for destination navigation
- large center operation card for deployment focus
- right rail for operator and faction status
- low-profile footer telemetry

The target feeling is tense, procedural, and Backrooms-specific rather than glossy military futurism.

## Layout Breakdown

### Left Rail

- section label: `Main Menu`
- vertical destinations:
  - Deploy
  - Loadout
  - Operators
  - Market
  - Intel
  - Settings
  - Exit
- `Deploy` should read as the strongest highlighted action

### Center Operation Card

- title format: `Operation: Service Halls`
- zone code format: `Zone // SH-17`
- supporting fields:
  - threat level
  - extraction windows
  - environmental anomaly
  - recommended team size
  - brief objective
- primary call to action:
  - `Deploy`
  - subtext: `Enter Zone`

### Right Rail

- operator name and ID
- faction name and faction role
- health condition
- reputation summary
- currency/resources summary
- current kit summary

This should feel like a field briefing, not a social profile.

### Footer

- build label
- environment label
- online/system state
- local time

The footer should read like live telemetry.

## Liminal Dominion Adaptation

Keep the visual grammar grounded in the existing world:

- M.E.G. should feel archive/research procedural
- B.N.T.G. should feel logistics and salvage aware
- Clippers should feel route-marked and hand-maintained
- muted yellow-green, off-white, and dirty amber accents are preferred over neon
- typography should feel industrial and operational

## Immediate Implementation Rule

The first pass does not need final widget polish. It does need the correct information architecture and default data:

1. left-rail navigation identity
2. center deployment briefing identity
3. right-rail operator status identity
4. footer telemetry identity

That information architecture now matters more than decoration.
