"""Shared toolkit for Backstory Daily reels: gold-on-black, 1080x1920, 30fps."""
import json, math, os, subprocess, functools
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
GOLD = (231, 184, 74); GOLD_D = (150, 112, 36); WHITE = (245, 242, 235)
GREY = (150, 146, 138); RED = (229, 72, 77); BLUE = (120, 190, 255); BG = (10, 10, 10)
ANTON = '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
DMS = '/usr/share/fonts/truetype/google-fonts/ofl/dmsans/DMSans[opsz,wght].ttf'

# ---------- easing ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, start, dur=0.35): return clamp((t - start) / dur)

# ---------- fonts / text ----------
@functools.lru_cache(maxsize=None)
def font(kind, size, weight=700):
    if kind == 'anton': return ImageFont.truetype(ANTON, size)
    f = ImageFont.truetype(DMS, size)
    f.set_variation_by_axes([min(40, max(9, size // 2)), weight])
    return f

@functools.lru_cache(maxsize=4096)
def text_img(text, kind='anton', size=120, color=WHITE, weight=700, spacing=0):
    f = font(kind, size, weight)
    if spacing:
        widths = [f.getlength(c) for c in text]
        tw = int(sum(widths) + spacing * (len(text) - 1)) + 4
        asc, desc = f.getmetrics(); th = asc + desc + 4
        im = Image.new('RGBA', (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 0
        for c, w in zip(text, widths):
            d.text((x, 0), c, font=f, fill=color + (255,)); x += w + spacing
        return im
    l, t, r, b = f.getbbox(text)
    asc, desc = f.getmetrics()
    im = Image.new('RGBA', (int(r - min(l, 0)) + 6, asc + desc + 6), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((3 - min(l, 0), 3), text, font=f, fill=color + (255,))
    return im

def wrap(text, kind, size, maxw, weight=700):
    f = font(kind, size, weight); words = text.split(); lines = []; cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if f.getlength(test) <= maxw or not cur: cur = test
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def paste(canvas, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0, anchor='c'):
    if alpha <= 0.003 or scale <= 0.01: return
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if abs(scale - 1) > 0.002:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if alpha < 0.999:
        a = im.getchannel('A').point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    if anchor == 'c': x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    elif anchor == 'l': x, y = int(cx), int(cy - im.height / 2)
    elif anchor == 'r': x, y = int(cx - im.width), int(cy - im.height / 2)
    canvas.alpha_composite(im, (x, y))

def text(canvas, s, cx, cy, kind='anton', size=120, color=WHITE, scale=1, alpha=1, rot=0, anchor='c', weight=700, spacing=0):
    paste(canvas, text_img(s, kind, size, color, weight, spacing), cx, cy, scale, alpha, rot, anchor)

def pop(canvas, s, cx, cy, t, start, size=120, color=WHITE, kind='anton', dur=0.4, weight=700, anchor='c'):
    p = prog(t, start, dur)
    if p <= 0: return
    text(canvas, s, cx, cy, kind, size, color, scale=0.6 + 0.4 * back(p), alpha=eo(p * 1.6), anchor=anchor, weight=weight)

def rise(canvas, s, cx, cy, t, start, size=60, color=WHITE, kind='dms', dur=0.45, weight=600, anchor='c'):
    p = prog(t, start, dur)
    if p <= 0: return
    text(canvas, s, cx, cy + 40 * (1 - eo(p)), kind, size, color, alpha=eo(p), anchor=anchor, weight=weight)

def stamp(canvas, s, cx, cy, t, start, size=110, color=RED, rot=-8, dur=0.3, box=True):
    p = prog(t, start, dur)
    if p <= 0: return
    im = text_img(s, 'anton', size, color)
    if box:
        pad = 26; b = Image.new('RGBA', (im.width + pad * 2, im.height + pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(b); d.rounded_rectangle([4, 4, b.width - 5, b.height - 5], radius=14, outline=color + (255,), width=9)
        b.alpha_composite(im, (pad, pad // 2 - 2)); im = b
    sc = 2.2 - 1.2 * eo(p)
    paste(canvas, im, cx, cy, scale=sc, alpha=eo(p * 1.5), rot=rot)

def overlay(canvas, fn, alpha=1.0):
    """Draw with ImageDraw on a transparent layer, then composite at alpha."""
    if alpha <= 0.003: return
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(lay), lay)
    if alpha < 0.999:
        a = lay.getchannel('A').point(lambda v: int(v * alpha)); lay.putalpha(a)
    canvas.alpha_composite(lay)

def rgba(c, a=255): return tuple(c[:3]) + (int(a),)

# ---------- logo ----------
@functools.lru_cache(maxsize=8)
def logo(size=120):
    q = text_img('?', 'anton', size, GOLD)
    im = q.copy(); d = ImageDraw.Draw(im)
    a = np.array(q.getchannel('A')); rows = np.where(a.max(axis=1) > 0)[0]
    # find the dot: last block of rows separated by a gap
    gaps = np.where(np.diff(rows) > 1)[0]
    if len(gaps):
        top = rows[gaps[-1] + 1]; bot = rows[-1]
        cols = np.where(a[top:bot + 1].max(axis=0) > 0)[0]; l, r = cols[0], cols[-1]
        cx, cy = (l + r) / 2, (top + bot) / 2; rad = max(r - l, bot - top) / 2 * 1.25
        d.ellipse([cx - rad - 2, cy - rad - 2, cx + rad + 2, cy + rad + 2], fill=(0, 0, 0, 0))
        im2 = Image.new('RGBA', im.size, (0, 0, 0, 0)); im2.alpha_composite(im)
        # clear dot area, then draw globe
        arr = np.array(im2); yy, xx = np.ogrid[:arr.shape[0], :arr.shape[1]]
        mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= (rad + 3) ** 2; arr[mask] = 0; im2 = Image.fromarray(arr)
        d2 = ImageDraw.Draw(im2); lw = max(2, int(size / 45))
        d2.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=GOLD + (255,), width=lw)
        d2.ellipse([cx - rad * .45, cy - rad, cx + rad * .45, cy + rad], outline=GOLD + (255,), width=max(1, lw - 1))
        d2.line([cx - rad, cy, cx + rad, cy], fill=GOLD + (255,), width=max(1, lw - 1))
        d2.line([cx, cy - rad, cx, cy + rad], fill=GOLD + (255,), width=max(1, lw - 1))
        return im2
    return im

# ---------- background ----------
@functools.lru_cache(maxsize=1)
def base_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.42) / H) ** 2)
    v = np.clip(1 - r * 1.25, 0, 1) ** 1.6
    rng = np.random.default_rng(7); n = rng.normal(0, 3.0, (H, W)).astype(np.float32)
    img = np.zeros((H, W, 3), np.float32)
    img[..., 0] = 8 + 22 * v + n; img[..., 1] = 8 + 16 * v + n; img[..., 2] = 8 + 7 * v + n
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
    # brand header
    lg = logo(64); im.alpha_composite(lg, (int(W / 2 - 250), 92))
    t = text_img('THE BACKSTORY DAILY', 'dms', 34, GOLD, 800, spacing=6)
    im.alpha_composite(t, (int(W / 2 - 250 + lg.width + 14), 92 + (lg.height - t.height) // 2 + 4))
    return im

def frame_base(gt, total):
    c = base_bg().copy(); d = ImageDraw.Draw(c)
    # progress bar under header
    d.rectangle([80, 196, W - 80, 199], fill=(40, 34, 22, 255))
    d.rectangle([80, 196, 80 + int((W - 160) * clamp(gt / total)), 199], fill=GOLD + (255,))
    return c

def caption(canvas, s, alpha=1.0):
    if not s or alpha <= 0: return
    lines = wrap(s, 'dms', 42, 820, 600)
    lh = 56; h = lh * len(lines) + 30; y0 = 1460
    def fn(d, lay):
        d.rounded_rectangle([110, y0, W - 110, y0 + h], radius=22, fill=(0, 0, 0, 150))
    overlay(canvas, fn, alpha)
    for i, l in enumerate(lines):
        text(canvas, l, W / 2, y0 + 15 + lh * i + lh / 2, 'dms', 42, WHITE, alpha=alpha, weight=600)

# ---------- shapes ----------
def envelope(d, cx, cy, w, h, col=GOLD, fill=(24, 20, 12, 255), open_=0.0, lw=7):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=fill, outline=col + (255,), width=lw)
    fy = y0 + (h * 0.55) * (1 - 2 * open_)
    d.line([(x0 + 6, y0 + 6), (cx, fy), (x1 - 6, y0 + 6)], fill=col + (255,), width=lw, joint='curve')

def check(d, cx, cy, s, col=GOLD, lw=12):
    d.line([(cx - s * .5, cy), (cx - s * .12, cy + s * .38), (cx + s * .55, cy - s * .42)], fill=col + (255,), width=lw, joint='curve')

def cross(d, cx, cy, s, col=RED, lw=12):
    d.line([(cx - s / 2, cy - s / 2), (cx + s / 2, cy + s / 2)], fill=col + (255,), width=lw)
    d.line([(cx - s / 2, cy + s / 2), (cx + s / 2, cy - s / 2)], fill=col + (255,), width=lw)

# ---------- timeline + render ----------
class Timeline:
    def __init__(self, lines, durs, scenes, gap=0.18, scene_gap=0.32, lead=0.25, tail=2.2):
        self.text = dict(lines); self.start = {}; self.durs = durs; self.scenes = []
        t = lead
        for si, (name, keys) in enumerate(scenes):
            s0 = t if si else 0.0
            for i, k in enumerate(keys):
                self.start[k] = t; t += durs[k] + (gap if i < len(keys) - 1 else 0)
            t += scene_gap
            self.scenes.append((name, s0, keys))
        self.total = t + tail
        # scene boundaries
        b = [s[1] for s in self.scenes] + [self.total]
        self.bounds = [(self.scenes[i][0], b[i], b[i + 1]) for i in range(len(self.scenes))]
    def cue(self, k, scene_start): return self.start[k] - scene_start
    def line_at(self, gt):
        cur = None
        for k, s in self.start.items():
            if gt >= s - 0.05 and gt <= s + self.durs[k] + 0.25: cur = k
        return cur

def render_scene(path, n_frames, draw_frame):
    tmp = path[:-4] + '.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
    for i in range(n_frames):
        im = draw_frame(i)
        p.stdin.write(im.convert('RGB').tobytes())
    p.stdin.close(); rc = p.wait()
    if rc == 0: os.replace(tmp, path)
    return rc
