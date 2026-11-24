import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, H, clamp01, lerp, loop, ramp, Shot, Stage, W} from './ui';
import shotsJson from './shots.json';

export type SceneProps = {t: number; dur: number};

type ShotData = {template: string; props: any; accent: string; chapter: number; chapterTitle: string};

const ACCENT: Record<string, string> = {
  cyan: C.cyan,
  magenta: C.magenta,
  violet: C.violet,
  gold: C.gold,
  green: C.green,
  red: C.red,
};

/** A particle: four concentric discs, no gradients, so ids can never collide. */
const Halo: React.FC<{x: number; y: number; r: number; color: string; opacity?: number}> = ({
  x, y, r, color, opacity = 1,
}) => (
  <>
    <circle cx={x} cy={y} r={r * 3.4} fill={color} opacity={0.05 * opacity} />
    <circle cx={x} cy={y} r={r * 2.1} fill={color} opacity={0.1 * opacity} />
    <circle cx={x} cy={y} r={r * 1.45} fill={color} opacity={0.18 * opacity} />
    <circle cx={x} cy={y} r={r} fill={color} opacity={0.95 * opacity} />
    <circle cx={x - r * 0.3} cy={y - r * 0.32} r={r * 0.3} fill="#ffffff" opacity={0.7 * opacity} />
  </>
);

const Dust: React.FC<{t: number; n?: number; color?: string}> = ({t, n = 18, color = '#9fe8ff'}) => (
  <>
    {Array.from({length: n}).map((_, i) => {
      const q = loop(t, 160 + (i % 5) * 45, i * 37);
      const x = 60 + ((i * 233) % 1800);
      const y = 1060 - q * 980;
      return <circle key={i} cx={x} cy={y} r={2 + (i % 3)} fill={color} opacity={0.12 + 0.2 * Math.sin(q * Math.PI)} />;
    })}
  </>
);

const T: React.FC<{x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'; weight?: number; children: string}> = ({
  x, y, size = 44, color = C.cream, anchor = 'middle', weight = 800, children,
}) => (
  <text x={x} y={y} fill={color} fontSize={size} fontFamily='Helvetica, Arial, "DejaVu Sans", "Noto Sans Devanagari", "Lohit Devanagari", sans-serif'
    fontWeight={weight} letterSpacing={1} textAnchor={anchor}>
    {children}
  </text>
);

/* ------------------------------------------------------------------ card */
const Card: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const a = ramp(t, 0, dur * 0.35);
  const accent = ACCENT[s.accent] ?? C.cyan;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} />
      <rect x={0} y={0} width={8} height={H} fill={accent} opacity={0.7 * a} />
      <T x={230} y={640} size={300} color={accent} anchor="start">{String(s.props.n)}</T>
      <T x={620} y={520} size={82} color={C.cream} anchor="start">{s.props.title}</T>
      <rect x={620} y={560} width={160 * a} height={6} fill={accent} />
      <T x={620} y={640} size={40} color="#9fb2e0" anchor="start">{s.props.sub}</T>
    </svg>
  );
};

/* ----------------------------------------------------------------- quote */
const Quote: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const a = ramp(t, 0, dur * 0.3);
  const accent = ACCENT[s.accent] ?? C.cyan;
  const drift = Math.sin(t / 22) * 8;
  const line = String(s.props.line ?? '');
  const size = line.length > 26 ? 68 : 88;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} />
      <rect x={W / 2 - 90 * a} y={400} width={180 * a} height={5} fill={accent} opacity={0.9} />
      <T x={W / 2 + drift} y={540} size={size} color={C.cream}>{line}</T>
      <rect x={W / 2 - 90 * a} y={600} width={180 * a} height={5} fill={accent} opacity={0.9} />
    </svg>
  );
};

/* ----------------------------------------------------------------- board */
const Board: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const accent = ACCENT[s.accent] ?? C.cyan;
  const lines: string[] = s.props.lines ?? [];
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} n={12} />
      <T x={170} y={250} size={62} color={accent} anchor="start">{s.props.title}</T>
      <rect x={172} y={282} width={140} height={5} fill={accent} opacity={0.8} />
      {lines.map((l, i) => {
        const a = ramp(t, dur * (0.1 + i * 0.12), dur * (0.28 + i * 0.12));
        const y = 430 + i * 130;
        return (
          <g key={i} opacity={a}>
            <rect x={176} y={y - 26} width={22} height={22} rx={5} fill={accent} opacity={0.9} />
            <T x={232} y={y} size={52} color={C.cream} anchor="start">{l}</T>
          </g>
        );
      })}
    </svg>
  );
};

/* ------------------------------------------------------------------ pair */
const Pair: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const accent = ACCENT[s.accent] ?? C.cyan;
  const breathe = 0.5 + 0.5 * Math.sin(t / 9);
  const grow = ramp(t, 0, dur * 0.4);
  const lx = 520;
  const rx = 1400;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} />
      <ellipse cx={W / 2} cy={470} rx={lerp(120, 560, grow)} ry={lerp(90, 240, grow) + breathe * 8}
        fill={accent} opacity={0.07} />
      <ellipse cx={W / 2} cy={470} rx={lerp(120, 560, grow)} ry={lerp(90, 240, grow) + breathe * 8}
        fill="none" stroke={accent} strokeWidth={3} opacity={0.35} />
      <line x1={lx + 70} y1={470} x2={rx - 70} y2={470} stroke={C.cream} strokeWidth={3}
        strokeDasharray="14 12" opacity={0.35 * grow} />
      <Halo x={lx} y={470} r={52 + breathe * 4} color={C.cyan} />
      <Halo x={rx} y={470} r={52 + breathe * 4} color={C.magenta} />
      <T x={lx} y={400} size={54} color={C.cyan}>{String(s.props.left ?? 'A')}</T>
      <T x={rx} y={400} size={54} color={C.magenta}>{String(s.props.right ?? 'B')}</T>
      <T x={W / 2} y={680} size={40} color="#9fb2e0">{String(s.props.mid ?? '')}</T>
    </svg>
  );
};

/* --------------------------------------------------------------- formula */
const Formula: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const a = ramp(t, dur * 0.08, dur * 0.4);
  const accent = ACCENT[s.accent] ?? C.cyan;
  const eq = String(s.props.eq ?? '');
  // Size the formula to the box, not to a character-count guess: the box is
  // 840 wide, so a long equation at a fixed size spills past the border.
  const INNER = 760;
  const eqLen = Math.max(1, eq.length);
  const size = Math.max(40, Math.min(84, Math.floor(INNER / (0.6 * eqLen))));
  const estWidth = 0.6 * eqLen * size;
  const squeeze = estWidth > INNER ? {textLength: INNER, lengthAdjust: 'spacingAndGlyphs' as const} : {};
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} n={12} />
      <rect x={W / 2 - 420} y={330} width={840} height={260} rx={28} fill="#0d1730" stroke={accent}
        strokeWidth={4} opacity={0.4 + 0.6 * a} />
      <text x={W / 2} y={492} fill={accent} fontSize={size} textAnchor="middle"
        fontFamily='Helvetica, Arial, "DejaVu Sans", "Noto Sans Devanagari", "Lohit Devanagari", sans-serif' fontWeight={800} letterSpacing={1} {...squeeze}>
        {eq}
      </text>
      <T x={W / 2} y={660} size={38} color="#9fb2e0">{String(s.props.note ?? '')}</T>
    </svg>
  );
};

/* ----------------------------------------------------------------- chart */
const Chart: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const limit = Number(s.props.limit ?? 2);
  const peak = Number(s.props.peak ?? 2.83);
  const measured = s.props.measured == null ? null : Number(s.props.measured);
  const X = (v: number) => 260 + (v / 3) * 1400;
  const Y = 780;
  const dot = ramp(t, dur * 0.2, dur * 0.8);
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} n={10} />
      <line x1={220} y1={Y} x2={1700} y2={Y} stroke={C.cream} strokeWidth={4} opacity={0.4} />
      {[0, 1, 2, 3].map((v) => (
        <g key={v}>
          <line x1={X(v)} y1={Y} x2={X(v)} y2={Y + 18} stroke={C.cream} strokeWidth={3} opacity={0.35} />
          <T x={X(v)} y={Y + 66} size={34} color="#8fa3c8">{String(v)}</T>
        </g>
      ))}
      <line x1={X(limit)} y1={Y - 30} x2={X(limit)} y2={300} stroke={C.red} strokeWidth={6} strokeDasharray="16 12" />
      <T x={X(limit)} y={270} size={40} color={C.red}>LIMIT 2</T>
      <line x1={X(peak)} y1={Y - 30} x2={X(peak)} y2={250} stroke={C.cyan} strokeWidth={6} opacity={0.85} />
      <T x={X(peak)} y={220} size={40} color={C.cyan}>2.83</T>
      {measured != null ? (
        <g opacity={dot}>
          <Halo x={X(lerp(0.2, measured, dot))} y={Y - 110} r={34} color={C.gold} />
          <T x={X(lerp(0.2, measured, dot))} y={Y - 180} size={34} color={C.gold}>S</T>
        </g>
      ) : null}
    </svg>
  );
};

/* -------------------------------------------------------------- timeline */
const Timeline: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const years: [string, string][] = s.props.years ?? [];
  const at = Number(s.props.at ?? 0);
  const accent = ACCENT[s.accent] ?? C.cyan;
  const y = 470;
  const step = years.length > 1 ? 1400 / (years.length - 1) : 0;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} n={10} />
      <line x1={260} y1={y} x2={1660} y2={y} stroke={C.cream} strokeWidth={3} opacity={0.3} />
      {years.map(([yr, label], i) => {
        const x = 260 + i * step;
        const on = i === at;
        const a = ramp(t, dur * (0.1 + i * 0.12), dur * (0.3 + i * 0.12));
        return (
          <g key={yr} opacity={a}>
            <circle cx={x} cy={y} r={on ? 26 : 14} fill={on ? accent : '#4a5a80'} />
            {on ? <circle cx={x} cy={y} r={26 + 10 * Math.sin(t / 8)} fill="none" stroke={accent} strokeWidth={3} opacity={0.6} /> : null}
            <T x={x} y={y - 60} size={on ? 58 : 40} color={on ? accent : '#9fb2e0'}>{yr}</T>
            <T x={x} y={y + 80} size={34} color={on ? C.cream : '#7f8db0'}>{label}</T>
          </g>
        );
      })}
    </svg>
  );
};

/* ------------------------------------------------------------------- rig */
const Rig: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const accent = ACCENT[s.accent] ?? C.cyan;
  const on = ramp(t, dur * 0.1, dur * 0.35);
  const spin = t * 22;
  const fly = loop(t, 44);
  const Node: React.FC<{x: number; label: string; color: string}> = ({x, label, color}) => (
    <g opacity={on}>
      <rect x={x - 160} y={620} width={320} height={230} rx={26} fill="#0d1730" stroke={color} strokeWidth={5} />
      <g transform={`translate(${x} 735) rotate(${spin})`}>
        <rect x={-100} y={-12} width={200} height={24} rx={12} fill={color} opacity={0.8} />
        <rect x={-12} y={-100} width={24} height={200} rx={12} fill={color} opacity={0.4} />
      </g>
      <T x={x} y={910} size={34} color="#9fb2e0">{label}</T>
    </g>
  );
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} n={12} />
      <Halo x={W / 2} y={230} r={34} color={accent} />
      <T x={W / 2} y={150} size={34} color="#c8b98a">SOURCE</T>
      {[520, 1400].map((x, i) => (
        <line key={x} x1={W / 2} y1={270} x2={x} y2={610} stroke={i ? C.magenta : C.cyan} strokeWidth={5} opacity={0.35 * on} />
      ))}
      {[520, 1400].map((x, i) => {
        const q = fly;
        return <Halo key={`f${x}`} x={lerp(W / 2, x, q)} y={lerp(270, 600, q)} r={16}
          color={i ? C.magenta : C.cyan} opacity={on} />;
      })}
      <Node x={520} label={String(s.props.left ?? 'A')} color={C.cyan} />
      <Node x={1400} label={String(s.props.right ?? 'B')} color={C.magenta} />
    </svg>
  );
};

/* --------------------------------------------------------------- channel */
const Channel: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const accent = ACCENT[s.accent] ?? C.gold;
  const a = ramp(t, dur * 0.05, dur * 0.3);
  const packet = loop(t, 80);
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} n={12} />
      <g opacity={a}>
        <rect x={220} y={330} width={340} height={240} rx={26} fill="#0d1730" stroke={C.cyan} strokeWidth={5} />
        <T x={390} y={470} size={44} color={C.cyan}>{String(s.props.left ?? 'A')}</T>
        <rect x={1360} y={330} width={340} height={240} rx={26} fill="#0d1730" stroke={C.magenta} strokeWidth={5} />
        <T x={1530} y={470} size={44} color={C.magenta}>{String(s.props.right ?? 'B')}</T>
      </g>
      <line x1={580} y1={720} x2={1340} y2={720} stroke={C.cream} strokeWidth={4} strokeDasharray="18 14" opacity={0.45} />
      <rect x={lerp(580, 1250, packet)} y={690} width={64} height={64} rx={14} fill={accent} />
      <T x={960} y={620} size={36} color={accent}>{String(s.props.note ?? '')}</T>
    </svg>
  );
};

/* ----------------------------------------------------------------- three */
const Three: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const items: string[] = s.props.items ?? [];
  const accent = ACCENT[s.accent] ?? C.cyan;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} color={accent} n={12} />
      {items.map((it, i) => {
        const a = ramp(t, dur * (0.08 + i * 0.12), dur * (0.3 + i * 0.12));
        const w = items.length > 3 ? 330 : 460;
        const gap = 60;
        const total = items.length * w + (items.length - 1) * gap;
        const x = (W - total) / 2 + i * (w + gap);
        return (
          <g key={it} opacity={a}>
            <rect x={x} y={380} width={w} height={220} rx={26} fill="#0d1730" stroke={accent} strokeWidth={4} opacity={0.95} />
            <T x={x + w / 2} y={510} size={items.length > 3 ? 40 : 44} color={accent}>{it}</T>
          </g>
        );
      })}
      <T x={W / 2} y={700} size={36} color="#9fb2e0">{String(s.props.note ?? '')}</T>
    </svg>
  );
};

/* ---------------------------------------------------------------- levels */
const Levels: React.FC<{s: ShotData; t: number; dur: number}> = ({s, t, dur}) => {
  const items: string[] = s.props.items ?? [];
  const accent = ACCENT[s.accent] ?? C.violet;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
      <Dust t={t} n={12} />
      {items.map((it, i) => {
        const a = ramp(t, dur * (0.06 + i * 0.14), dur * (0.28 + i * 0.14));
        const y = 260 + i * 170;
        const last = i === items.length - 1;
        return (
          <g key={it} opacity={a}>
            <rect x={230} y={y} width={1460} height={130} rx={24} fill={last ? '#17233f' : '#0d1730'}
              stroke={last ? accent : '#2a3a60'} strokeWidth={4} />
            <T x={300} y={y + 86} size={54} color={last ? accent : '#7f8db0'}>{String(i + 1)}</T>
            <T x={420} y={y + 84} size={44} color={last ? accent : C.cream} anchor="start">{it}</T>
          </g>
        );
      })}
      <T x={W / 2} y={840} size={34} color="#9fb2e0">{String(s.props.note ?? '')}</T>
    </svg>
  );
};

const RENDER: Record<string, React.FC<{s: ShotData; t: number; dur: number}>> = {
  card: Card,
  quote: Quote,
  board: Board,
  pair: Pair,
  formula: Formula,
  chart: Chart,
  timeline: Timeline,
  rig: Rig,
  channel: Channel,
  three: Three,
  levels: Levels,
};

const SHOTS = (shotsJson as unknown as {shots: Record<string, ShotData>}).shots;

const ShotView: React.FC<{s: ShotData} & SceneProps> = ({s, t, dur}) => {
  const Comp = RENDER[s.template] ?? Quote;
  return (
    <Shot t={t} dur={dur} push={0.05}>
      <Stage t={t}>
        <Comp s={s} t={t} dur={dur} />
      </Stage>
    </Shot>
  );
};

export const SCENES: Record<string, React.FC<SceneProps>> = Object.fromEntries(
  Object.entries(SHOTS).map(([id, s]) => [id, (p: SceneProps) => <ShotView s={s} t={p.t} dur={p.dur} />]),
);
