---
name: motion-video-production
description: Create polished product-style motion videos and research explainers as complete MP4s from papers, text, interfaces, data, images, or footage. Includes visual direction, varied compositions, object transitions, layered animation, sound, rendering, and encoded-file QA. Use for video creation and revision.
---

# Motion Video Production

Deliver a playable, inspected MP4. Storyboards, keyframes, source projects, and previews are intermediate artifacts unless the user narrows the request.

## Start from the approved quality reference

For an unspecified visual direction, start with [references/visual-direction.md](references/visual-direction.md). The public example explains an EEG finger-control paper; [references/approved-recipe.md](references/approved-recipe.md) documents its treatment and reproducible source. View the example storyboard when available before designing new keyframes.

Carry forward varied composition, purposeful palette changes, large focal elements, object continuity, independently animated layers, sound tied to events, and a readable closing hold. Adapt imagery and copy to the new subject. The supplied paper, numbers, four-scene structure, 20-second duration, and exact palette belong to the example.

The user's feedback established these defaults: bright or light surfaces with a saturated accent scene; asymmetric layouts; substantial changes in focal scale and placement; product-demo pacing. Repeated dark backgrounds and identical title-plus-card layouts did not satisfy the intended style. Follow an explicit brand or user direction when it differs.

## Establish the brief

Extract the message, audience, intended action, duration, aspect ratio, delivery platform, brand rules, required assets, audio needs, and editable-project requirements. Ask only about missing facts that would materially change content, cost, or route. Record assumptions that affect the result.

Treat references as evidence of desired composition, rhythm, color, typography, or motion behavior. Do not copy protected characters, logos, music, or distinctive assets without authorization. Keep real product footage, reconstructed interfaces, simulations, and concept visuals clearly identified.

For a paper, read the supplied version and visually check the source figure or table for each featured claim. Record source pages and metric definitions in the project. Design a short story around the problem, mechanism, and supported result. Label invented demonstration text and preserve the evaluation scope in readable on-screen copy or an unobtrusive note. Do not transplant the example's metrics into a new topic.

## Choose the production route

Honor a user-specified tool or existing project. Otherwise choose the smallest reliable route that can meet the visual and delivery requirements:

- Use a web, SVG, Canvas, WebGL, Remotion, or HyperFrames route for UI animation, typography, explainers, deterministic graphics, and reusable parameterized scenes.
- Use FFmpeg or an available nonlinear editor for footage-led cutting, timing, compositing, subtitles, encoding, and audio assembly.
- Use Blender or an equivalent 3D route when lighting, camera parallax, geometry, materials, or physically coherent 3D motion is central.
- Use Python or another numerical route for data animation, scientific plots, offline simulation, procedural assets, or audio synthesis.
- Use a mixed route when real footage or product capture must sit inside a programmatic scene.

Base the choice on available tools, asset type, determinism, editability, batch needs, render cost, and portability. State the chosen route and why in one concise progress update. Do not install a new dependency or use a paid or authenticated service without the authority required by the environment.

This skill owns the brief and review sequence. Use available specialist skills for the selected renderer or media operation as needed, without repeating intake questions already answered. The user has authorized automatic route selection; a framework preference alone is not a reason to replace a suitable existing route. For Python graphics and FFmpeg, read [references/python-rendering.md](references/python-rendering.md).

## Work in two approval stages

Default to `design review -> full production`.

### Stage 1: design review

Create a compact treatment containing:

- one-sentence objective and viewer arc;
- actual target duration and output format;
- scene-by-scene storyboard with purpose, timing, content, motion, transition, and audio cue;
- the recurring visual object and what it becomes at each scene boundary;
- visual system: palette, typography, spacing, focal element, depth, and safe areas;
- representative keyframes covering every major visual mode and the ending;
- proposed production route and required assets.

Inspect the keyframes at the target aspect ratio. They must already communicate each scene's main point without relying on animation. Present them for confirmation before full animation.

Inspect the contact sheet for composition diversity before showing it. A sequence of equal-sized panels under repeated headers needs a design revision. Preserve visual identity through typography, color roles, materials, and recurring objects. Assess style against the bundled approved contact sheet.

Skip the user-facing checkpoint when the user explicitly requests direct production, no intermediate confirmation, or full automation. Still create and inspect the storyboard and keyframes internally.

### Stage 2: full production

After approval, implement every scene, transition, title, caption, audio layer, and ending. Preserve confirmed design decisions unless a technical constraint makes a change necessary; surface such a change at the decision point.

Positive acceptance such as “看上去还不错”, “可以”, or “按这个做” following the concrete preview authorizes this stage. Continue through the final MP4 without asking for the same approval again. “太黑”, “布局死板”, or comparable criticism calls for a visible keyframe revision before full production.

Read [references/production-workflow.md](references/production-workflow.md) for scene construction, animation, audio, and assembly. For physical or interaction-led motion, also read [references/motion-physics.md](references/motion-physics.md).

Render foreground objects, text, highlights, and data marks as independent layers. Static PNGs are review artifacts; moving an entire PNG does not implement the approved object animation. Give every major scene at least one meaningful internal action, and every major transition a stated spatial or semantic relation. Preserve a legible first frame and a stable final hold, about two seconds for a 20-second short.

## Preserve deterministic rendering when applicable

For programmatic animation, use one authoritative timeline and make frame state a function of time, inputs, asset versions, and seeded randomness. A live preview may use a real-time playback loop, but that loop must only advance the authoritative time. Offline rendering must be able to seek to exact frame times.

Preload local assets and fonts. Do not depend on render-time network requests, wall clocks, uncontrolled timers, or unseeded randomness. Cache a simulation only when direct evaluation cannot reproduce it reliably or meet render cost; choose its sample rate from the dynamics and output frame rate.

## Render and verify the MP4

Unless the user or publishing platform specifies otherwise, use:

- MP4 container, H.264 video, AAC audio;
- 1920x1080 for landscape, 1080x1920 for portrait, or 1080x1080 for square;
- 30 fps, 48 kHz stereo audio, `yuv420p`, and fast-start metadata.

Adapt bitrate, frame rate, codec profile, loudness, and color handling to the content and destination. Text, gradients, and fast movement must survive compression without obvious damage.

Read and execute [references/mp4-qa.md](references/mp4-qa.md) before declaring completion. A successful render command alone is insufficient.

Use [scripts/verify_mp4.py](scripts/verify_mp4.py) for reusable metadata, full decode, frame sampling, and audio measurement. Inspect its extracted contact sheet and key frames yourself; the script reports visual and listening review as pending. Use the project-specific brief, not the example, as the expected duration, size, and frame rate.

## Completion contract

The task is complete only when:

- the confirmed scope is present in the rendered video;
- the MP4 plays from start to finish;
- duration, dimensions, frame rate, codecs, and audio match the target;
- key frames and the final encoded video have been visually inspected;
- there are no known black or blank frames, missing assets, substituted fonts, layout overflow, obvious judder, broken transitions, clipping, or audio-sync errors;
- the final response links the MP4 by absolute path and reports its measured duration and encoding parameters;
- the editable project, assets, and reproduction instructions are retained when the task requires them.

If a required asset, credential, approval, renderer, or codec remains unavailable, report the concrete blocker and the completed intermediate artifacts. Do not describe a storyboard, preview, GIF, or source project as the final video.
