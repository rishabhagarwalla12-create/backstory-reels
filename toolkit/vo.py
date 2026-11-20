import json, sys, os
import soundfile as sf, numpy as np
from kokoro_onnx import Kokoro

# usage: python3 vo.py lines.json outdir [only_keys]
VOICE = 'am_michael'; SPEED = 1.2
lines = json.load(open(sys.argv[1]))
outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
FIX = json.load(open(sys.argv[1].replace('.json', '_fix.json'))) if os.path.exists(sys.argv[1].replace('.json', '_fix.json')) else []
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
dp = f'{outdir}/durs.json'
out = json.load(open(dp)) if os.path.exists(dp) else {}
for key, text in lines:
    if ONLY and key not in ONLY: continue
    ph = k.tokenizer.phonemize(text, 'en-us')
    for a, b in FIX: ph = ph.replace(a, b)
    s, sr = k.create(ph, voice=VOICE, speed=SPEED, lang='en-us', is_phonemes=True)
    a = np.abs(s); idx = np.where(a > 0.01)[0]
    s = s[max(0, idx[0] - int(.03 * sr)):min(len(s), idx[-1] + int(.08 * sr))]
    sf.write(f'{outdir}/{key}.wav', s, sr); out[key] = round(len(s) / sr, 3)
    print(key, out[key], ph, flush=True)
json.dump(out, open(dp, 'w'), indent=1)
print('TOTAL', round(sum(out.values()), 2))
