"""Turn the chapter data into the two files the pipeline reads.

  narration.json  — what the voice says, in order, with the join for each cut
  src/shots.json  — which template draws each shot, and with what text

Nothing here is hand-timed: durations come from the measured audio later.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FPS = 24
WIDTH, HEIGHT = 1920, 1080
PAD = 0.6
MIN_SECONDS = 3.0

JOINS = ["push", "portal", "squeeze", "flash"]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CH


def load_extra(path):
    spec = importlib.util.spec_from_file_location("extra", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXTRA


def main():
    chapters = []
    for f in ("ch1_4.py", "ch5_8.py", "ch9_12.py"):
        chapters += load(os.path.join(ROOT, "content", f), f[:-3])

    # fold the extra detail into each chapter, before its closing card
    extra = load_extra(os.path.join(ROOT, "content", "extra.py"))
    for ch in chapters:
        more = extra.get(ch["n"], [])
        if more:
            ch["shots"] = ch["shots"][:-1] + more + ch["shots"][-1:]

    scenes, shots = [], {}
    n = 0
    for ch in chapters:
        for i, (text, caption, template, props) in enumerate(ch["shots"]):
            n += 1
            sid = f"{ch['n']:02d}-{i + 1:02d}"
            kind = JOINS[n % len(JOINS)]
            if kind == "squeeze":
                join = {"kind": "squeeze", "dir": 1 if n % 2 else -1}
            elif kind == "flash":
                join = {"kind": "flash"}
            else:
                join = {"kind": kind, "anchor": {"x": 960, "y": 470, "r": 180}}
            scenes.append({"id": sid, "text": text, "caption": caption, "joinOut": join})
            shots[sid] = {
                "template": template,
                "props": props,
                "accent": ch["accent"],
                "chapter": ch["n"],
                "chapterTitle": ch["title"],
            }
    # the film never ends on a join effect
    scenes[-1]["joinOut"] = {"kind": "push", "anchor": {"x": 960, "y": 470, "r": 180}}

    narration = {
        "fps": FPS,
        "width": WIDTH,
        "height": HEIGHT,
        "title": "Quantum Entanglement — ek hi avastha, do kan",
        "engine": "piper",
        "voice": "hi_IN-pratham-medium",
        "lang": "hi",
        "lengthScale": 1.0,
        "pad": PAD,
        "minSeconds": MIN_SECONDS,
        "scenes": scenes,
    }
    with open(os.path.join(ROOT, "narration.json"), "w", encoding="utf-8") as f:
        json.dump(narration, f, ensure_ascii=False, indent=2)
    with open(os.path.join(ROOT, "src", "shots.json"), "w", encoding="utf-8") as f:
        json.dump({"shots": shots}, f, ensure_ascii=False, indent=2)

    words = sum(len(s["text"].split()) for s in scenes)
    print(f"{len(chapters)} chapters, {len(scenes)} shots, {words} words")
    print(f"estimated speech {words / 2.4:.0f}s at 145 wpm")


if __name__ == "__main__":
    main()
