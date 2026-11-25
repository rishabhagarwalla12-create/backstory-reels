import json, sys, os
import soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

# usage: python3 vo.py lines.json outdir [only_keys]
# lines.json: list of [key, text] or [key, text, speed_mult] or [key, text, speed_mult, pause_after_s]
#   speed_mult < 1 slows a line down (hooks, reveals); pause_after_s adds silence after it
#   (a beat before the twist). See STORY VOICE in PLAYBOOK.md.
# Narrator settings live here and in PLAYBOOK.md; change both together.
VOICE = 'am_fenrir'       # owner's pick, 25 Nov 2026. A Kokoro voice name, or a blend like 'am_michael+am_onyx:0.55'
LANG = 'en-us'
SPEED = 1.05              # story pace (was 1.2 before 25 Nov 2026)

k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
if '+' in VOICE:
    pair, w = (VOICE.split(':') + ['0.5'])[:2]; a, b = pair.split('+'); w = float(w)
    STYLE = (k.get_voice_style(a) * w + k.get_voice_style(b) * (1 - w)).astype(np.float32)
else:
    STYLE = VOICE

lines = json.load(open(sys.argv[1]))
outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
fixp = sys.argv[1].replace('.json', '_fix.json')
FIX = json.load(open(fixp)) if os.path.exists(fixp) else []
dp = f'{outdir}/durs.json'
out = json.load(open(dp)) if os.path.exists(dp) else {}
for row in lines:
    key, text = row[0], row[1]
    mult = row[2] if len(row) > 2 else 1.0
    pause = row[3] if len(row) > 3 else 0.0
    if ONLY and key not in ONLY: continue
    ph = k.tokenizer.phonemize(text, LANG)
    for a, b in FIX: ph = ph.replace(a, b)
    s, sr = k.create(ph, voice=STYLE, speed=SPEED * mult, lang=LANG, is_phonemes=True)
    a = np.abs(s); idx = np.where(a > 0.01)[0]
    s = s[max(0, idx[0] - int(.03 * sr)):min(len(s), idx[-1] + int(.08 * sr))]
    if pause: s = np.concatenate([s, np.zeros(int(pause * sr), np.float32)])
    sf.write(f'{outdir}/{key}.wav', s, sr); out[key] = round(len(s) / sr, 3)
    print(key, out[key], ph, flush=True)
json.dump(out, open(dp, 'w'), indent=1)
print('TOTAL', round(sum(out.values()), 2))
