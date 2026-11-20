import sys, json, math
sys.path.insert(0, '/home/claude/lib')
from reel import *

LINES = json.load(open('/home/claude/tts/tender.json'))
DURS = json.load(open('/home/claude/tender/vo/durs.json'))
SCENES = [('shop', ['a1', 'a2']), ('how', ['b1']), ('tender', ['c1', 'c2']), ('env', ['d1', 'd2', 'd3']),
          ('l1', ['e1', 'e2']), ('bribe', ['f1', 'f2', 'f3', 'f4']), ('cartel', ['g1', 'g2']), ('trail', ['h1', 'h2'])]
T = Timeline(LINES, DURS, SCENES, gap=0.14, scene_gap=0.26, tail=2.0)
CAP = dict(LINES)
CAP['e2'] = "The lowest price wins. It's called L1."
CAP['a2'] = "From pens to bridges, ₹5 lakh crore went through one government website last year."
CAP['f4'] = "In March, it says it caught a senior engineer accepting ₹10 lakh. The alleged ask? 1% of a ₹40 crore tender."

def src(c, s, alpha=1):
    text(c, s, W / 2, 1385, 'dms', 30, GREY, alpha=alpha, weight=500)

# ---------------- scenes ----------------
def s_shop(c, t, cu):
    # icons: pen, laptop, bridge
    def icons(d, lay):
        for i, (x, k) in enumerate([(300, 'pen'), (540, 'laptop'), (780, 'bridge')]):
            p = eo(prog(t, 0.15 + i * 0.25, 0.4)); y = 640 + 40 * (1 - p); a = int(255 * p)
            col = GOLD + (a,)
            if k == 'pen':
                d.line([(x - 60, y + 70), (x + 55, y - 60)], fill=col, width=22)
                d.polygon([(x - 60, y + 70), (x - 80, y + 95), (x - 48, y + 80)], fill=col)
            elif k == 'laptop':
                d.rounded_rectangle([x - 85, y - 70, x + 85, y + 40], radius=10, outline=col, width=10)
                d.rectangle([x - 110, y + 50, x + 110, y + 66], fill=col)
            else:
                d.arc([x - 110, y - 60, x + 110, y + 140], 200, 340, fill=col, width=12)
                d.line([(x - 120, y + 50), (x + 120, y + 50)], fill=col, width=12)
                for k2 in (-60, 0, 60): d.line([(x + k2, y + 50), (x + k2, y - 30 + abs(k2) * .35)], fill=col, width=8)
    a_out = 1 - eo(prog(t, cu['a2'] - 0.2, 0.3)) * 0.0
    overlay(c, icons, a_out)
    pop(c, 'GIANT SHOPPER', W / 2, 430, t, 0.05, 130, WHITE)
    # counter
    t0 = cu['a2'] + 0.9
    if t >= t0 - 0.3:
        v = 5.03 * eo(prog(t, t0, 1.6))
        text(c, f'₹{v:.2f}', W / 2, 960, 'anton', 230, GOLD, scale=0.8 + 0.2 * eo(prog(t, t0 - 0.3, 0.4)), alpha=eo(prog(t, t0 - 0.3, 0.3)))
        rise(c, 'LAKH CRORE', W / 2, 1120, t, t0 + 0.2, 90, WHITE, 'anton', weight=400)
        rise(c, 'through GeM, the govt\'s buying website, in FY26', W / 2, 1215, t, t0 + 0.6, 40, GREY, weight=500)
        src(c, 'Source: Commerce Ministry / GeM, Apr 2026', eo(prog(t, t0 + 0.8)))

def s_how(c, t, cu):
    for i, l in enumerate(['HOW DO', 'BUSINESSES', 'WIN THESE', 'ORDERS?']):
        pop(c, l, W / 2, 470 + i * 165, t, 0.05 + i * 0.22, 165, WHITE if i != 2 else GOLD)
    p = prog(t, 1.0, 0.5)
    if p > 0:
        paste(c, logo(240), W / 2, 1230, scale=0.5 + 0.5 * back(p), alpha=eo(p), rot=6 * math.sin(t * 2))

def s_tender(c, t, cu):
    # small buy card
    p = eo(prog(t, 0.05, 0.4))
    def card(d, lay):
        d.rounded_rectangle([120, 400, 960, 640], radius=26, fill=(26, 22, 14, 255), outline=GOLD_D + (255,), width=4)
    overlay(c, card, p)
    text(c, 'SMALL BUY', 170, 470, 'anton', 80, WHITE, alpha=p, anchor='l')
    rise(c, '→  officials order directly', 172, 575, t, 0.6, 46, GOLD, anchor='l')
    # notice sheet
    q = prog(t, cu['c2'], 0.5)
    if q > 0:
        y = 1040 + 300 * (1 - eo(q))
        def sheet(d, lay):
            d.rounded_rectangle([200, y - 280, 880, y + 280], radius=18, fill=(240, 234, 220, 255))
            for i in range(6): d.rectangle([260, y - 40 + i * 50, 820 - (i % 3) * 90, y - 22 + i * 50], fill=(190, 182, 165, 255))
        overlay(c, sheet, eo(q))
        text(c, 'BIG BUY = TENDER', W / 2, y - 210, 'anton', 74, (20, 18, 14), alpha=eo(q))
        text(c, 'PUBLIC NOTICE · OPEN TO ALL', W / 2, y - 125, 'dms', 34, (120, 90, 30), alpha=eo(q), weight=800, spacing=2)
        stamp(c, 'OPEN TO BID', 760, y + 210, t, cu['c2'] + 1.6, 64, GOLD_D, rot=-10)

def s_env(c, t, cu):
    pop(c, '2 ENVELOPES', W / 2, 420, t, 0.05, 140, WHITE)
    for i, (k, lab, sub) in enumerate([('d2', '1 · TECHNICAL', 'Can you do the job?'), ('d3', '2 · FINANCIAL', 'Your price')]):
        cy = 760 + i * 420; p = eo(prog(t, 0.35 + i * 0.25, 0.45))
        hi = prog(t, cu[k], 0.3)
        col = GOLD if hi > 0 else GOLD_D
        overlay(c, lambda d, lay, cy=cy, col=col: envelope(d, W / 2 - 200 + 0, cy, 300, 200, col), p)
        text(c, lab, 620, cy - 35, 'anton', 72, WHITE if hi > 0 else GREY, alpha=p, anchor='l')
        if hi > 0: rise(c, sub, 622, cy + 50, t, cu[k] + 0.1, 46, GOLD, anchor='l')
    if t > cu['d2']:
        rise(c, 'turnover · past work · documents', W / 2, 1010, t, cu['d2'] + 0.6, 36, GREY, weight=500)

BIDS = [('Firm A', 48.2), ('Firm B', 45.9), ('Firm C', 42.7), ('Firm D', 44.1)]
def s_l1(c, t, cu):
    pop(c, 'PRICES OPENED', W / 2, 420, t, 0.05, 120, WHITE)
    text(c, 'example', W / 2, 515, 'dms', 34, GREY, alpha=eo(prog(t, 0.3)), weight=500)
    win = prog(t, cu['e2'] + 0.2, 0.35)
    for i, (n, v) in enumerate(BIDS):
        y = 650 + i * 150; p = eo(prog(t, 0.6 + i * 0.18, 0.6))
        L = int(450 * (v / 50) * p); best = (n == 'Firm C')
        col = GOLD if (best and win > 0) else (90, 84, 74)
        def bar(d, lay, y=y, L=L, col=col):
            d.rounded_rectangle([300, y - 42, 300 + max(L, 20), y + 42], radius=14, fill=col + (255,))
        overlay(c, bar, eo(prog(t, 0.6 + i * 0.18, 0.2)))
        text(c, n, 270, y, 'dms', 44, WHITE, alpha=p, anchor='r', weight=700)
        if p > 0.5: text(c, f'₹{v} lakh', 300 + L + 24, y, 'dms', 44, WHITE if not (best and win > 0) else GOLD, alpha=eo((p - .5) * 2), anchor='l', weight=700)
    stamp(c, 'L1 WINS', W / 2, 1290, t, cu['e2'] + 0.5, 130, GOLD, rot=-6)

def s_bribe(c, t, cu):
    # f1 title
    a1 = 1 - eo(prog(t, cu['f3'] - 0.25, 0.3))
    if a1 > 0:
        p = prog(t, 0.05, 0.4)
        text(c, 'THE BRIBE', W / 2, 560, 'anton', 210, RED, scale=0.6 + 0.4 * back(p), alpha=eo(p) * a1)
        if t > cu['f2']:
            rise(c, "Know your rival's price…", W / 2, 800, t, cu['f2'], 64, WHITE, weight=700)
            q = prog(t, cu['f2'] + 0.8, 0.4)
            if q > 0: text(c, '…and you can beat it by ₹1', W / 2, 900, 'dms', 64, GOLD, alpha=eo(q) * a1, weight=800)
        # envelope with rupee, sliding
        if t > cu['f2']:
            e = eo(prog(t, cu['f2'] + 0.2, 0.6))
            overlay(c, lambda d, lay: envelope(d, W / 2 - 300 + 300 * e, 1170, 300, 190, GOLD), a1 * e)
            text(c, '₹', W / 2 - 300 + 300 * e, 1185, 'anton', 120, GOLD, alpha=a1 * e)
    # f3 leaked rates doc
    a2 = eo(prog(t, cu['f3'], 0.35)) * (1 - eo(prog(t, cu['f4'] - 0.2, 0.3)))
    if a2 > 0:
        text(c, 'CBI ALLEGES:', W / 2, 470, 'anton', 90, WHITE, alpha=a2)
        def doc(d, lay):
            d.rounded_rectangle([240, 600, 840, 1220], radius=16, fill=(240, 234, 220, 255))
            for i in range(5):
                d.rectangle([300, 760 + i * 80, 560, 790 + i * 80], fill=(190, 182, 165, 255))
                d.rectangle([640, 760 + i * 80, 780, 790 + i * 80], fill=(60, 56, 50, 255))
        overlay(c, doc, a2)
        text(c, 'BID RATES', W / 2, 680, 'anton', 70, (20, 18, 14), alpha=a2)
        stamp(c, 'LEAKED', W / 2 + 40, 1000, t, cu['f3'] + 1.0, 120, RED, rot=-12)
        if t < cu['f4'] - 0.2: rise(c, 'railway officials, for cash', W / 2, 1300, t, cu['f3'] + 1.5, 46, GOLD)
    # f4 numbers
    a3 = eo(prog(t, cu['f4'], 0.35))
    if a3 > 0:
        text(c, 'MARCH 2026 · CBI', W / 2, 430, 'dms', 44, GREY, alpha=a3, weight=700, spacing=3)
        pop(c, '₹10 LAKH', W / 2, 610, t, cu['f4'] + 1.0, 220, GOLD)
        rise(c, 'taken by a senior railway engineer, CBI says', W / 2, 770, t, cu['f4'] + 1.5, 40, WHITE, weight=600)
        # 1% bar
        q = prog(t, cu['f4'] + 3.6, 0.5)
        if q > 0:
            def bar(d, lay):
                d.rounded_rectangle([140, 960, 940, 1060], radius=16, fill=(60, 56, 50, 255))
                d.rounded_rectangle([140, 960, 140 + max(24, int(800 * 0.01 * 3)), 1060], radius=16, fill=RED + (255,))
            overlay(c, bar, eo(q))
            text(c, '₹40 crore tender', W / 2 + 40, 1010, 'dms', 46, WHITE, alpha=eo(q), weight=700)
            pop(c, 'alleged ask: 1%', W / 2, 1160, t, cu['f4'] + 4.3, 80, RED)
        src(c, 'Sources: CBI statements, Mar 2026, as reported by PTI / IANS', a3)

def s_cartel(c, t, cu):
    pop(c, 'THE CARTEL', W / 2, 420, t, 0.05, 150, WHITE)
    rise(c, 'rivals secretly decide who wins', W / 2, 540, t, 0.4, 46, GOLD)
    q = prog(t, cu['g2'] + 1.6, 0.6)
    for i, n in enumerate(['FIRM A', 'FIRM B', 'FIRM C']):
        x = 220 + i * 320; p = eo(prog(t, 0.6 + i * 0.15, 0.4))
        def box(d, lay, x=x):
            d.rounded_rectangle([x - 130, 660, x + 130, 820], radius=18, fill=(26, 22, 14, 255), outline=GOLD_D + (255,), width=4)
            if q > 0:
                e = eo(q); d.line([(x, 820), (x + (W / 2 - x) * e, 820 + 290 * e)], fill=RED + (255,), width=8)
        overlay(c, box, p)
        text(c, n, x, 740, 'anton', 64, WHITE, alpha=p)
    if q > 0.6:
        def ip(d, lay):
            d.rounded_rectangle([250, 1110, 830, 1270], radius=20, fill=(60, 16, 18, 255), outline=RED + (255,), width=6)
        overlay(c, ip, eo((q - .6) * 2.5))
        text(c, 'SAME IP ADDRESS', W / 2, 1190, 'anton', 84, WHITE, alpha=eo((q - .6) * 2.5))
    src(c, 'Source: Competition Commission of India, Railways tender case, 2022', eo(prog(t, cu['g2'])))

def s_trail(c, t, cu):
    a = 1 - eo(prog(t, cu['h2'] - 0.25, 0.3))
    if a > 0:
        pop(c, 'EVERY CLICK', W / 2, 430, t, 0.05, 140, WHITE)
        pop(c, 'LEAVES A TRAIL', W / 2, 580, t, 0.3, 140, GOLD)
        def screen(d, lay):
            d.rounded_rectangle([150, 700, 930, 1240], radius=20, fill=(18, 18, 18, 255), outline=GOLD_D + (255,), width=4)
        overlay(c, screen, a * eo(prog(t, 0.5)))
        logs = ['10:02  bid submitted · Firm B', '10:05  bid submitted · Firm D', '11:00  bids locked', '11:01  technical round opened', '14:30  prices opened · audit saved']
        for i, l in enumerate(logs):
            p = prog(t, 0.9 + i * 0.45, 0.25)
            if p > 0: text(c, l, 200, 780 + i * 95, 'dms', 38, (140, 230, 150) if i == 4 else WHITE, alpha=eo(p) * a, anchor='l', weight=500)
    b = eo(prog(t, cu['h2'], 0.35))
    if b > 0:
        pop(c, 'FAIR ON PAPER.', W / 2, 560, t, cu['h2'], 130, WHITE)
        pop(c, 'HUMANS STILL RUN IT.', W / 2, 720, t, cu['h2'] + 0.9, 98, GOLD)
        e = prog(t, cu['h2'] + 2.2, 0.5)
        if e > 0:
            paste(c, logo(300), W / 2, 1000, scale=0.6 + 0.4 * back(e), alpha=eo(e))
            text(c, '@thebackstory.daily', W / 2, 1210, 'dms', 50, WHITE, alpha=eo(e), weight=700)
            text(c, 'Follow for the story behind the headlines', W / 2, 1280, 'dms', 36, GREY, alpha=eo(e), weight=500)

FN = {'shop': s_shop, 'how': s_how, 'tender': s_tender, 'env': s_env, 'l1': s_l1, 'bribe': s_bribe, 'cartel': s_cartel, 'trail': s_trail}

def draw(gt):
    for name, s0, s1 in T.bounds:
        if s0 <= gt < s1 or (name == T.bounds[-1][0] and gt >= s0): break
    c = frame_base(gt, T.total)
    keys = dict(SCENES)[name]
    cu = {k: T.cue(k, s0) for k in keys}
    t = gt - s0
    # scene fade in/out
    FN[name](c, t, cu)
    k = T.line_at(gt)
    if k and not (name == 'trail' and gt > T.start['h2'] + 2.0): caption(c, CAP[k])
    return c

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        for g in sys.argv[2:]:
            draw(float(g)).convert('RGB').save(f'/home/claude/tender/chk/f_{g}.jpg', quality=88)
    elif mode == 'scene':
        os.makedirs('/home/claude/tender/parts', exist_ok=True)
        for i, (name, s0, s1) in enumerate(T.bounds):
            if len(sys.argv) > 2 and name not in sys.argv[2].split(','): continue
            f0 = round(s0 * FPS); f1 = round(s1 * FPS)
            rc = render_scene(f'/home/claude/tender/parts/{i:02d}.mp4', f1 - f0, lambda j: draw((f0 + j) / FPS))
            print(name, f1 - f0, rc, flush=True)
    elif mode == 'info':
        print(json.dumps({'total': T.total, 'start': T.start, 'bounds': T.bounds}, indent=1))

def audio():
    sys.path.insert(0, '/home/claude/lib'); import audio as A
    S = T.start; B = {b[0]: b[1] for b in T.bounds}
    ev = [(B[n] + 0.02, 'whoosh') for n in B if B[n] > 0.1]
    ev += [(0.05, 'hit'), (S['a2'] + 0.9, 'rise'), (S['a2'] + 2.5, 'hit'), (B['how'] + 0.05, 'hit'),
           (S['c2'], 'whoosh'), (S['c2'] + 1.6, 'stamp'), (B['env'] + 0.05, 'hit'), (S['d2'], 'tick'), (S['d3'], 'tick'),
           (S['e2'] + 0.5, 'stamp'), (B['bribe'] + 0.05, 'hit'), (S['f3'] + 1.0, 'stamp'), (S['f4'] + 1.0, 'hit'),
           (S['f4'] + 4.3, 'stamp'), (B['cartel'] + 0.05, 'hit'), (S['g2'] + 2.3, 'stamp'), (S['h2'], 'hit'), (S['h2'] + 2.2, 'rise')]
    ev += [(B['trail'] + 0.9 + i * 0.45, 'tick') for i in range(5)]
    voice = [(S[k], f'/home/claude/tender/vo/{k}.wav') for k in S]
    A.build(T.total, voice, ev, '/home/claude/tender/mix_full.wav', '/home/claude/tender/mix_voice.wav', seed=3)
    print('audio ok', T.total)

if __name__ == '__main__' and sys.argv[1] == 'audio': audio()
