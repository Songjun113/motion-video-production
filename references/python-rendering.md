# Python graphics and FFmpeg route

Use when typography, diagrams, cards, plots, or procedural graphics dominate and local Python can render them reliably. The approved source is in `assets/eeg-finger-control/`; copy it into the project before adapting it.

## Composition

Expose `frame(t)` returning a Pillow RGB image at the target size. Evaluate each frame at `n / fps` for `n` in `0 .. frame_count - 1`. Define how duration is quantized when duration times fps is not an integer; record the actual encoded duration.

Keep background, text, foreground objects, transition masks, and audio event times explicit. Reuse the same geometry for keyframes and full animation. Real-time clocks, cumulative state, and unseeded randomness must not affect a requested frame.

Cache fonts and static local assets. Bound caches for transformed objects and changing number labels: every full-resolution cached image costs memory. Blur shadows inside an object's bounding box. Composite RGBA layers using `alpha_composite`; avoid accidentally applying alpha twice. Render rotation and scaling with appropriate resampling.

For each transition inspect the start, midpoint, and completion. The reveal mask must cover the target frame by the end, and the next scene must have a meaningful visible state during the reveal. Avoid unintended blank flashes. Low-amplitude idle motion can sustain life during a hold; main text should be stable.

## Encoding

Pipe RGB24 frames directly into FFmpeg when retaining a PNG sequence is unnecessary. Set input size and frame rate explicitly. Typical final settings are H.264, CRF around 18, `yuv420p`, and `+faststart`; adjust for the destination. Use an argument array, capture encoder errors, and fail if the pipe or encoder fails.

For FFmpeg discovery prefer an explicitly supplied executable, then PATH, then `imageio_ffmpeg.get_ffmpeg_exe()` when installed. Use optional dependencies only when needed; do not assume ffprobe is bundled with imageio-ffmpeg.

For audio, synthesize or stage a WAV at the intended sample rate, schedule events against the same timeline, fade the start and ending, and mix with headroom before AAC encoding. Equal-power stereo pan is useful for spatially located actions. Declare deliberate silence when the brief calls for it, and do not fail a silent brief for lacking an audio stream.

## Validation and handoff

Use the supplied `scripts/verify_mp4.py` with the project's duration, dimensions, fps, audio expectation, and transition times. It uses ffprobe JSON when available; otherwise it inspects FFmpeg metadata and counts fully decoded frames. It produces a report and contact sheet, plus audio measurements and a waveform when audio exists.

Then inspect the extracted images and audio appropriately. Decode success, sampled visual review, and audio listening are distinct evidence. Report only checks performed. Retain source, font requirements, asset provenance, and a direct render command alongside the MP4.
