#!/usr/bin/env python3
"""Build scenes/world.blend for the quantum entanglement film.

One world, one film: every shot renders from this single file, so the light, the palette and
the scale cannot disagree between shots. Six sets sit in a line along +X, each with a wide and
a macro camera; the shotlist names a camera and never a scene file.

    blender -b -P scenes/build_world.py -- --out scenes/world.blend --frames 19750

Everything animates on continuous, looping curves driven by the absolute frame, so a shot
rendered in isolation still moves and still matches its neighbours.
"""
import argparse, math, sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
_sl, _br = {}, {}
try:                                     # brief.json owns size/fps; the shotlist owns length
    import json as _json
    _sl = _json.load(open("shotlist.json", encoding="utf-8"))
    _br = _json.load(open("brief.json", encoding="utf-8"))
except Exception:
    pass
ap.add_argument("--out", default="scenes/world.blend")
ap.add_argument("--frames", type=int, default=int(_sl.get("totalFrames", 19750)))
ap.add_argument("--fps", type=int, default=int(_br.get("fps", _sl.get("fps", 24))))
ap.add_argument("--width", type=int, default=int(_br.get("width", 960)))
ap.add_argument("--height", type=int, default=int(_br.get("height", 540)))
a = ap.parse_args(argv)

CYAN = (0.10, 0.80, 1.00)
MAGENTA = (1.00, 0.25, 0.85)
GOLD = (1.00, 0.72, 0.18)
GREEN = (0.20, 0.95, 0.55)
RED = (1.00, 0.28, 0.32)
VIOLET = (0.55, 0.40, 1.00)
CREAM = (1.00, 0.97, 0.90)
INK = (0.012, 0.018, 0.035)

SETS = ["pair", "crystal", "rig", "lattice", "channel", "chart"]
GAP = 34.0
ORIGIN = {s: Vector((i * GAP, 0.0, 0.0)) for i, s in enumerate(SETS)}

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = a.fps
scene.frame_start = 0
scene.frame_end = a.frames - 1


# --------------------------------------------------------------------------- helpers
def mat(name, color, emit=0.0, rough=0.35, metal=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if "Emission Color" in bsdf.inputs:          # 4.x names
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit
    # NOTE: alpha is ignored on purpose. Transparent surfaces cost far more per sample than
    # they are worth, and the film has to render inside GitHub's 6-hour job limit.
    return m


def mesh(kind, name, loc, scale=(1, 1, 1), material=None, rot=(0, 0, 0), parent=None):
    if kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, location=loc)
    elif kind == "cube":
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=loc)
    elif kind == "ico":
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=loc)
    elif kind == "torus":
        bpy.ops.mesh.primitive_torus_add(location=loc, major_radius=1.0, minor_radius=0.16,
                                         major_segments=48, minor_segments=12)
    elif kind == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=1.0, location=loc)
    elif kind == "plane":
        bpy.ops.mesh.primitive_plane_add(size=2.0, location=loc)
    else:
        raise SystemExit(f"unknown mesh {kind}")
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    ob.rotation_euler = rot
    if material:
        ob.data.materials.append(material)
    if parent:
        ob.parent = parent
    return ob


def key_rotate(ob, turns=1.0, axis=2, phase=0.0):
    """One full revolution across the film, linear, so it never stalls at a cut."""
    ob.rotation_mode = "XYZ"
    ob.keyframe_insert("rotation_euler", frame=0)
    e = list(ob.rotation_euler)
    e[axis] = phase + turns * 2 * math.pi
    ob.rotation_euler = e
    ob.keyframe_insert("rotation_euler", frame=a.frames - 1)
    for fc in ob.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def key_pulse(ob, lo=0.85, hi=1.15, period=48, phase=0):
    """Breathing scale — the cheapest way to make a still frame feel alive."""
    for f in range(0, a.frames, period // 2):
        t = ((f // (period // 2)) % 2)
        s = hi if t else lo
        ob.scale = tuple(v * s for v in ob.get("base_scale", ob.scale))
        ob.keyframe_insert("scale", frame=f)
    for fc in ob.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"


def add_light(name, loc, energy, color, size=6.0, target=None):
    d = bpy.data.lights.new(name, type="AREA")
    d.energy = energy
    d.color = color
    d.size = size
    ob = bpy.data.objects.new(name, d)
    ob.location = loc
    scene.collection.objects.link(ob)
    if target is not None:
        direction = Vector(target) - Vector(loc)
        ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return ob


def add_camera(name, loc, target, lens=50.0, fstop=2.8):
    d = bpy.data.cameras.new(name)
    d.lens = lens
    ob = bpy.data.objects.new(name, d)
    ob.location = loc
    direction = Vector(target) - Vector(loc)
    ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(ob)
    return ob


# --------------------------------------------------------------------------- world floor
floor = mat("floor", (0.02, 0.03, 0.06), rough=0.22, metal=0.4)
grid_line = mat("grid", CYAN, emit=0.5)
mesh("plane", "Floor", (0, 0, -1.6), scale=(220, 40, 1), material=floor)

# a faint luminous grid: thin bars, so the space reads as a stage rather than a void
for i in range(-11, 12):
    mesh("cube", f"grid_x_{i}", (i * 8.0, 0, -1.55), scale=(0.02, 34, 0.02), material=grid_line)
for j in range(-4, 5):
    mesh("cube", f"grid_y_{j}", (0, j * 7.0, -1.55), scale=(150, 0.02, 0.02), material=grid_line)

# drifting dust: cheap, and it gives every lens a sense of depth
dust = mat("dust", CREAM, emit=0.6)
for i in range(24):
    x = -10 + (i * 97 % 210)
    y = -14 + (i * 61 % 28)
    z = -1.0 + (i * 29 % 14) * 0.55
    d = mesh("sphere", f"dust_{i}", (x, y, z), scale=(0.035, 0.035, 0.035), material=dust)
    d["base_scale"] = (0.035, 0.035, 0.035)
    key_pulse(d, lo=0.6, hi=1.5, period=60 + (i % 5) * 18)

# --------------------------------------------------------------------------- 1. PAIR
O = ORIGIN["pair"]
core_a = mat("core_a", CYAN, emit=0.6)
core_b = mat("core_b", MAGENTA, emit=0.6)
halo_a = mat("halo_a", CYAN, emit=0.15)
halo_b = mat("halo_b", MAGENTA, emit=0.15)
filament = mat("filament", CREAM, emit=0.8)

a_sphere = mesh("sphere", "A_core", O + Vector((-7, 0, 0)), scale=(1.0, 1.0, 1.0), material=core_a)
a_sphere["base_scale"] = (1.0, 1.0, 1.0)
b_sphere = mesh("sphere", "B_core", O + Vector((7, 0, 0)), scale=(1.0, 1.0, 1.0), material=core_b)
b_sphere["base_scale"] = (1.0, 1.0, 1.0)
for i, (r, m) in enumerate([(1.25, halo_a), (1.65, halo_b), (2.05, halo_a)]):
    for side, sgn in (("A", -1), ("B", 1)):
        h = mesh("sphere", f"{side}_halo_{i}", O + Vector((sgn * 7, 0, 0)),
                 scale=(r, r, r), material=m)
        h["base_scale"] = (r, r, r)
        key_pulse(h, lo=0.94, hi=1.07, period=72 + i * 24)
key_pulse(a_sphere, lo=0.9, hi=1.1, period=54)
key_pulse(b_sphere, lo=1.1, hi=0.9, period=54)

# the filament between them: a chain of beads, so it reads as one object made of two
for k in range(23):
    t = k / 22.0
    p = O + Vector((-7 + 14 * t, 0, 0))
    bead = mesh("sphere", f"fil_{k}", p, scale=(0.09, 0.09, 0.09), material=filament)
    bead["base_scale"] = (0.09, 0.09, 0.09)
    key_pulse(bead, lo=0.7, hi=1.6, period=40, phase=k)

# entangled ellipse: one state drawn around both particles
ell = mesh("torus", "pair_ellipse", O, scale=(6.2, 6.2, 6.2), material=mat("ell", VIOLET, emit=1.0))
ell.rotation_euler = (math.radians(90), 0, 0)
key_rotate(ell, turns=0.25, axis=1)

# --------------------------------------------------------------------------- 2. CRYSTAL
O = ORIGIN["crystal"]
cry = mat("crystal", VIOLET, emit=0.6, rough=0.08, metal=0.2)
beam = mat("beam", CREAM, emit=2.0)
mesh("ico", "crystal_body", O + Vector((0, 0, 0)), scale=(3.4, 3.4, 3.4), material=cry)
pump = mesh("cylinder", "pump_beam", O + Vector((-9, 0, 0)), scale=(0.16, 0.16, 7.0),
            material=beam, rot=(0, math.radians(90), 0))
for sgn in (-1, 1):
    ang = math.radians(26 * sgn)
    out = mesh("cylinder", f"spdc_{'l' if sgn < 0 else 'r'}",
               O + Vector((7.0, 5.2 * sgn, 0)), scale=(0.13, 0.13, 6.2),
               material=mat(f"spdc_m{sgn}", CYAN if sgn < 0 else MAGENTA, emit=0.9),
               rot=(0, math.radians(90), ang))
key_rotate(mesh("ico", "crystal_shell", O, scale=(4.6, 4.6, 4.6),
                material=mat("shell", CYAN, emit=0.25)), turns=0.6, axis=2)

# --------------------------------------------------------------------------- 3. RIG
O = ORIGIN["rig"]
ring = mat("ring", GOLD, emit=1.2, metal=0.6, rough=0.2)
glass = mat("glass", CYAN, emit=0.3)
boxmat = mat("box", (0.05, 0.07, 0.12), rough=0.3, metal=0.5)

for sgn, col in ((-1, CYAN), (1, MAGENTA)):
    station = O + Vector((sgn * 10, 0, 0))
    mesh("cube", f"station_{sgn}", station + Vector((0, 0, -0.2)), scale=(2.6, 2.6, 2.6), material=boxmat)
    r1 = mesh("torus", f"pol_{sgn}", station, scale=(1.7, 1.7, 1.7), material=ring)
    r1.rotation_euler = (math.radians(90), 0, 0)
    key_rotate(r1, turns=1.2 * sgn, axis=1)
    r2 = mesh("torus", f"pol_inner_{sgn}", station, scale=(1.15, 1.15, 1.15),
              material=mat(f"inner_{sgn}", col, emit=0.5))
    r2.rotation_euler = (0, math.radians(90), 0)
    key_rotate(r2, turns=-0.9 * sgn, axis=2)

# photon travelling between the stations, on a loop
photon = mesh("sphere", "photon", O + Vector((-10, 0, 0)), scale=(0.22, 0.22, 0.22),
              material=mat("photon", CREAM, emit=1.4))
for f in range(0, a.frames, 24):
    t = (f % 96) / 96.0
    photon.location = O + Vector((-10 + 20 * t, 0, 0))
    photon.keyframe_insert("location", frame=f)
for fc in photon.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"

# --------------------------------------------------------------------------- 4. LATTICE
O = ORIGIN["lattice"]
node = mat("node", CYAN, emit=1.4)
strut = mat("strut", CREAM, emit=0.6, alpha=0.5)
for ix in range(-2, 3):
    for iy in range(-1, 2):
        for iz in range(0, 2):
            p = O + Vector((ix * 2.3, iy * 2.3, iz * 2.3 - 1.0))
            n = mesh("cube", f"lat_{ix}_{iy}_{iz}", p, scale=(0.16, 0.16, 0.16), material=node)
            n["base_scale"] = (0.16, 0.16, 0.16)
            key_pulse(n, lo=0.6, hi=1.4, period=54 + (ix + iy + iz) % 4 * 12)
for ix in range(-2, 3):
    for iy in range(-1, 2):
        for iz in (0, 1):
                mesh("cube", f"st_{ix}_{iy}_{iz}", O + Vector((ix * 2.3, iy * 2.3, iz * 2.3 + 0.15)),
                     scale=(0.03, 0.03, 1.15), material=strut)

# --------------------------------------------------------------------------- 5. CHANNEL
O = ORIGIN["channel"]
alice = mesh("cube", "alice_box", O + Vector((-11, 0, 0)), scale=(2.4, 2.4, 2.4), material=boxmat)
bob = mesh("cube", "bob_box", O + Vector((11, 0, 0)), scale=(2.4, 2.4, 2.4), material=boxmat)
mesh("torus", "alice_ring", O + Vector((-11, 0, 0)), scale=(3.2, 3.2, 3.2),
     material=mat("alice_ring", CYAN, emit=1.4))
mesh("torus", "bob_ring", O + Vector((11, 0, 0)), scale=(3.2, 3.2, 3.2),
     material=mat("bob_ring", MAGENTA, emit=1.4))
# the classical channel: a dashed link with a pulse that crawls along it
dash = mat("dash", GOLD, emit=1.0)
for k in range(21):
    x = -9.0 + k * 0.9
    mesh("cube", f"dash_{k}", O + Vector((x, 0, -0.4)), scale=(0.30, 0.06, 0.06), material=dash)
pulse = mesh("sphere", "channel_pulse", O + Vector((-9, 0, -0.4)), scale=(0.2, 0.2, 0.2),
             material=mat("pulse", GOLD, emit=0.6))
for f in range(0, a.frames, 30):
    t = (f % 120) / 120.0
    pulse.location = O + Vector((-9 + 18 * t, 0, -0.4))
    pulse.keyframe_insert("location", frame=f)
for fc in pulse.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = "LINEAR"

# the forbidden faster-than-light link: a broken red arc between the same two boxes
mesh("torus", "forbidden_arc", O + Vector((0, 0, 2.2)), scale=(5.5, 5.5, 5.5),
     material=mat("forbidden", RED, emit=1.2, alpha=0.22))

# --------------------------------------------------------------------------- 6. CHART
O = ORIGIN["chart"]
bar_ok = mat("bar_ok", CYAN, emit=0.9)
bar_over = mat("bar_over", GREEN, emit=1.6)
for i in range(9):
    h = 1.2 + i * 0.55
    mesh("cube", f"bar_{i}", O + Vector((-8 + i * 2.0, 0, h - 1.6)),
         scale=(0.55, 0.55, h), material=bar_ok if i < 6 else bar_over)
# the limit plane the local theory cannot cross, and the quantum ceiling above it
mesh("cube", "limit_plane", O + Vector((-1.0, 0, 3.4)), scale=(9.5, 2.2, 0.03),
     material=mat("limit", RED, emit=0.85))
mesh("cube", "quantum_plane", O + Vector((-1.0, 0, 5.1)), scale=(9.5, 2.2, 0.03),
     material=mat("qceil", GREEN, emit=0.8))

# --------------------------------------------------------------------------- lights
for i, s in enumerate(SETS):
    O = ORIGIN[s]
    add_light(f"key_{s}", O + Vector((-8, -10, 12)), 380, (1.0, 0.96, 0.9), size=9, target=O)
    add_light(f"rim_{s}", O + Vector((10, 9, 7)), 220, (0.45, 0.7, 1.0), size=8, target=O)

world = bpy.data.worlds.new("World")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (*INK, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
scene.world = world

# --------------------------------------------------------------------------- cameras
# two angles per set: geography and the detail that proves it
CAMS = {
    "cam-pair-wide":   ("pair",    (-2, -22, 9),   (0, 0, 0.5), 42, 4.0),
    "cam-pair-macro":  ("pair",    (-19, -13, 3.5), (-7, 0, 0),  58, 2.8),
    "cam-crystal":     ("crystal", (-12, -16, 8),  (2, 0, 0),   50, 3.2),
    "cam-crystal-macro": ("crystal", (-16, -13, 5.5), (2, 0, 0), 55, 2.6),
    "cam-rig-wide":    ("rig",     (0, -24, 7),    (0, 0, 0.5), 40, 4.0),
    "cam-rig-macro":   ("rig",     (-22, -14, 3.0), (-9, 0, 0), 62, 2.6),
    "cam-lattice":     ("lattice", (0, -20, 10),   (0, 0, 1.5), 45, 3.5),
    "cam-lattice-macro": ("lattice", (-16, -13, 5.0), (0, 0, 1.5), 52, 2.8),
    "cam-channel":     ("channel", (0, -22, 6),    (0, 0, 0.5), 40, 4.0),
    "cam-channel-macro": ("channel", (-22, -14, 2.5), (-9, 0, 0), 60, 2.6),
    "cam-chart":       ("chart",   (0, -20, 7),    (0, 0, 2.5), 45, 4.0),
    "cam-chart-macro": ("chart",   (4, -18, 5.5),  (4, 0, 3.0), 55, 2.8),
}
for name, (setname, loc, tgt, lens, fstop) in CAMS.items():
    O = ORIGIN[setname]
    add_camera(name, O + Vector(loc), O + Vector(tgt), lens=lens, fstop=fstop)

scene.camera = bpy.data.objects["cam-pair-wide"]

# --------------------------------------------------------------------------- render defaults
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 8
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 1
scene.cycles.diffuse_bounces = 1
scene.cycles.glossy_bounces = 1
scene.cycles.transmission_bounces = 0
scene.cycles.transparent_max_bounces = 0
scene.render.resolution_x = a.width
scene.render.resolution_y = a.height
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
_tf = [v.name for v in scene.view_settings.bl_rna.properties["view_transform"].enum_items]
scene.view_settings.view_transform = "AgX" if "AgX" in _tf else "Standard"
try:
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    pass
scene.view_settings.exposure = -0.2

# no compositor: the glare pass costs a full-frame buffer operation per sample
scene.use_nodes = False

bpy.ops.wm.save_as_mainfile(filepath=a.out)
print(f"wrote {a.out}: {a.frames} frames, {len(SETS)} sets, {len(CAMS)} cameras, "
      f"{a.width}x{a.height}@{a.fps}")
