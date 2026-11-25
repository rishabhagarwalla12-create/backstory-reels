"""Grid cover for a Backstory Daily reel.

The profile grid crops every reel to its centre 3:4 (y 240-1680 of 1080x1920), and the feed can crop
to 4:5 (y 285-1635), so everything sits inside y 330-1590. The headline is huge so the topic reads
at thumbnail size (a grid tile is ~1/3 of a phone's width).

usage:
  python3 cover.py OUT.jpg --kicker MONEY --title "Why the *rupee* keeps *falling*" [--bg reel.mp4 --t 4.0]
Words wrapped in *asterisks* are gold, the rest white. Keep titles to 3-6 words.
"""
import argparse, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
from reel import W, H, GOLD, WHITE, GREY, font, text_img, logo, base_bg  # noqa: E402

SAFE_X0, SAFE_X1 = 90, 990          # 900 px wide
TITLE_TOP, TITLE_BOT = 520, 1330     # headline block lives here


def background(bg, t):
    """Brand gradient, tinted by the reel's colours (heavily blurred so no shapes or text show)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.48) / H) ** 2)
    glow = np.clip(1 - r * 1.35, 0, 1) ** 1.7
    tint = np.array([1.0, 0.75, 0.32], np.float32)          # gold
    if bg:
        tmp = tempfile.mktemp(suffix='.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', bg, '-frames:v', '1', tmp], check=True)
        fr = np.asarray(Image.open(tmp).convert('RGB').resize((48, 85)).filter(ImageFilter.GaussianBlur(6)), np.float32)
        os.remove(tmp)
        c = fr.reshape(-1, 3).max(axis=0) + 1                # dominant bright colour of the frame
        tint = 0.6 * tint + 0.4 * (c / c.max())
    rng = np.random.default_rng(3); n = rng.normal(0, 2.2, (H, W)).astype(np.float32)
    img = 7 + glow[..., None] * 34 * tint[None, None, :] + n[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')


def parse(title):
    words = []
    for w in title.upper().split():
        words.append((w.replace('*', ''), '*' in w))
    return words


def layout(words, maxw=SAFE_X1 - SAFE_X0, maxh=TITLE_BOT - TITLE_TOP):
    for size in range(250, 100, -6):
        f = font('anton', size); sp = f.getlength(' ')
        lines, cur, curw = [], [], 0
        for w, g in words:
            ww = f.getlength(w)
            if cur and curw + sp + ww > maxw:
                lines.append(cur); cur, curw = [], 0
            curw = curw + (sp if cur else 0) + ww; cur.append((w, g))
        if cur: lines.append(cur)
        lh = int(size * 1.08)
        if len(lines) <= 4 and lh * len(lines) <= maxh and all(
                sum(f.getlength(w) for w, _ in ln) + sp * (len(ln) - 1) <= maxw for ln in lines):
            return size, lines, lh
    raise SystemExit('title too long: cut it to 3-6 words')


def make(out, title, kicker, bg=None, t=3.0):
    im = background(bg, t)
    d = ImageDraw.Draw(im)
    size, lines, lh = layout(parse(title))
    block = lh * len(lines)
    y = (TITLE_TOP + TITLE_BOT) // 2 - block // 2

    # kicker pill above the headline
    if kicker:
        kt = text_img(kicker.upper(), 'dms', 38, (12, 10, 6), 800, spacing=6)
        pw, ph = kt.width + 56, kt.height + 18
        px, py = W // 2 - pw // 2, y - ph - 46
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=ph // 2, fill=GOLD + (255,))
        im.alpha_composite(kt, (px + 28, py + 9 + 2))

    f = font('anton', size); sp = f.getlength(' ')
    for ln in lines:
        lw = sum(f.getlength(w) for w, _ in ln) + sp * (len(ln) - 1)
        x = W / 2 - lw / 2
        for w, g in ln:
            col = GOLD if g else WHITE
            # soft shadow for legibility
            sh = text_img(w, 'anton', size, (0, 0, 0)).filter(ImageFilter.GaussianBlur(8))
            im.alpha_composite(sh, (int(x) + 4, int(y) + 8))
            im.alpha_composite(text_img(w, 'anton', size, col), (int(x), int(y)))
            x += f.getlength(w) + sp
        y += lh

    # gold rule under the last line's glyphs + brand line, still inside the grid crop
    gb = y - lh + 3 + f.getbbox('A')[3]
    d.rectangle([W // 2 - 70, gb + 44, W // 2 + 70, gb + 50], fill=GOLD + (255,))
    lg = logo(58); bt = text_img('THE BACKSTORY DAILY', 'dms', 30, GOLD, 800, spacing=5)
    bw = lg.width + 12 + bt.width; bx = W // 2 - bw // 2; by = 1500
    im.alpha_composite(lg, (bx, by)); im.alpha_composite(bt, (bx + lg.width + 12, by + (lg.height - bt.height) // 2 + 3))

    im.convert('RGB').save(out, quality=90)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--title', required=True); ap.add_argument('--kicker', default='')
    ap.add_argument('--bg'); ap.add_argument('--t', type=float, default=3.0)
    a = ap.parse_args()
    print(make(a.out, a.title, a.kicker, a.bg, a.t))
