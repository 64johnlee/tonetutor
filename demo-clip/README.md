# ToneTutor Demo Clip — finishing guide

A **skeleton** 30s vertical (1080×1920) demo, with the `LAUNCH.md` shot list, captions, the
red→green tone-flip "money shot", and the end card already built. You swap in real footage + audio.

```
cd demo-clip
npm run dev      # preview in browser
npm run check    # lint + validate
npm run render   # export MP4 once footage is in
```

## The 7 beats (already timed)

| Scene | Time | Placeholder to replace | Caption (done) |
|-------|------|------------------------|----------------|
| S1 | 0–2s | (text only, no clip) | "Your vocab is fine. Your tones aren't." |
| S2 | 2–5s | tap Restaurant + HSK 2 | "Pick a scene + your level." |
| S3 | 5–8s | tap mic + speak (flub a tone) | "Just talk." |
| S4 | 8–14s | reply card grading — **money shot** | "It caught the one tone I got wrong." |
| S5 | 14–19s | redo → grade flips green | "Fix it. Hear it. Lock it in." |
| S6 | 19–24s | session report card | "End-of-session report card." |
| S7 | 24–30s | (end card, no clip) | "Practice free → tonetutor.tefusiang.com" |

## 1. Swap in your screen recordings

Record each beat on your phone, drop the files in `demo-clip/clips/`, then in `index.html`
replace each `<div class="screen-ph">…</div>` with a **muted** video element. Example for S4:

```html
<video id="clip-s4" src="clips/s4.mp4" muted playsinline
       data-start="8" data-duration="6" data-track-index="0"
       style="width:100%;height:100%;object-fit:cover;border-radius:60px"></video>
```

Use these `data-start` / `data-duration` per scene: S2 `2/3`, S3 `5/3`, S4 `8/6`, S5 `14/5`, S6 `19/5`.
Every swapped-in video **must** be `muted`, have a unique `id`, and `playsinline`.

## 2. Add audio (separate elements — never the video's own track)

Drop `vo.mp3` etc. in `demo-clip/`, then paste these just before `</body>` in `index.html`:

```html
<audio id="vo"    src="vo.mp3"    data-start="0"  data-duration="30"  data-track-index="2" data-volume="1"></audio>
<audio id="ding"  src="ding.mp3"  data-start="9"  data-duration="1"   data-track-index="3" data-volume="0.8"></audio>
<audio id="chime" src="chime.mp3" data-start="14" data-duration="1.5" data-track-index="3" data-volume="0.7"></audio>
<audio id="music" src="music.mp3" data-start="0"  data-duration="30"  data-track-index="4" data-volume="0.25"></audio>
```

- `ding` (~9s) lands on the red tone-catch; `chime` (~14s) on the green fix — matches the visual flips.
- Keep `music` low (`0.25`) so your real spoken Mandarin (the moat) stays clear.
- Mute-first: captions are burned in, so it reads with sound off too.

## 3. Re-check, then render

```bash
npm run check     # must pass once real media files exist
npm run render    # outputs the MP4
```

Then trim a **15s version** (hook → money shot → green → end card) for X tweet-1 + fast Shorts,
per `LAUNCH.md`.
