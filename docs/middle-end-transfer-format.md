# Middle-end transfer format

This document will detail the format in which data will be stored while it is being transferred from the back-end to the front-end for the replay viewer. The format should be provided as a regular JSON object.

## Sample File

```json
[
  [
    [["x1", "y1"], ["x2", "y2"], ["x3", "y3"], ["x4", "y4"]]
  ],
  ["player-1", "player-2"],
  [
    ["class", "..."],
    ["..."]
  ],
  [
    [
      [
        ["x", "y", "HP", "shield", "firing angle (or -1)", "ability cooldown", "ability target (or -1, or 0 for self-cast, or [x, y] for coordinate cast)", ["status effects", "..."]],
        "..."
      ],
      ["..."],
      ["barrier 1 HP (or -1)", "..."]
    ]
  ]
]
```

## Hierarchy

- file
  - map
    - barrier
      - corner coordinate
        - x
        - y
  - players
    - player 1
    - player 2
  - teams
    - tanks
      - class
  - frames
    - teams
      - tanks
        - ... (if the tank dies this frame, submit 0 instead of a list and discard it from the list)
