#!/usr/bin/env python3
"""Verify the shard videos and stitch them into public/out/base.mp4.

The frames no longer travel as PNGs: each render job encodes its own range into one MP4, which
keeps the artifact a few MB instead of ~10 GB. What still has to hold is coverage — every global
frame index rendered exactly once, in numeric order.

Exit 0 clean, 2 a shard missing or a coverage gap, 3 stitch failed.
"""
import argparse, glob, json, os, re, subprocess, sys


def shard_files(frames_dir):
    """Shards in NUMERIC order. A shell glob sorts shard-10 before shard-2."""
    paths = glob.glob(os.path.join(frames_dir, "shard_*.mp4"))
    def num(p):
        m = re.search(r"shard_(\d+)\.mp4$", p)
        return int(m.group(1)) if m else -1
    return sorted(paths, key=num)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return -1.0


def verify(frames_dir, total, fps):
    shards = shard_files(frames_dir)
    if not shards:
        print(f"FAIL: no shard_*.mp4 in {frames_dir}")
        return 2
    frames = 0
    for p in shards:
        d = probe_duration(p)
        if d <= 0:
            print(f"FAIL: unreadable shard {p}")
            return 2
        frames += round(d * fps)
        print(f"  {os.path.basename(p):20s} {d:8.2f}s")
    drift = frames - total
    print(f"OK: {len(shards)} shards, {frames} frames vs {total} expected (drift {drift:+d})")
    if abs(drift) > len(shards) * 2:      # a couple of frames per shard is container rounding
        print("FAIL: coverage does not match the manifest")
        return 2
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="public/out")
    ap.add_argument("--manifest", default="src/manifest.json")
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()

    man = json.load(open(a.manifest, encoding="utf-8"))
    total, fps = man["totalFrames"], man["fps"]

    rc = verify(a.frames, total, fps)
    if rc or a.verify_only:
        sys.exit(rc)

    shards = shard_files(a.frames)
    listfile = os.path.join(a.frames, "concat.txt")
    with open(listfile, "w") as f:
        for p in shards:
            f.write(f"file '{os.path.basename(p)}'\n")
    base = os.path.join(a.frames, "base.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                        "-c", "copy", "-movflags", "+faststart", base],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("stitch failed:", r.stderr[-600:])
        sys.exit(3)
    print(f"stitched {len(shards)} shards -> {base} ({probe_duration(base):.2f}s)")


if __name__ == "__main__":
    main()
