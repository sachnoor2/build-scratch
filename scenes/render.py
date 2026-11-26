#!/usr/bin/env python3
"""Blender driver: render an absolute frame range from ONE world file, through one camera.

    blender -b scenes/world.blend -P scenes/render.py -- \
        --camera cam-rig-med --start 0 --end 95 --move orbit-left@0.8

The world file holds the geometry, the lights, the materials and every camera, so two shots cannot
disagree about the light, the palette or the scale. Every shot also gets a camera move across its
own range, because a locked-off camera for 13 minutes is what makes twelve sets look like one set.
"""
import argparse, math, os, sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--camera", required=True)
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--end", type=int, required=True)
ap.add_argument("--out", default="public/out")
ap.add_argument("--samples", type=int, default=32)
ap.add_argument("--move", default="push-in@0.6", help="name@strength, e.g. orbit-left@0.8")
a = ap.parse_args(argv)

scene = bpy.context.scene

cam = bpy.data.objects.get(a.camera)
if cam is None:
    sys.exit(f"camera {a.camera!r} not found in this world - add it to the world file, do not invent a new angle")
scene.camera = cam



def fcurves_of(action):
    """F-curves from an action, on Blender 4.x and 5.x.

    Blender 4.4+ moved animation onto layered actions, so `action.fcurves` raises
    AttributeError on 5.0 - which silently killed every shard before a frame was written.
    """
    try:
        return list(action.fcurves)
    except AttributeError:
        curves = []
        for layer in getattr(action, "layers", []) or []:
            for strip in getattr(layer, "strips", []) or []:
                for bag in getattr(strip, "channelbags", []) or []:
                    curves.extend(getattr(bag, "fcurves", []) or [])
        return curves

def apply_move(ob, move, frames):
    """Key the camera from where it is to where the move takes it, across this shot only."""
    name, _, strength = move.partition("@")
    try:
        s = float(strength) if strength else 0.6
    except ValueError:
        s = 0.6
    span = max(1, frames) / 24.0                      # seconds of screen time
    quat = ob.matrix_world.to_quaternion()
    fwd = quat @ Vector((0, 0, -1))
    right = quat @ Vector((1, 0, 0))
    up = quat @ Vector((0, 1, 0))
    target = ob.location + fwd * 12.0

    base_loc = ob.location.copy()
    base_rot = ob.rotation_euler.copy()

    if name in ("push-in", "pull-out"):
        d = (0.55 if name == "push-in" else -0.55) * s * span
        ob.location = base_loc + fwd * d
    elif name in ("drift-left", "drift-right"):
        d = (-1.0 if name == "drift-left" else 1.0) * s * span
        ob.location = base_loc + right * d
    elif name in ("crane-up", "crane-down"):
        d = (0.9 if name == "crane-up" else -0.9) * s * span
        ob.location = base_loc + up * d
    elif name in ("orbit-left", "orbit-right"):
        ang = math.radians((-13.0 if name == "orbit-left" else 13.0) * s)
        pivot = target
        rel = base_loc - pivot
        ca, sa = math.cos(ang), math.sin(ang)
        ob.location = pivot + Vector((rel.x * ca - rel.y * sa, rel.x * sa + rel.y * ca, rel.z))
    elif name in ("roll-left", "roll-right"):
        ob.rotation_euler = (base_rot.x, base_rot.y,
                             base_rot.z + math.radians((-7.0 if name == "roll-left" else 7.0) * s))
    elif name == "still":
        pass
    else:
        print(f"unknown move {name!r}, holding still")

    if name in ("orbit-left", "orbit-right"):
        direction = target - ob.location
        ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    # key the end pose, then rewind to the start pose so the shot interpolates across itself
    end_loc, end_rot = ob.location.copy(), ob.rotation_euler.copy()
    ob.location = base_loc
    ob.rotation_euler = base_rot
    ob.keyframe_insert("location", frame=a.start)
    ob.keyframe_insert("rotation_euler", frame=a.start)
    ob.location = end_loc
    ob.rotation_euler = end_rot
    ob.keyframe_insert("location", frame=a.end)
    ob.keyframe_insert("rotation_euler", frame=a.end)
    if ob.animation_data and ob.animation_data.action:
        for fc in fcurves_of(ob.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    ob.location = base_loc
    ob.rotation_euler = base_rot


apply_move(cam, a.move, a.end - a.start + 1)

scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = a.samples
# the pod has 2 GB and the denoiser needs more; NO_DENOISE=1 keeps local checks cheap
scene.cycles.use_denoising = os.environ.get("NO_DENOISE") != "1"
scene.render.motion_blur_shutter = 0.5
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(a.out, "frame_######")
scene.frame_start = a.start
scene.frame_end = a.end

bpy.ops.render.render(animation=True)
print(f"rendered {a.start}-{a.end} via {a.camera} ({a.move}) into {a.out}")
