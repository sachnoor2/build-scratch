"""Merge the measured voice timings into the film manifest.

`scripts/hinglish_voice.py` writes `src/voice.json`: one entry per shot with the
duration it actually measured after the processing chain. This script joins that
with `narration.json` (text, caption, join) and writes `src/manifest.json`, which
is what Remotion, the foley and the QA gate read.

No duration is ever typed here — they all come from the measured audio.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NARR = json.load(open(os.path.join(ROOT, "narration.json"), encoding="utf-8"))
VOICE = json.load(open(os.path.join(ROOT, "src", "voice.json"), encoding="utf-8"))

measured = {s["id"]: s for s in VOICE["scenes"]}
fps = int(VOICE["fps"])

cursor = 0
scenes = []
for sc in NARR["scenes"]:
    sid = sc["id"]
    if sid not in measured:
        raise SystemExit(f"voice.json has no entry for {sid} — did the voice stage run?")
    frames = int(measured[sid]["frames"])
    scenes.append(
        {
            "id": sid,
            "text": sc["text"],
            "caption": sc.get("caption", ""),
            "start": cursor,
            "dur": frames,
            "seconds": measured[sid]["seconds"],
            "joinOut": sc["joinOut"],
        }
    )
    cursor += frames

manifest = {
    "fps": fps,
    "width": NARR["width"],
    "height": NARR["height"],
    "title": NARR["title"],
    "voice": VOICE.get("voice", ""),
    "scenes": scenes,
    "totalFrames": cursor,
    "totalSeconds": round(cursor / fps, 3),
}

with open(os.path.join(ROOT, "src", "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

for s in scenes:
    print(f"{s['id']:>14}  {s['seconds']:6.2f}s  {s['dur']:5d}f  start {s['start']:5d}  {s['joinOut']['kind']}")

print(f"\ntotal {cursor} frames = {cursor / fps:.2f}s, {len(scenes)} shots")
print(f"cut density {len(scenes) / (cursor / fps / 60):.1f} shots/min")
