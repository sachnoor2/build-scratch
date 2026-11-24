#!/usr/bin/env python3
"""Build shotlist.json from the measured manifest.

Shot boundaries come from the voice that was actually synthesised, never from a guess, so a
caption can never land on the wrong beat. Cameras come from the chapter, so the cut follows the
argument: the pair set for the trap, the chart for the inequality, the channel for no-message.
"""
import json

SET_OF_CHAPTER = {1: "pair", 2: "crystal", 3: "pair", 4: "chart", 5: "rig", 6: "rig",
                  7: "chart", 8: "channel", 9: "channel", 10: "lattice", 11: "lattice", 12: "pair"}
CAMS = {"pair": ["cam-pair-wide", "cam-pair-macro"],
        "crystal": ["cam-crystal", "cam-crystal-macro"],
        "rig": ["cam-rig-wide", "cam-rig-macro"],
        "lattice": ["cam-lattice", "cam-lattice-macro"],
        "channel": ["cam-channel", "cam-channel-macro"],
        "chart": ["cam-chart", "cam-chart-macro"]}

man = json.load(open("src/manifest.json", encoding="utf-8"))
brief = json.load(open("brief.json", encoding="utf-8"))
fps = brief.get("fps", man["fps"])          # brief.json is the single source of truth
shots, at = [], 0
for i, s in enumerate(man["scenes"]):
    ch = int(s["id"].split("-")[0])
    setname = SET_OF_CHAPTER.get(ch, "pair")
    cam = CAMS[setname][i % 2]
    if i % 4 == 3:                      # break the alternation so it never feels mechanical
        other = [k for k in CAMS if k != setname][(i // 4) % 5]
        cam = CAMS[other][i % 2]
    shots.append({"id": s["id"], "start": at, "end": at + s["frames"] - 1, "camera": cam,
                  "set": setname, "sim": "none", "character": "none",
                  "stateIn": f"beat {i+1} begins", "stateOut": f"beat {i+1} lands",
                  "motion": ["camera drift", "loop animation"], "samples": 8,
                  "cameraIn": "push-in@1.0", "cameraOut": "push-in@1.0"})
    at += s["frames"]

json.dump({"fps": fps, "width": brief["width"], "height": brief["height"],
           "world": "scenes/world.blend",
           "totalFrames": at, "sets": sorted(set(SET_OF_CHAPTER.values())), "shots": shots},
          open("shotlist.json", "w", encoding="utf-8"), indent=1)
print(f"shotlist: {len(shots)} shots, {at} frames = {at/fps:.1f}s")
