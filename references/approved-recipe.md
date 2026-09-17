# EEG finger-control example

The public showcase explains Ding et al., *EEG-based brain-computer interface enables real-time robotic hand control at individual finger level*, Nature Communications 16, 5401 (2025). DOI: https://doi.org/10.1038/s41467-025-61064-x.

## Visual treatment

A 20-second landscape example follows four beats: an articulated robotic hand and oversized opening type on cream; an EEG-to-decoder mechanism on cobalt; a close-up command timeline on lilac; trial-level motor-imagery results on mint. Draw text, traces, joints, packets, networks, counters, and transition masks as independent layers.

## Evidence boundaries

The study's 80.56% and 60.61% are mean online MI trial accuracies for two and three classes in 21 screened healthy experienced BCI users after online training and fine-tuning. A 125 ms command update uses the latest 1-second EEG window; feedback starts after the first second. Animated hands, waveforms and packets are explanatory drawings, not recorded experimental data. These results do not establish simultaneous independent control of all fingers or clinical recovery.

## Reproduction and adaptation

Source belongs in `assets/eeg-finger-control/`. Use Python 3.10+, Pillow, NumPy and imageio-ffmpeg. Follow the README for render and QA commands. Copy the example to a writable project before adapting it. Typography uses installed fonts or explicit font overrides.

Preserve varied framing, saturated scene contrast, reading holds, independent object movement, and transitions motivated by visible objects. Adapt scene count, duration, palette, and claims to the new brief. This renderer illustrates one paper; it does not automatically read arbitrary papers.
