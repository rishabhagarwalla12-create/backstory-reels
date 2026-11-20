# The Backstory Daily — reel playbook

Instagram: @thebackstory.daily (Creator account). Bio: "One explainer a day. No opinions, just how it works 👇"
Owner: Rishabh Agarwalla. Posts twice a day: **1:30 PM IST** and **7:00 PM IST**, on Instagram (Reels) and YouTube (Shorts).

## What a reel is
- Vertical 1080x1920, 30 fps, **55–60 s max**, explaining one interesting concept in plain, layman language (anyone should understand it).
- Topics: business, money, economy, how-things-work, world concepts. Finshots (finshots.in) is a good source of ideas.
- Informative only: **no opinions, no advice**. Never recommend stocks or say buy/sell; no live stock prices (SEBI finfluencer rules allow education only; historical data only, 3+ months old). Add "Not investment advice." in captions on finance topics.
- Corruption / crime / allegations: attribute every claim to its source (CBI, CCI, court, regulator) and say "alleged"/"says". Never generalise ("all X are corrupt").
- Male narrator: Kokoro TTS voice `am_michael`, speed 1.2, American English. Check phonemes for Indian words and fix them (lakh -> lˈɑːk, Paytm -> pˈeɪtˌiːˈɛm, karo -> kəɹˈoʊ, Dubai -> duːbˈaɪ).
- Look: gold-on-black, brand header "? THE BACKSTORY DAILY" with the globe-dot question-mark logo, thin gold progress bar, burnt-in captions box near the bottom, source line in grey. Anton for headlines, DM Sans for body. Red for warnings, blue for "frozen" etc. End card: logo + @thebackstory.daily.
- Music and SFX are synthesized in code (no licensed audio). Loudness -14 LUFS.

## HOOK RULES (owner's feedback, mandatory)
The opening must grab attention in the first 2 seconds:
1. **Lead with the shock**: the most surprising fact/number first; context comes after.
2. **Text on screen from frame 1** (big number / stamp / slam), no slow lead-in.
3. **Open loop**: tease the payoff so people keep watching.
4. **Make it about the viewer** where it fits ("your money", "you").
Example: not "India's government is a giant shopper" but "One percent. That's the bribe a railway engineer allegedly asked for on a ₹40 crore tender."

## Fact rules
- Research with web search before writing. Every number must come from a source found that day; note it for the caption's Sources line.
- "Trending/this week" means the event happened in the last ~2 weeks: **check the actual date and year** of the source (a 2025 story once got mistaken for 2026).
- If a topic in the queue turns out stale or unverifiable, skip it, mark it in TOPICS.md, and take the next one.

## Caption format (same every time)
```
<Hook line> <1–2 emoji>

<Question or "What happened?">
<emoji> point
<emoji> point
... (4–8 points, short)

<one-line punchline>

<Question to the audience> 👇

Follow @thebackstory.daily for the story behind the headlines.

Sources: <sources with month/year>. <"Not investment advice." for finance>

#tag1 #tag2 #tag3 #tag4 #TheBackstoryDaily
```
4–5 relevant, popular hashtags; always end with #TheBackstoryDaily (with the #).
YouTube title: hook-led, under 100 chars, ending with #Shorts. YouTube description = the caption.

## How to build a reel (toolkit in /toolkit)
```
cp -r toolkit/lib /home/claude/lib && mkdir -p /home/claude/tts && cp toolkit/vo.py /home/claude/tts/
pip install --break-system-packages -q kokoro-onnx soundfile
cd /home/claude/tts && for f in kokoro-v1.0.onnx voices-v1.0.bin; do curl -sSL -o $f https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f; done
```
1. Write `/home/claude/tts/<slug>.json` (list of [key, line]) and optional `<slug>_fix.json` (phoneme fixes). Run `python3 vo.py <slug>.json /home/claude/<slug>/vo` and check TOTAL ≈ 52–54 s (trim lines if longer).
2. Copy `toolkit/examples/tenders/build.py` to `/home/claude/<slug>/build.py`, change paths, SCENES and scene functions. Helpers in `lib/reel.py`: pop, rise, stamp, text, paste, overlay, envelope, check, cross, logo, caption, Timeline, render_scene. `lib/audio.py` builds music+SFX+voice mix.
3. `python3 build.py info` (total ≤ 60 s), `python3 build.py still <t> ...` and LOOK at the frames (overlaps, text off-screen, safe zone x 80–1000, y 230–1420), fix, then `python3 build.py audio` and `python3 build.py scene`.
4. Join + mux:
```
ls parts/*.mp4 | sed "s/^/file '/;s/$/'/" > list.txt && ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy joined.mp4 && ffmpeg -y -loglevel error -i joined.mp4 -i mix_full.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart <Name>_reel.mp4
```
5. Check final frames once more.

## How to publish
1. Copy the mp4 to `reels/YYYY-MM-DD-<slug>.mp4`, commit, push to `main` (end commit messages with the session attribution lines). Public link:
   `https://raw.githubusercontent.com/rishabhagarwalla12-create/backstory-reels/main/reels/<file>.mp4`
2. Instagram (mcp__Instagram__ tools): `instagram_post_ig_user_media` with ig_user_id "me", media_type REELS, video_url, caption, share_to_feed true -> container id. Poll `instagram_get_ig_media` fields status_code until FINISHED.
3. At the slot time (1:30 PM or 7:00 PM IST) call `instagram_post_ig_user_media_publish` (ig_user_id "me", creation_id). If the slot is still in the future, schedule it with `send_later` into this same session; if it has passed, publish right away.
4. YouTube (Zapier, selected_api YouTubeV4CLIAPI, action upload_video): title, description, video = the raw GitHub URL, privacy_status public, made_for_kids false, notify_subscribers true. Do it at the same time as the Instagram publish.
5. Mark the topic done in TOPICS.md with date, slot, and both links; commit and push.
6. Tell the owner (SendUserMessage) the Instagram permalink and YouTube link.
