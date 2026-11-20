"""Synthesized music + SFX + voice mix for reels (no licensed audio)."""
import numpy as np, soundfile as sf
SR = 48000

def _env(n, a=0.01, r=0.3):
    e = np.ones(n); na = int(a * SR); nr = int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] = np.linspace(1, 0, nr)
    return e

def _lp(x, alpha):
    y = np.empty_like(x); acc = 0.0
    # vectorised one-pole via cumulative trick is unstable; use simple loop in chunks via scipy if present
    try:
        from scipy.signal import lfilter
        return lfilter([alpha], [1, alpha - 1], x)
    except Exception:
        for i, v in enumerate(x): acc += alpha * (v - acc); y[i] = acc
        return y

def music(total, seed=1, bpm=96, key=57):
    """Soft minor pad + pluck arpeggio + light kick. key = MIDI root (57 = A3)."""
    rng = np.random.default_rng(seed)
    n = int(total * SR); out = np.zeros((n, 2))
    beat = 60 / bpm; bar = beat * 4
    prog = [[0, 3, 7], [-4, 0, 3], [-9, -5, 0], [-2, 2, 5]]  # i - VI - III - VII (minor)
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    t = np.arange(n) / SR
    for bi in range(int(total / bar) + 1):
        ch = prog[bi % 4]; s0 = int(bi * bar * SR); s1 = min(n, int((bi + 1) * bar * SR) + int(0.4 * SR))
        if s0 >= n: break
        tt = t[s0:s1] - t[s0]; e = np.minimum(1, tt / 0.6) * np.exp(-np.maximum(0, tt - bar) * 6)
        pad = sum(np.sin(2 * np.pi * f(key + iv - 12) * tt * (1 + d)) for iv in ch for d in (-0.002, 0.002)) / 6
        out[s0:s1, 0] += 0.10 * pad * e; out[s0:s1, 1] += 0.10 * pad * e
        # arpeggio 8ths
        for k in range(8):
            a0 = s0 + int(k * beat / 2 * SR)
            if a0 >= n: break
            nn = int(0.35 * SR); a1 = min(n, a0 + nn); ta = np.arange(a1 - a0) / SR
            note = key + ch[k % 3] + (12 if k % 4 == 3 else 0)
            pl = np.sin(2 * np.pi * f(note) * ta) * np.exp(-ta * 9) * 0.06
            pan = 0.35 + 0.3 * (k % 2)
            out[a0:a1, 0] += pl * (1 - pan); out[a0:a1, 1] += pl * pan
        # kick on beats 1 and 3
        for k in (0, 2):
            a0 = s0 + int(k * beat * SR); nn = int(0.25 * SR); a1 = min(n, a0 + nn)
            if a0 >= n: break
            ta = np.arange(a1 - a0) / SR
            kk = np.sin(2 * np.pi * (45 + 70 * np.exp(-ta * 30)) * ta) * np.exp(-ta * 14) * 0.18
            out[a0:a1] += kk[:, None]
    # fade
    fi = int(1.0 * SR); fo = int(1.5 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]; out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return out

def sfx(kind):
    rng = np.random.default_rng(len(kind))
    if kind == 'hit':
        n = int(0.5 * SR); t = np.arange(n) / SR
        x = np.sin(2 * np.pi * (50 + 90 * np.exp(-t * 25)) * t) * np.exp(-t * 7) * 0.55
        x += _lp(rng.normal(0, 1, n), 0.25) * np.exp(-t * 30) * 0.25
    elif kind == 'whoosh':
        n = int(0.45 * SR); t = np.arange(n) / SR
        noise = rng.normal(0, 1, n); a = 0.02 + 0.25 * np.sin(np.pi * t / t[-1])
        x = _lp(noise, 0.12) * np.sin(np.pi * t / t[-1]) ** 2 * 0.35
    elif kind == 'tick':
        n = int(0.08 * SR); t = np.arange(n) / SR
        x = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 80) * 0.18
    elif kind == 'stamp':
        n = int(0.4 * SR); t = np.arange(n) / SR
        x = _lp(rng.normal(0, 1, n), 0.35) * np.exp(-t * 22) * 0.5 + np.sin(2 * np.pi * 80 * t) * np.exp(-t * 18) * 0.45
    elif kind == 'rise':
        n = int(1.2 * SR); t = np.arange(n) / SR
        x = (_lp(rng.normal(0, 1, n), 0.18) * (t / t[-1]) ** 2 * 0.25 + np.sin(2 * np.pi * (200 + 600 * t / t[-1]) * t) * (t / t[-1]) ** 3 * 0.05)
    return np.stack([x, x], 1)

def build(total, voice, events, out_full, out_voice, seed=1):
    """voice: list of (start_sec, wav_path); events: list of (start_sec, kind)."""
    n = int(total * SR); v = np.zeros((n, 2))
    for st, p in voice:
        s, sr = sf.read(p)
        if sr != SR:
            idx = np.arange(0, len(s), sr / SR); s = np.interp(idx, np.arange(len(s)), s)
        if s.ndim == 1: s = np.stack([s, s], 1)
        a = int(st * SR); b = min(n, a + len(s)); v[a:b] += s[:b - a] * 0.95
    fx = np.zeros((n, 2))
    for st, k in events:
        x = sfx(k); a = int(st * SR); b = min(n, a + len(x))
        if a < n: fx[a:b] += x[:b - a] * 0.55
    m = music(total, seed)
    # duck music under voice
    env = np.abs(v[:, 0]); win = int(0.25 * SR)
    sm = np.convolve(env, np.ones(win) / win, mode='same')
    duck = 1 - 0.6 * np.clip(sm / (sm.max() * 0.15 + 1e-9), 0, 1)
    full = v + fx + m * duck[:, None] * 1.1
    vo = v + fx
    for arr, p in ((full, out_full), (vo, out_voice)):
        pk = np.abs(arr).max(); arr = arr / pk * 0.89 if pk > 0.89 else arr
        sf.write(p, arr.astype(np.float32), SR)
