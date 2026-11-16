# Architecture Notes — dome2

## Environment

- Platform: Raspberry Pi, Linux 6.8.0-1057-raspi
- ROS2 distro: verify actual target (docs mention both Humble and Jazzy — resolve before chasing build issues)

## Key design decisions

- Intent as JSON in `std_msgs/String` — easy to debug, weakly typed. Candidate for custom `Intent.msg` once schema stabilizes.
- Movement helpers block — acceptable for CLI experiments, risky inside ROS callbacks or autonomous behaviors.
- Behavior manager dispatches to handler objects — keep it thin, add handlers not branches.

## Known risks

- Some docs describe planned architecture not yet implemented (action servers, safety monitor).
- `dome_control` vs `control` naming inconsistency in older docs — `dome_control` is correct.
- Vision-control coupling must stay at ROS interface level (topics/services), not cross-package imports.

- **Stale colcon cache after a repo move:** a package that moved repos can leave `build/<pkg>` pointing at its old source folder (seen with `dome_telemetry_msgs`, moved out of `dome_vision`). Delete `build/<pkg>` and `install/<pkg>`, then rebuild.

## Sibling packages

`dome_control`, `dome_voice`, `dome_vision`, `dome_nav` all live under `~/ros2_ws/src/`.
