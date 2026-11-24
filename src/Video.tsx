import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import {manifest} from "./manifest";
import {theme} from "./theme";

// The Blender frames arrive as ONE video per shard, stitched into out/base.mp4 by stitch.py.
// Compositing a single file instead of ~19,700 PNGs keeps the artifact inside the repository's
// storage quota, and it removes any way for a single frame index to go missing.

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  let at = 0;
  for (const scene of manifest.scenes) {
    const end = at + scene.frames;
    if (frame >= at && frame < end && scene.caption) {
      return (
        <AbsoluteFill
          style={{justifyContent: "flex-end", alignItems: "center", paddingBottom: "12%"}}
        >
          <div style={theme.caption}>{scene.caption}</div>
        </AbsoluteFill>
      );
    }
    at = end;
  }
  return null;
};

export const Video: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: theme.ink}}>
    <OffthreadVideo src={staticFile("out/base.mp4")} />

    {manifest.scenes.map((scene, i) => {
      const from = manifest.scenes.slice(0, i).reduce((a, s) => a + s.frames, 0);
      return (
        <Sequence
          key={scene.id}
          from={from}
          durationInFrames={scene.frames}
          name={`audio-${scene.id}`}
        >
          <Audio src={staticFile(`audio/${scene.id}.wav`)} />
        </Sequence>
      );
    })}

    <Captions />
  </AbsoluteFill>
);
