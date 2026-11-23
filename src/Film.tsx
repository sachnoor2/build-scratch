import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import manifestJson from './manifest.json';
import {FlashOverlay, HALF_WINDOW, Join, JoinLayer} from './joins';
import {SCENES} from './scenes';
import {C, Grain, Vignette, ramp} from './ui';

type Scene = {
  id: string;
  text: string;
  caption: string;
  start: number;
  dur: number;
  joinOut: Join;
};

const MANIFEST = manifestJson as unknown as {
  fps: number;
  width: number;
  height: number;
  scenes: Scene[];
};

const HALF = HALF_WINDOW;

// The scenes are authored in a 1080x1920 design space. The composition can be
// smaller (720x1280 for shorts), so the whole film is drawn at design size and
// scaled once, here — never per scene, and never by cropping.
const DESIGN_W = 1920;
const DESIGN_H = 1080;
const K = MANIFEST.width / DESIGN_W;

/**
 * Caption cards for one shot. The script's `caption` field holds the on-screen
 * words (Roman Hinglish), split into cards by "|". Each card takes an equal
 * share of the shot, so a card never outlives its line.
 */
const captionCards = (caption: string, dur: number) => {
  const parts = caption
    .split('|')
    .map((s) => s.trim())
    .filter(Boolean);
  const list = parts.length ? parts : [''];
  const span = dur / list.length;
  return list.map((text, i) => ({text, from: i * span, to: (i + 1) * span}));
};

const Caption: React.FC<{text: string; opacity: number}> = ({text, opacity}) => (
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 54}}>
    <div
      style={{
        opacity,
        fontFamily: 'Helvetica, Arial, "DejaVu Sans", sans-serif',
        fontSize: 54,
        fontWeight: 900,
        letterSpacing: -1,
        color: '#ffffff',
        textAlign: 'center',
        maxWidth: '78%',
        lineHeight: 1.06,
        textShadow: '0 6px 22px rgba(0,0,0,0.78), 0 2px 4px rgba(0,0,0,0.65)',
      }}
    >
      {text}
    </div>
  </AbsoluteFill>
);

export const Film: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scenes = MANIFEST.scenes;
  const n = scenes.length;

  // Which boundary window are we inside, if any?
  let active: {i: number; p: number} | null = null;
  for (let i = 0; i < n - 1; i++) {
    const b = scenes[i + 1].start;
    if (frame >= b - HALF && frame < b + HALF) {
      active = {i, p: (frame - (b - HALF)) / (2 * HALF)};
      break;
    }
  }

  let solo = scenes.findIndex((s) => frame >= s.start && frame < s.start + s.dur);
  if (solo < 0) solo = frame < 0 ? 0 : n - 1;

  // Scene-local time is remapped across the extended window so a shot is
  // already moving before its official start and still moving after its end.
  const localT = (s: Scene) => (frame - s.start + HALF) * (s.dur / (s.dur + 2 * HALF));

  const layers: {s: Scene; role: 'out' | 'in' | 'solo'; p: number}[] = active
    ? [
        {s: scenes[active.i], role: 'out', p: active.p},
        {s: scenes[active.i + 1], role: 'in', p: active.p},
      ]
    : [{s: scenes[solo], role: 'solo', p: 0}];

  const joinCfg: Join | null = active ? scenes[active.i].joinOut : null;

  return (
    <AbsoluteFill style={{backgroundColor: C.ink}}>
      <AbsoluteFill
        style={{width: DESIGN_W, height: DESIGN_H, transform: `scale(${K})`, transformOrigin: 'top left'}}
      >
      {/* narration, one file per shot, starting exactly on its frame */}
      {scenes.map((s) => (
        <Sequence key={`a-${s.id}`} from={s.start} durationInFrames={s.dur} name={`vo-${s.id}`}>
          <Audio src={staticFile(`audio/${s.id}.wav`)} />
        </Sequence>
      ))}

      {/* foley: one whoosh per join, starting 10 frames before the boundary (J-cut) */}
      {scenes.slice(0, n - 1).map((s, i) => (
        <Sequence
          key={`f-${i}`}
          from={Math.max(0, scenes[i + 1].start - 10)}
          durationInFrames={26}
          name={`foley-${i}`}
        >
          <Audio
            src={staticFile(`audio/foley/join-${String(i + 1).padStart(2, '0')}.wav`)}
            volume={0.42}
          />
        </Sequence>
      ))}

      {layers.map(({s, role, p}) => {
        const Comp = SCENES[s.id];
        const body = <Comp t={localT(s)} dur={s.dur} />;
        if (role === 'solo' || !joinCfg) {
          return (
            <AbsoluteFill key={s.id} style={{zIndex: 1}}>
              {body}
            </AbsoluteFill>
          );
        }
        // A flash hides its swap under the blow-out: the OUTGOING shot stays on top
        // until the white peaks, then the incoming takes over while the white is
        // still burning off.
        const z =
          joinCfg.kind === 'flash'
            ? p < 0.5
              ? role === 'out'
                ? 2
                : 1
              : role === 'out'
                ? 1
                : 2
            : role === 'out'
              ? 1
              : 2;
        return (
          <JoinLayer key={`${s.id}-${role}`} join={joinCfg} role={role} p={p} z={z}>
            {body}
          </JoinLayer>
        );
      })}

      {/* captions ride on top of the join, never inside it */}
      {layers.map(({s, role, p}) => {
        const cards = captionCards(s.caption ?? '', s.dur);
        const lt = localT(s);
        const env = role === 'out' ? 1 - ramp(p, 0, 0.32) : role === 'in' ? ramp(p, 0.68, 1) : 1;
        return (
          <React.Fragment key={`cap-${s.id}`}>
            {cards.map((card, ci) => {
              // Cards hand over with a 4-frame overlap-free gap, so two captions
              // can never sit on top of each other.
              const from = card.from + 2;
              const to = card.to - 2;
              const fade = Math.min(
                interpolate(lt, [from, from + 4], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
                interpolate(lt, [to - 4, to], [1, 0], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
              );
              if (fade <= 0.001) return null;
              return (
                <div key={`cap-${s.id}-${ci}`} style={{zIndex: 40, opacity: fade * env}}>
                  <Caption text={card.text} opacity={1} />
                </div>
              );
            })}
          </React.Fragment>
        );
      })}

      {joinCfg && joinCfg.kind === 'flash' && active ? <FlashOverlay p={active.p} /> : null}

      <Vignette />
      <Grain />

      {/* frame one is an image, never black; only the very end fades */}
      <AbsoluteFill
        style={{
          zIndex: 60,
          backgroundColor: '#000',
          opacity: interpolate(frame, [durationInFrames - 6, durationInFrames - 1], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
