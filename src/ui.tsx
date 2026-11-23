import React from 'react';
import {AbsoluteFill, interpolate, Easing} from 'remotion';

export const W = 1920;
export const H = 1080;

/** Science/data palette held across every shot. */
export const C = {
  ink: '#05070F',
  night: '#0A1024',
  deep: '#111A3A',
  cyan: '#22D3EE',
  cyanDim: '#0E7490',
  magenta: '#E879F9',
  violet: '#7C5CFF',
  gold: '#FFD166',
  cream: '#F7F3EA',
  red: '#F2545B',
  green: '#4ADE80',
};

export const clamp01 = (v: number) => Math.min(1, Math.max(0, v));

export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

/** Smooth 0..1 ramp of `v` between `from` and `to`. */
export const ramp = (v: number, from: number, to: number, easing = Easing.inOut(Easing.cubic)) =>
  interpolate(v, [from, to], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });

/** A repeating 0..1 loop for continuous secondary motion (dust, packets, orbits). */
export const loop = (t: number, period: number, offset = 0) => {
  const v = ((t + offset) % period) / period;
  return v < 0 ? v + 1 : v;
};

/** The world: deep space, one slow starfield, one soft key light from upper left. */
export const Stage: React.FC<{t: number; children?: React.ReactNode}> = ({t, children}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 90% at 42% 30%, ${C.deep} 0%, ${C.night} 45%, ${C.ink} 100%)`,
    }}
  >
    <AbsoluteFill
      style={{
        opacity: 0.5,
        backgroundImage:
          'radial-gradient(#ffffff 1px, transparent 1.4px), radial-gradient(#8fd7ff 1px, transparent 1.5px)',
        backgroundSize: '180px 220px, 260px 300px',
        backgroundPosition: `${(t * 0.6) % 180}px ${(t * 0.9) % 220}px, ${(t * 0.35) % 260}px ${(t * 0.5) % 300}px`,
      }}
    />
    {children}
  </AbsoluteFill>
);

/** Every shot carries its own slow camera push, so no shot is ever a still. */
export const Shot: React.FC<{
  t: number;
  dur: number;
  push?: number;
  children: React.ReactNode;
}> = ({t, dur, push = 0.06, children}) => {
  const p = clamp01(t / dur);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${1 + push * p})`}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Blurred foreground element: the depth tell that reads as a real lens. */
export const Foreground: React.FC<{children: React.ReactNode}> = ({children}) => (
  <AbsoluteFill style={{filter: 'blur(26px)', opacity: 0.95}}>{children}</AbsoluteFill>
);

export const Grain: React.FC = () => (
  <AbsoluteFill
    style={{
      opacity: 0.05,
      mixBlendMode: 'overlay',
      backgroundImage:
        'radial-gradient(#ffffff 0.6px, transparent 0.7px), radial-gradient(#000000 0.6px, transparent 0.7px)',
      backgroundSize: '5px 5px, 7px 7px',
      backgroundPosition: '0 0, 3px 3px',
    }}
  />
);

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        'radial-gradient(78% 58% at 50% 46%, rgba(0,0,0,0) 40%, rgba(2,6,16,0.55) 100%)',
      pointerEvents: 'none',
    }}
  />
);
