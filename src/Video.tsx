import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";
import shotlist from "../shotlist.json";
import {manifest} from "./manifest";
import {theme} from "./theme";

// The hand-off: the carry is a function of the ABSOLUTE frame, so it never resets at a cut.
// A per-shot interpolate that starts every shot at the same offset is the bug this prevents.
const carry = (absolute: number) => Math.sin(absolute / 36) * 6;

const FrameSeq: React.FC<{start: number; end: number}> = ({start}) => {
  const frame = useCurrentFrame();
  const absolute = start + frame;
  const drift = carry(absolute);
  const scale = 1 + Math.abs(drift) * 0.0008;
  const blur = Math.abs(drift) > 4 ? Math.min(Math.abs(drift) / 6, 3) : 0;

  return (
    <AbsoluteFill>
      <Img
        src={staticFile(`out/frame_${String(absolute).padStart(6, "0")}.png`)}
        style={{
          transform: `translateX(${drift}px) scale(${scale})`,
          filter: blur > 0 ? `blur(${blur}px)` : undefined,
        }}
      />
    </AbsoluteFill>
  );
};

const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  let at = 0;
  for (const scene of manifest.scenes) {
    const end = at + scene.frames;
    if (frame >= at && frame < end && scene.caption) {
      return (
        <AbsoluteFill style={{justifyContent: "flex-end", alignItems: "center", paddingBottom: "18%"}}>
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
    {shotlist.shots.map((shot) => (
      <Sequence
        key={shot.id}
        from={shot.start}
        durationInFrames={shot.end - shot.start + 1}
        name={shot.id}
      >
        <FrameSeq start={shot.start} end={shot.end} />
      </Sequence>
    ))}

    {manifest.scenes.map((scene, i) => {
      const from = manifest.scenes.slice(0, i).reduce((a, s) => a + s.frames, 0);
      return (
        <Sequence key={scene.id} from={from} durationInFrames={scene.frames} name={`audio-${scene.id}`}>
          <Audio src={staticFile(`audio/${scene.id}.wav`)} />
        </Sequence>
      );
    })}

    <Captions />
  </AbsoluteFill>
);
