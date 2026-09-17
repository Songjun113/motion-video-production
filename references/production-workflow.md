# Production workflow

Use this reference after selecting a production route. Apply visual-direction.md before the first keyframes.

## 1. Build the scene plan

For each scene record its purpose, start and end times, focal element, supporting elements, initial state, peak state, final state, primary motion, transition relation, text, assets, and audio cue. Every scene must earn its duration by advancing the message or establishing a necessary pause.

Record the outgoing object and incoming object at every scene boundary. Allocate reading holds within the duration rather than adding them after the timeline is filled.

Use a single composition for a short continuous piece. Split reusable scenes or a piece with several hard cuts into sub-compositions when the chosen tool supports them.

## 2. Establish design before animation

Define the background and foreground, palette, typography, layout grid, safe areas, shape language, material treatment, and depth rules. Use one clear focal point per beat. Keep text readable at the target viewing size.

Build each scene's representative still first. Check composition, hierarchy, copy accuracy, asset fidelity, and cross-scene consistency. Animate only after those stills pass review.

Use the approved contact sheet as a quality reference. Adjacent scenes should change the viewer's focus through scale, position, depth, density, or background role. A stable identity does not require identical geometry.

## 3. Animate in dependency order

Implement large structural motion before secondary responses and decoration:

1. camera, scene, or main-object movement;
2. transitions and continuity between scenes;
3. text and information reveals;
4. supporting motion and interaction responses;
5. blur, particles, highlights, and micro-motion;
6. captions and audio synchronization.

Give every motion an object, cause, start, duration, direction, velocity profile, and stable end state. Use pauses to let the viewer read. Let transitions preserve a visible relation through direction, shape, position, color, or sound.

Build scene functions or equivalent independently animated layers. PNG contact sheets serve review; the final composition must realize the proposed internal action. Preserve readable endpoint frames and a settled final state. Keep sound event times in the timeline or an explicit event schedule.

Use depth, motion blur, elastic deformation, and camera effects only when motivated by speed, focus, material, or spatial structure. Keep the focal subject readable. Avoid continuous camera motion that makes UI, diagrams, or text hard to follow.

## 4. Work with product and factual content

Prefer real product captures, confirmed designs, and user-provided data. A reconstructed interface must be labeled as a mockup or concept when it could be mistaken for an implemented product. Do not invent business results, metrics, quotes, or interface states that appear factual.

Preserve aspect ratios and crop deliberately. Preload all frame sequences and media. When using recorded UI, synchronize the embedded media time with the master timeline.

## 5. Design audio with the picture

Choose deliberate silence or an audio identity containing the applicable layers: narration, music, ambience, transitions, interaction sounds, impacts, and an ending mark.

Align sounds to the same events that drive the image. Pan localized effects from their on-screen horizontal position when it improves spatial coherence. Use user-owned, licensed, generated, recorded, or parameterically synthesized audio with known provenance.

Check narration intelligibility, frequency masking, harsh transients, low-frequency buildup, clipping, and cut-off tails. Platform requirements determine final loudness and peak targets. Real narration duration overrides estimated timing.

## 6. Assemble and review

Render a low-cost preview before the final encode. Review the opening, closing, every transition, every text change, motion peaks, and quiet holds. For multi-scene work, generate a contact sheet using representative frames from all scenes.

Apply revisions at their responsible layer: copy errors in content, hierarchy errors in design, timing errors in the timeline, simulation errors in the motion model, and encoding artifacts in export settings.

Keep the scene plan, asset paths, versions, render command, and output path with the project so another run can reproduce the delivery.
