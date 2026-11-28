# The Backstory Daily — reel playbook

Instagram: @thebackstory.daily (Creator account). Bio: "One explainer a day. No opinions, just how it works 👇"
Owner: Rishabh Agarwalla. Posts twice a day: **1:30 PM IST** and **7:00 PM IST**, on Instagram (Reels) and YouTube (Shorts).

## What a reel is
- Vertical 1080x1920, 30 fps, **35–50 s** (60 s hard max), explaining ONE interesting concept in plain, layman language (anyone should understand it).
- Topics: business, money, economy, how-things-work, world concepts. Finshots (finshots.in) is a good source of ideas.
- Informative only: **no opinions, no advice**. Never recommend stocks or say buy/sell; no live stock prices (SEBI finfluencer rules allow education only; historical data only, 3+ months old). Add "Not investment advice." in captions on finance topics.
- Corruption / crime / allegations: attribute every claim to its source (CBI, CCI, court, regulator) and say "alleged"/"says". Never generalise ("all X are corrupt").
- Male narrator: Kokoro TTS voice `am_fenrir` (owner's pick, 25 Nov 2026; was am_michael), speed 1.05 (story pace), American English; settings live at the top of `toolkit/vo.py`. Delivery follows STORY VOICE below. Check phonemes for Indian words and fix them (lakh -> lˈɑːk, Paytm -> pˈeɪtˌiːˈɛm, karo -> kəɹˈoʊ, Dubai -> duːbˈaɪ).
- Look: gold-on-black, brand header "? THE BACKSTORY DAILY" with the globe-dot question-mark logo, thin gold progress bar, burnt-in captions box near the bottom, source line in grey. Anton for headlines, DM Sans for body. Red for warnings, blue for "frozen" etc. End card: logo + @thebackstory.daily.
- Music and SFX are synthesized in code (no licensed audio). Loudness -14 LUFS.

## HOOK RULES (owner's feedback, mandatory)
The opening must grab attention in the first 2 seconds:
1. **Lead with the shock the viewer doesn't know yet** (26 Nov 2026, from the data): the most surprising fact/number first; context comes after. It must be news to them, a hidden money flow, risk or trick ("India's oil backup lasts 10 days", "Every IPL team gets ₹484 crore before a ball is bowled"), not a price rise they've already felt at the shop ("Milk is ₹4 costlier" held people 6 s).
2. **Text on screen from frame 1** (big number / stamp / slam), no slow lead-in.
3. **Open loop**: tease the payoff so people keep watching.
4. **Make it about the viewer** where it fits ("your money", "you").
5. **Frame 0 already shows the hook text** at full size and opacity (no fade or pop from blank), and the first voice line starts within 0.1 s. Check with `python3 build.py still 0`.
Example: not "India's government is a giant shopper" but "One percent. That's the bribe a railway engineer allegedly asked for on a ₹40 crore tender."

## STORY VOICE (owner's feedback, 25 Nov 2026, mandatory)
The narration should feel like someone telling a story with a bit of curiosity, not reading a news bulletin.
1. **Write it as a story**: a time or place, a person, a problem, a twist, a payoff. "Nineteen twenty-six. Detroit. One man made a decision that still shapes your week."
2. **Curiosity beats**: 1–2 per reel, e.g. "Sounds kind, right?", "But here's the twist.", "So why would anyone do that?", "And that's where it gets interesting." Don't overdo it.
3. **Short lines, split at the reveal**: put the set-up and the reveal on separate lines so there is a beat between them.
4. **Pacing via lines.json** (`[key, text, speed_mult, pause_after_s]`): the FIRST line is never slowed and has no pause before it (most viewers decide in 2–3 s; see PERFORMANCE.md). After the hook, slow reveal lines (speed_mult 0.92–0.95) and add a 0.5–0.7 s pause before a twist and after a question; normal lines need neither. Questions end with "?" so the voice rises.
5. Listen-check by reading the printed durations: no line should run longer than ~4 s.

## KEEP IT LIGHT (owner's feedback, 22 Nov 2026, mandatory)
Interesting, appealing and educational, but never more info than people can process in one watch.
1. **One core idea per reel** (e.g. "astrology apps run on a per-minute meter"). Everything in the script serves that idea.
2. **Max 3 numbers** in the whole reel, rounded and simple. The hook number counts.
3. **~10–12 short voice lines (~85–100 words, voice total ≈ 34–44 s including story pauses)**, one visual per line, with breathing room (Timeline gap=0.3, scene_gap=0.45).
4. Cut facts that aren't needed for the core idea, however interesting; extras can go in the caption.
5. End on a punchline that calls back to the hook.

## COVER RULES (owner's feedback, 25 Nov 2026, mandatory)
The profile grid must show what every reel is about. A bare number ("+12%", "10 DAYS") or a dark first frame is not enough.
1. Every reel gets its own cover, made with `toolkit/cover.py`, and is published with it (Instagram `cover_url`, YouTube `thumbnail`).
2. **Title = the topic in 3–6 words**, readable by someone who knows nothing yet: "Why *China* pays people to *shop*", "India's oil lasts only *10 days*", "Who *invented* the *weekend*?". Put 1–2 key words in gold with *asterisks*. A number is fine only inside a phrase that says what it is.
3. **Kicker** (gold pill above the title), one of: YOUR MONEY, BUSINESS, INDIA, WORLD, HISTORY, HOW IT WORKS, TECH, CRIME & JUSTICE.
4. The grid crops reels to the middle 3:4 (y 240–1680), so the script keeps everything inside y 330–1590. Don't add text outside that.
5. Command (after the final mp4 exists):
   `python3 toolkit/cover.py reels/YYYY-MM-DD-<slug>.jpg --kicker "YOUR MONEY" --title "Why *tyres* keep getting *costlier*" --bg reels/YYYY-MM-DD-<slug>.mp4 --t 5`
   Then LOOK at the cover cropped to 3:4 (`Image.open(f).crop((0,240,1080,1680))`): the title must be readable at thumbnail size, with no cut-off words.

## YOU'RE IN CHARGE (owner's instruction, 25 Nov 2026)
The owner wants this page run by you, not by him. Think about what would make the page better and decide; don't ask him to choose.
1. **Every run, start with the numbers**: pull Instagram insights (views, reach, ig_reels_avg_watch_time, saved, shares) for the last ~20 reels and update the table in PERFORMANCE.md.
2. **Act on them**: if the data shows something (a topic type, hook style, length or slot that clearly wins or loses), change the rule in this playbook, log it in PERFORMANCE.md's Decisions log with the reason, and apply it in this run's reel. Small, measurable changes; one at a time where possible.
3. **Sunday 1:30 PM run = weekly review**: compare the week, keep what worked, drop what didn't, end or extend running tests, and decide on slots.
4. **Tell, don't ask**: in the run's final message, add one line on what you changed and why (if anything). Only check with the owner before spending money, changing the brand look or name, or anything that could get the account flagged.
5. Hard rules never change: fact rules, SEBI/finfluencer limits, attribution for allegations.

## TOPIC SCORE (from the data, 25 Nov 2026)
Before picking, score the candidate 0–3, one point each:
- **Big stage, told through money** (28 Nov 2026, from the data): a country-scale subject or mega event every Indian knows: the rupee, India's oil, IPL/cricket, the wedding season, a mega launch (GTA 6), a giant brand. Household bills and personal-finance tips (a shelf price, your card, a shopping deal) don't earn this point: they were 0 for 5 (6.0–8.8 s avg watch) while all 4 breakouts were big-stage subjects.
- **In the news this week** (or a launch/result day), checked by date.
- **One jaw-drop number or twist the viewer doesn't already know**, and it fits in the first line. A price rise people have already seen ("milk/petrol/tyres got costlier") scores 0 here unless the first line is the hidden cause (price-rise reels were 0 for 3, 26 Nov 2026).
Pick only 2+; prefer 3. Foreign or history topics need an Indian angle in the first line ("Why China pays its people to shop — and why your phone could get cheaper"). Skip anniversaries unless something new happened.

## Topics and initiative
- Pick topics yourself and post; **never ask the owner** to choose or approve. The owner's own ideas in TOPICS.md go first.
- Prefer topics with one surprising, relatable idea (everyday money, how things around you work). You may reorder or replace queue topics if a better one exists; note it in TOPICS.md.
- The owner allows account-benefiting actions without asking (e.g. replying to genuine comments on our reels, fixing a caption typo). No spammy growth tactics (mass follow/like/DM, buying engagement) and nothing that risks the account getting flagged.

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
... (3–5 points, short)

<one-line punchline>

<Question to the audience> 👇
<Share prompt, test until 2 Dec 2026: "Send this to someone who …" 📤>

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
1. Write `/home/claude/tts/<slug>.json` (list of [key, line] or [key, line, speed_mult, pause_after_s]) and optional `<slug>_fix.json` (phoneme fixes). Run `python3 vo.py <slug>.json /home/claude/<slug>/vo` and check TOTAL ≈ 34–44 s (trim lines if longer; see KEEP IT LIGHT and STORY VOICE).
2. Copy `toolkit/examples/tenders/build.py` to `/home/claude/<slug>/build.py`, change paths, SCENES and scene functions. Helpers in `lib/reel.py`: pop, rise, stamp, text, paste, overlay, envelope, check, cross, logo, caption, Timeline, render_scene. `lib/audio.py` builds music+SFX+voice mix.
3. `python3 build.py info` (total ≤ 60 s), `python3 build.py still <t> ...` and LOOK at the frames (overlaps, text off-screen, safe zone x 80–1000, y 230–1420), fix, then `python3 build.py audio` and `python3 build.py scene`.
4. Join + mux:
```
ls parts/*.mp4 | sed "s/^/file '/;s/$/'/" > list.txt && ffmpeg -y -loglevel error -f concat -safe 0 -i list.txt -c copy joined.mp4 && ffmpeg -y -loglevel error -i joined.mp4 -i mix_full.wav -map 0:v -map 1:a -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart <Name>_reel.mp4
```
5. Check final frames once more. Single-pass loudnorm lands around -15 LUFS; for -14, run a two-pass loudnorm (measure with print_format=json, then apply measured_* values with linear=true).

## How to publish
1. Copy the mp4 to `reels/YYYY-MM-DD-<slug>.mp4`, make the cover `reels/YYYY-MM-DD-<slug>.jpg` (COVER RULES), commit both, push to `main` (end commit messages with the session attribution lines). Public links:
   `https://raw.githubusercontent.com/rishabhagarwalla12-create/backstory-reels/main/reels/<file>.mp4` (and the same path with `.jpg` for the cover)
2. Instagram (mcp__Instagram__ tools): `instagram_post_ig_user_media` with ig_user_id "me", media_type REELS, video_url, **cover_url = the raw .jpg link**, caption, share_to_feed true -> container id. Poll `instagram_get_ig_media` fields status_code until FINISHED.
3. At the slot time (1:30 PM or 7:00 PM IST) call `instagram_post_ig_user_media_publish` (ig_user_id "me", creation_id). If the slot is still in the future, schedule it with `send_later` into this same session; if it has passed, publish right away.
4. YouTube (Zapier, selected_api YouTubeV4CLIAPI, action upload_video; if it says no default connection, pass connection_id 02edc458-57c5-8e87-85f5-b0452819f48f, the Backstory Daily channel): title, description, video = the raw GitHub URL, thumbnail = the raw .jpg cover URL, privacy_status public, made_for_kids false, notify_subscribers true. Do it at the same time as the Instagram publish. If YouTube answers "doesn't have permissions to upload and set custom video thumbnails", the video is usually uploaded anyway (check with a GET to youtube/v3/search?forMine=true&order=date before retrying, so you don't post it twice); custom thumbnails need the channel's phone verification (youtube.com/verify), which only the owner can do. Seen 25 Nov 2026.
5. Mark the topic done in TOPICS.md with date, slot, and both links; commit and push.
6. Tell the owner (SendUserMessage) the Instagram permalink and YouTube link.
