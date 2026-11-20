import sys, json, math
sys.path.insert(0, '/home/claude/lib')
from reel import *

LINES = json.load(open('/home/claude/tts/paytm.json'))
DURS = json.load(open('/home/claude/paytm/vo/durs.json'))
SCENES = [('hook', ['a1', 'a2', 'a3']), ('launch', ['b1', 'b2']), ('bank', ['c1', 'c2']), ('fall', ['d1', 'd2', 'd3']),
          ('back', ['e1', 'e2', 'e3']), ('learner', ['f1', 'f2', 'f3']), ('end', ['g1', 'g2'])]
T = Timeline(LINES, DURS, SCENES, gap=0.14, scene_gap=0.26, tail=2.4)
CAP = dict(LINES)
CAP['a1'] = 'Remember "Paytm karo"?'
CAP['e3'] = 'On 13 November, the RBI gave it an in-principle nod to run wallets.'
CAP['d1'] = '2022: the RBI stopped it from adding new customers.'
CAP['d2'] = 'January 2024: no more deposits, no wallet top-ups.'

def src(c, s, alpha=1):
    text(c, s, W / 2, 1385, 'dms', 30, GREY, alpha=alpha, weight=500)

def phone(d, cx, cy, w=380, h=720, col=GOLD, a=255):
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=48, fill=(20, 18, 14, a), outline=col[:3] + (a,), width=9)
    d.rounded_rectangle([cx - 50, cy - h / 2 + 22, cx + 50, cy - h / 2 + 36], radius=7, fill=col[:3] + (a,))

def s_hook(c, t, cu):
    p = eo(prog(t, 0.0, 0.4))
    overlay(c, lambda d, lay: phone(d, W / 2, 850), p)
    pop(c, 'PAYTM', W / 2, 760, t, 0.15, 120, WHITE)
    pop(c, 'KARO', W / 2, 890, t, 0.45, 120, GOLD)
    # frost
    fz = eo(prog(t, cu['a2'] + 1.6, 0.6)) * (1 - eo(prog(t, cu['a3'] + 0.3, 0.5)))
    if fz > 0:
        def frost(d, lay):
            d.rounded_rectangle([W / 2 - 190, 490, W / 2 + 190, 1210], radius=48, fill=(150, 200, 255, 90))
            for i in range(3):
                cx, cy = W / 2 - 120 + (i % 3) * 120, 600; r = 36
                for k in range(3):
                    a = math.pi / 3 * k
                    d.line([(cx - r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=(220, 240, 255, 230), width=6)
        overlay(c, frost, fz)
    if t < cu['a3'] + 0.3:
        stamp(c, 'FROZEN · 2024', W / 2, 1060, t, cu['a2'] + 1.8, 84, BLUE, rot=-8)
    if t > cu['a3']:
        pop(c, 'SECOND LIFE?', W / 2, 400, t, cu['a3'], 130, GOLD)

def s_launch(c, t, cu):
    a = 1 - eo(prog(t, cu['b2'] - 0.2, 0.3))
    if a > 0:
        text(c, '2014', W / 2, 620, 'anton', 300, GOLD, scale=0.6 + 0.4 * back(prog(t, 0.05, 0.4)), alpha=eo(prog(t, 0.05)) * a)
        rise(c, 'Paytm Wallet launches', W / 2, 860, t, 0.4, 64, WHITE, weight=700)
    b = eo(prog(t, cu['b2'], 0.35))
    if b > 0:
        text(c, 'NOV 2016', W / 2, 420, 'dms', 50, GREY, alpha=b, weight=800, spacing=4)
        pop(c, 'DEMONETISATION', W / 2, 520, t, cu['b2'], 120, WHITE)
        for i, v in enumerate(['500', '1000']):
            x = W / 2 - 190 + i * 380; y = 760
            def note(d, lay, x=x):
                d.rounded_rectangle([x - 160, y - 85, x + 160, y + 85], radius=14, fill=(52, 48, 40, 255), outline=GREY + (255,), width=4)
            overlay(c, note, b)
            text(c, '₹' + v, x, y, 'anton', 90, GREY, alpha=b)
            q = prog(t, cu['b2'] + 0.6 + i * 0.2, 0.25)
            if q > 0: overlay(c, lambda d, lay, x=x: cross(d, x, y, 150 * eo(q) + 1, RED, 16), 1)
        # chart shoots up
        q = prog(t, cu['b2'] + 1.2, 1.2)
        if q > 0:
            def chart(d, lay):
                pts = []
                for i in range(41):
                    u = i / 40
                    if u > eo(q): break
                    yv = 0.08 + 0.05 * math.sin(u * 9) if u < 0.55 else 0.08 + (u - 0.55) ** 1.4 * 1.9
                    pts.append((160 + u * 760, 1290 - yv * 360))
                if len(pts) > 1: d.line(pts, fill=GOLD + (255,), width=12, joint='curve')
                d.line([(160, 1300), (920, 1300)], fill=GREY + (180,), width=3)
            overlay(c, chart, 1)
            rise(c, 'Paytm, everywhere', W / 2 + 120, 1000, t, cu['b2'] + 2.0, 54, GOLD, weight=800)

def bank_icon(d, cx, cy, s, col=GOLD, a=255):
    cl = col[:3] + (a,)
    d.polygon([(cx - s, cy - s * .45), (cx, cy - s * .95), (cx + s, cy - s * .45)], fill=cl)
    for k in range(4):
        x = cx - s * .75 + k * s * .5
        d.rectangle([x - s * .09, cy - s * .35, x + s * .09, cy + s * .5], fill=cl)
    d.rectangle([cx - s, cy + s * .55, cx + s, cy + s * .7], fill=cl)

def s_bank(c, t, cu):
    pop(c, '2017', W / 2, 420, t, 0.05, 160, GOLD)
    p = eo(prog(t, 0.3, 0.4))
    overlay(c, lambda d, lay: bank_icon(d, 720, 800, 190), p)
    text(c, 'PAYTM PAYMENTS BANK', 720, 1010, 'dms', 40, WHITE, alpha=p, weight=800)
    # wallet slides into bank
    m = eio(prog(t, 0.9, 1.4))
    wx = 260 + (720 - 260) * m; wa = 1 - eo(prog(t, 2.2, 0.3))
    def wallet(d, lay):
        d.rounded_rectangle([wx - 110, 730, wx + 110, 880], radius=20, fill=(30, 26, 18, 255), outline=GOLD + (255,), width=8)
        d.rounded_rectangle([wx + 20, 780, wx + 110, 830], radius=12, outline=GOLD + (255,), width=6)
    overlay(c, wallet, eo(prog(t, 0.5)) * wa)
    if wa > 0: text(c, 'WALLET', wx, 920, 'dms', 36, GOLD, alpha=eo(prog(t, 0.5)) * wa, weight=800)
    if t > cu['c2']:
        pop(c, 'BANK = STRICTER RULES', W / 2, 1180, t, cu['c2'], 92, WHITE)
        rise(c, 'more checks · more audits · tighter KYC', W / 2, 1290, t, cu['c2'] + 0.5, 40, GREY, weight=600)

def s_fall(c, t, cu):
    items = [('d1', '2022', 'No new customers'), ('d2', 'JAN 2024', 'No deposits · no wallet top-ups'), ('d3', 'APR 2026', 'Bank licence cancelled')]
    def line(d, lay):
        top = 420; bot = 420 + 280 * 2 * eo(prog(t, 0.1, 0.8)) ; d.line([(220, top), (220, bot)], fill=(90, 40, 40, 255), width=8)
    overlay(c, line, 1)
    for i, (k, yr, lab) in enumerate(items):
        y = 420 + i * 280; p = prog(t, cu[k], 0.35)
        if p <= 0: continue
        overlay(c, lambda d, lay, y=y: d.ellipse([220 - 28, y - 28, 220 + 28, y + 28], fill=RED + (255,)), eo(p))
        text(c, yr, 290, y - 45, 'anton', 96, WHITE, alpha=eo(p), anchor='l')
        text(c, lab, 292, y + 50, 'dms', 46, RED if i == 2 else GOLD, alpha=eo(p), anchor='l', weight=700)
    stamp(c, 'CANCELLED', W / 2 + 60, 1235, t, cu['d3'] + 1.6, 120, RED, rot=-8)
    src(c, 'Source: RBI actions, as reported by PTI / Inc42 / YourStory', eo(prog(t, 0.5)))

def s_back(c, t, cu):
    a = 1 - eo(prog(t, cu['e2'] - 0.2, 0.3))
    if a > 0:
        for i, l in enumerate(['HOW IS IT', 'COMING BACK?']):
            p = prog(t, 0.05 + i * 0.25, 0.4)
            text(c, l, W / 2, 700 + i * 190, 'anton', 170, WHITE if i == 0 else GOLD, scale=0.6 + 0.4 * back(p), alpha=eo(p) * a)
    b = eo(prog(t, cu['e2'], 0.35)) * (1 - eo(prog(t, cu['e3'] - 0.2, 0.3)))
    if b > 0:
        def boxes(d, lay):
            d.rounded_rectangle([140, 480, 940, 640], radius=20, fill=(30, 28, 26, 255), outline=(90, 84, 74, 255), width=4)
            d.rounded_rectangle([140, 900, 940, 1100], radius=20, fill=(40, 32, 14, 255), outline=GOLD + (255,), width=6)
            d.polygon([(540 - 40, 700), (540 + 40, 700), (540, 830)], fill=GOLD + (255,))
        overlay(c, boxes, b)
        text(c, 'PAYTM PAYMENTS BANK', W / 2, 560, 'anton', 74, GREY, alpha=b)
        q = prog(t, cu['e2'] + 0.2, 0.3)
        if q > 0: overlay(c, lambda d, lay: d.line([(170, 560), (170 + 740 * eo(q), 560)], fill=RED + (255,), width=10), b)
        text(c, 'PAYTM PAYMENTS SERVICES', W / 2, 975, 'anton', 74, GOLD, alpha=b)
        text(c, 'a different Paytm company', W / 2, 1050, 'dms', 40, WHITE, alpha=b, weight=600)
    e = eo(prog(t, cu['e3'], 0.35))
    if e > 0:
        def cal(d, lay):
            d.rounded_rectangle([290, 440, 790, 960], radius=30, fill=(240, 234, 220, 255))
            d.rounded_rectangle([290, 440, 790, 570], radius=30, fill=RED + (255,)); d.rectangle([290, 520, 790, 570], fill=RED + (255,))
        overlay(c, cal, e)
        text(c, 'NOV 2026', 540, 505, 'anton', 70, WHITE, alpha=e)
        text(c, '13', 540, 760, 'anton', 300, (20, 18, 14), alpha=e)
        pop(c, 'RBI: IN-PRINCIPLE NOD', W / 2, 1110, t, cu['e3'] + 1.2, 92, GOLD)
        q = prog(t, cu['e3'] + 1.8, 0.3)
        if q > 0: rise(c, 'to issue wallets (prepaid instruments)', W / 2, 1220, t, cu['e3'] + 1.8, 40, WHITE, weight=600)
        src(c, "Source: Paytm's stock exchange filing, 13 Nov 2026 (via PTI)", e)

def s_learner(c, t, cu):
    a = 1 - eo(prog(t, cu['f2'] - 0.2, 0.3))
    if a > 0:
        p = prog(t, 0.05, 0.4)
        def plate(d, lay):
            d.rounded_rectangle([340, 440, 740, 840], radius=30, fill=(245, 245, 245, 255))
        overlay(c, plate, eo(p) * a)
        text(c, 'L', 540, 640, 'anton', 330, RED, scale=0.6 + 0.4 * back(p), alpha=eo(p) * a)
        pop(c, "A LEARNER'S LICENCE", W / 2, 1000, t, 0.4, 100, WHITE)
    b = eo(prog(t, cu['f2'], 0.35))
    if b > 0:
        pop(c, 'BEFORE IT GOES LIVE', W / 2, 430, t, cu['f2'], 100, WHITE)
        def rows(d, lay):
            for i in range(2):
                y = 640 + i * 330
                d.rounded_rectangle([110, y - 120, 970, y + 120], radius=24, fill=(26, 22, 14, 255), outline=GOLD_D + (255,), width=4)
        overlay(c, rows, b)
        text(c, 'Cyber-security audit', 170, 600, 'dms', 50, WHITE, alpha=b, anchor='l', weight=800)
        text(c, 'within 6 months, or approval lapses', 170, 675, 'dms', 36, RED, alpha=b, anchor='l', weight=600)
        # ring timer
        q = clamp((t - cu['f2']) / 3.5)
        def ring(d, lay):
            d.ellipse([820, 560, 940, 720], outline=(70, 64, 54, 255), width=12)
            d.arc([820, 560, 940, 720], -90, -90 + 360 * q, fill=GOLD + (255,), width=12)
        overlay(c, ring, b)
        text(c, '6M', 880, 640, 'anton', 50, GOLD, alpha=b)
        f = eo(prog(t, cu['f3'], 0.35))
        text(c, 'Final RBI approval', 170, 930, 'dms', 50, WHITE if f > 0 else GREY, alpha=b, anchor='l', weight=800)
        text(c, 'only after that', 170, 1005, 'dms', 36, GOLD, alpha=b * max(f, 0.0), anchor='l', weight=600)
        if f > 0: stamp(c, 'PENDING', 830, 970, t, cu['f3'] + 0.3, 56, GOLD, rot=-8)
        src(c, 'Source: RBI letter terms, as reported by YourStory, Nov 2026', b)

def s_end(c, t, cu):
    pop(c, 'SAME APP.', W / 2, 470, t, 0.05, 160, WHITE)
    pop(c, 'NEW COMPANY', W / 2, 640, t, 0.9, 140, GOLD)
    pop(c, 'BEHIND THE WALLET.', W / 2, 790, t, 1.3, 100, GOLD)
    if t > cu['g2']:
        rise(c, 'Would you load money', W / 2, 960, t, cu['g2'], 60, WHITE, weight=800)
        rise(c, 'into Paytm again?', W / 2, 1040, t, cu['g2'] + 0.15, 60, WHITE, weight=800)
        e = prog(t, cu['g2'] + 1.6, 0.5)
        if e > 0:
            paste(c, logo(200), W / 2, 1210, scale=0.6 + 0.4 * back(e), alpha=eo(e))
            text(c, '@thebackstory.daily', W / 2, 1360, 'dms', 46, WHITE, alpha=eo(e), weight=700)

FN = {'hook': s_hook, 'launch': s_launch, 'bank': s_bank, 'fall': s_fall, 'back': s_back, 'learner': s_learner, 'end': s_end}

def draw(gt):
    for name, s0, s1 in T.bounds:
        if s0 <= gt < s1: break
    c = frame_base(gt, T.total)
    keys = dict(SCENES)[name]; cu = {k: T.cue(k, s0) for k in keys}
    FN[name](c, gt - s0, cu)
    k = T.line_at(gt)
    if k and not (name == 'end' and gt > T.start['g2'] + 1.5): caption(c, CAP[k])
    return c

def audio():
    import audio as A
    S = T.start; B = {b[0]: b[1] for b in T.bounds}
    ev = [(B[n] + 0.02, 'whoosh') for n in B if B[n] > 0.1]
    ev += [(0.15, 'hit'), (S['a2'] + 1.8, 'stamp'), (S['a3'], 'rise'), (S['a3'] + 1.0, 'hit'), (B['launch'] + 0.05, 'hit'),
           (S['b2'], 'hit'), (S['b2'] + 0.6, 'stamp'), (S['b2'] + 0.8, 'stamp'), (B['bank'] + 0.05, 'hit'), (S['c2'], 'hit'),
           (S['d1'], 'tick'), (S['d2'], 'tick'), (S['d3'], 'tick'), (S['d3'] + 1.6, 'stamp'), (S['e3'], 'hit'), (S['e3'] + 1.2, 'hit'),
           (B['learner'] + 0.05, 'hit'), (S['f3'] + 0.3, 'stamp'), (B['end'] + 0.05, 'hit'), (B['end'] + 0.9, 'hit'), (S['g2'] + 1.6, 'rise')]
    voice = [(S[k], f'/home/claude/paytm/vo/{k}.wav') for k in S]
    A.build(T.total, voice, ev, '/home/claude/paytm/mix_full.wav', '/home/claude/paytm/mix_voice.wav', seed=5)
    print('audio ok', T.total)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        os.makedirs('/home/claude/paytm/chk', exist_ok=True)
        for g in sys.argv[2:]: draw(float(g)).convert('RGB').save(f'/home/claude/paytm/chk/f_{g}.jpg', quality=88)
    elif mode == 'scene':
        os.makedirs('/home/claude/paytm/parts', exist_ok=True)
        for i, (name, s0, s1) in enumerate(T.bounds):
            if len(sys.argv) > 2 and name not in sys.argv[2].split(','): continue
            f0 = round(s0 * FPS); f1 = round(s1 * FPS)
            print(name, f1 - f0, render_scene(f'/home/claude/paytm/parts/{i:02d}.mp4', f1 - f0, lambda j: draw((f0 + j) / FPS)), flush=True)
    elif mode == 'info':
        print('total', round(T.total, 2)); print([(b[0], round(b[1], 2)) for b in T.bounds]); print({k: round(v, 2) for k, v in T.start.items()})
    elif mode == 'audio': audio()
