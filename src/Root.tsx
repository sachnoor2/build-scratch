import React from "react";
import {Composition} from "remotion";
import {Video} from "./Video";
import {manifest} from "./manifest";
import brief from "../brief.json";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Video"
    component={Video}
    durationInFrames={Math.max(manifest.totalFrames, 1)}
    fps={manifest.fps}
    // brief.json owns the canvas, the same file the Blender world reads. Hardcoding 720x1280
    // here is how a landscape film came out portrait with letterbox bars.
    width={brief.width}
    height={brief.height}
  />
);
