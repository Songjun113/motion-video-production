# Physical motion and interaction

Read this reference when the brief calls for tactile UI, inertia, collisions, elastic motion, soft bodies, ropes, particles, or other physics-led animation.

## Shared causes

Elements responding to the same event must use the same time-stamped driver: pointer path, touch path, object state, scroll position, camera motion, beat grid, or master timeline. Derive following, force, deformation, particles, and sound from that shared state so their timing cannot drift apart.

## Springs and inertia

Use a damped spring or another continuous model for following, settling, and recoil. Choose natural frequency for response speed, damping ratio for oscillation, and effective mass for perceived weight. Carry velocity across state changes. The result must converge after input stops.

Do not assign one spring preset to every object. Large or heavy elements generally need slower response and less high-frequency motion than small controls, unless the art direction establishes another material.

## Squash and stretch

Drive deformation from velocity, acceleration, force, or impact:

- stretch along the direction of travel;
- compress across that direction;
- retain plausible area or volume;
- cap the deformation to preserve recognition and text readability;
- restore the stable shape as energy dissipates.

## Reusable physical behaviors

- **Magnetic attraction:** attenuate force with distance and release smoothly outside the influence radius.
- **Soft body:** use a particle-spring loop, mesh, or equivalent deformation field for localized dents and traveling surface response.
- **Rope or cable:** use distance constraints, Verlet integration, or an equivalent stable solver with fixed anchors and controlled iteration count.
- **Impact:** coordinate displacement, deformation, residual vibration, particles, and sound from the same collision event.
- **Particles:** seed randomness, bound counts and lifetimes, and make the state seekable or cached.

## Simulation and rendering

Prefer analytic evaluation when available. For numerical simulation, use a stable fixed step independent of preview refresh rate. Cache the state only when exact seeking or render cost requires it. Interpolate cached state for output frames and verify that high-frequency motion does not alias at the delivery frame rate.

Check extreme input, settling, collisions, constraint stretch, tunneling, and reproducibility at arbitrary seek times. Visual plausibility is the acceptance criterion for stylized motion; a stylized simulation must not be described as validated real-world physics.
