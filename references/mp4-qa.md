# MP4 delivery QA

Run these checks on the final encoded file, not only on an intermediate preview.

Run `scripts/verify_mp4.py` from the skill with expected duration, size, fps, optional audio requirement, and representative times. It supports other durations and aspect ratios. A technical pass leaves visual inspection and listening pending. Read its JSON report before interpreting a successful process exit.

## Probe the file

Use `ffprobe` or an equivalent inspector to record:

- container and file size;
- measured duration;
- video codec, profile, pixel format, dimensions, frame rate, and frame count when available;
- audio codec, sample rate, channel layout, and duration;
- color metadata when color accuracy matters.

Confirm that reported values match the brief and that audio and video durations do not drift visibly.

## Decode test

Decode the entire file with a tool that reports errors. A playable opening is not enough. Treat decode failures, truncated streams, missing required audio, and invalid timestamps as delivery failures. For an intentionally silent brief, validate the video without requiring an audio stream.

## Visual inspection

Inspect at least:

- the first and final frames;
- every scene midpoint;
- frames before, during, and after each transition;
- each major text appearance;
- the peak of fast movement or deformation;
- any frame containing real product UI or factual data.

Generate a contact sheet for multi-scene work. Check black or blank frames, missing fonts or assets, cropping, overflow, low contrast, banding, compression blocks, judder, flicker, tearing, and stale frames.

Check that the approved object motions are present and scene layouts retain the approved variation. Examine transition completion for uncovered corners, late arrivals, and unintended flashes. Ensure changing values settle to the sourced numbers and the final hold provides reading time.

## Audio inspection

Listen to the complete output or inspect the full waveform plus representative passages. Check synchronization, intelligibility, clipping, sudden level changes, unwanted silence, harsh transients, channel imbalance, and truncated reverb or tails.

If listening is unavailable, report decoded audio measurements and waveform inspection accurately. A peak or RMS check cannot establish pleasantness, intelligibility, or perceptual synchronization.

## Reproducibility

Retain the source project, asset manifest or paths, relevant versions, and exact render command. For deterministic work, rerender representative frames at identical timestamps and confirm they match.

## Handoff

Report the absolute MP4 path, measured duration, dimensions, frame rate, video and audio codecs, and the checks actually performed. Mention a limitation only when it affects use or interpretation of the file.
