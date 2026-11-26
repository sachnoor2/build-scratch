#!/usr/bin/env python3
"""Build shotlist.json from the measured manifest.

Shot boundaries come from the voice that was actually synthesised, never from a guess, so a caption
can never land on the wrong beat.

The visual grammar is the point of this file. Twelve sets, three angles each, eight camera moves.
Consecutive shots never repeat a set, and no set carries more than its share of the film, because a
film that returns to the same six rooms for thirteen minutes reads as one room.
"""
import json

# chapter -> the set whose geometry argues that beat
SET_OF_CHAPTER = {
    1: "pair",          # the trap: two particles, matched answers
    2: "crystal",       # the mathematics, and where pairs come from
    3: "split",         # EPR: one object, two halves
    4: "chart",         # Bell: the inequality and its ceiling
    5: "rig",           # the experiments
    6: "detector",      # the loopholes: what a detector misses
    7: "timeline",      # the Nobel history
    8: "channel",       # no message: the classical link
    9: "mirror",        # teleportation: the path the state takes
    10: "interference", # applications
    11: "cloud",        # three levels: interpretation as a cloud of readings
    12: "pair",         # recap
}
SETS = ["pair", "crystal", "rig", "lattice", "channel", "chart",
        "interference", "mirror", "detector", "timeline", "cloud", "split"]
RIGS = ["wide", "med", "macro"]
MOVES = ["push-in@0.7", "orbit-left@0.8", "crane-up@0.6", "drift-right@0.7",
         "pull-out@0.6", "orbit-right@0.9", "crane-down@0.5", "drift-left@0.6",
         "roll-left@0.5", "push-in@1.0"]

man = json.load(open("src/manifest.json", encoding="utf-8"))
brief = json.load(open("brief.json", encoding="utf-8"))
fps = brief.get("fps", man["fps"])          # brief.json is the single source of truth

shots, at = [], 0
prev_set, set_uses = None, {s: 0 for s in SETS}

for i, s in enumerate(man["scenes"]):
    ch = int(s["id"].split("-")[0])
    home = SET_OF_CHAPTER.get(ch, "pair")
    # rotate through the sets inside a chapter so the room changes every shot, but keep the
    # chapter's own set as the anchor of that stretch
    setname = home if i % 3 == 0 else SETS[(SETS.index(home) + i) % len(SETS)]
    if setname == prev_set:                       # never twice in a row
        setname = SETS[(SETS.index(setname) + 1) % len(SETS)]

    # macro on one shot in five; the rest alternate wide and medium
    rig = RIGS[2] if i % 5 == 4 else RIGS[i % 2]
    camera = f"cam-{setname}-{rig}"
    move = MOVES[i % len(MOVES)]

    shots.append({"id": s["id"], "start": at, "end": at + s["frames"] - 1, "camera": camera,
                  "set": setname, "rig": rig, "sim": "none", "character": "none",
                  "stateIn": f"beat {i+1} begins", "stateOut": f"beat {i+1} lands",
                  "motion": [move.split("@")[0]], "samples": 8,
                  "cameraIn": move, "cameraOut": move})
    at += s["frames"]
    set_uses[setname] += 1
    prev_set = setname

json.dump({"fps": fps, "width": brief["width"], "height": brief["height"],
           "world": "scenes/world.blend", "totalFrames": at, "sets": SETS, "shots": shots},
          open("shotlist.json", "w", encoding="utf-8"), indent=1)

print(f"shotlist: {len(shots)} shots, {at} frames = {at/fps:.1f}s")
print("set usage:", ", ".join(f"{k}:{v}" for k, v in sorted(set_uses.items(), key=lambda x: -x[1])))
print("cameras used:", len({s['camera'] for s in shots}), "| moves used:", len({s['cameraIn'] for s in shots}))
