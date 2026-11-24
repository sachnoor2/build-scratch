#!/usr/bin/env python3
"""Write bench.json from a timed render. plan_shards.py reads this, never a guess."""
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--end", type=int, required=True)
ap.add_argument("--frames", type=int, required=True)
a = ap.parse_args()

spf = max(1.0, (a.end - a.start) / a.frames)
json.dump({"secondsPerFrame": round(spf, 2), "frames": a.frames}, open("bench.json", "w"))
print(f"bench: {a.frames} frames in {a.end - a.start}s -> {spf:.2f} s/frame")
