# PROGRESS — quantum entanglement, 3D

## State

- Script: rewritten from scratch, hook-first (opens by showing a matched-outcome pair and saying
  outright that this is *not* entanglement). 175 lines, built from the supplied research brief.
  Lives in `narration.json`.
- Voice: measured, 175 scenes, **19,750 frames = 822.9 s** at 24 fps. 1.2x comes from Piper's
  `length_scale` 0.8333, so the accent stays natural (never atempo).
- World: `scenes/build_world.py` builds `scenes/world.blend` — 6 sets (pair, crystal, rig, lattice,
  channel, chart) and 12 cameras, 1280x720@24. Built and saved successfully.
- Shotlist: **not yet generated** (must be derived from `src/manifest.json`).

## Render cost, measured on the 2-core / 2 GB pod (bpy 4.2.0, Cycles CPU)

| settings | measured |
|---|---|
| 1280x720, 24 spp, glare | ~16 min/frame (40 s per sample) |
| 960x540, 8 spp, 2 bounces | **137 s/frame** |
| Workbench / EEVEE headless | unavailable — EGL_BAD_MATCH, no GL context |
| denoiser (OpenImageDenoise) | out of memory at 2 GB |

19,750 frames at 137 s/frame is ~750 CPU-hours. A 13-14 minute Cycles film cannot be rendered
from this pod, and on GitHub's 4-core runners it is still in the hundreds of runner-hours.

## What this means

The template pipeline (voice -> plan_shards -> render_shard -> stitch -> qa) is wired correctly and
the content is written, but the render is the wall. Feasible options:

1. **Blender short** (60-90 s) with a simplified world and low samples — a real 3D piece, renderable.
2. **Blender long on CI** with a large shard budget and reduced settings — hours of runner time,
   plus proper art direction on the world before it is worth rendering.
3. Keep the Remotion cut of this same script (delivered, 13:41.8) and spend effort on content.

The world still needs art direction: the first test still (640x360, 4 spp) showed the pair set
framed far too tight, with the spheres cut off at the frame edges.
