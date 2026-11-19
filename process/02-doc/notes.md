# Architecture Notes — dome2

## Environment

- Platform: Raspberry Pi, Linux 6.8.0-1057-raspi
- ROS 2 distro: **Kilted** on the robot (`/opt/ros/kilted`). Some package docs still say Jazzy.
- **Shell env comes from `~/rosutils/`**, not `.bashrc` itself. `.bashrc` sources `ros2_robot_bashrc.bash`, which sources `ros2_dome_bashrc.bash`, where the `DOME_*` variables are exported. That repo is shared with the remote computers.
- **tmux keeps removed variables alive.** New panes inherit the tmux server's copy of the environment, so a deleted export survives until `tmux set-environment -g -u NAME` or `tmux kill-server` (found 2026-11-19, retiring `DOME_VISION_CONFIG`).

## Build with `--symlink-install` (2026-11-19)

Always `colcon build --symlink-install`. Then installed `config/` files are symlinks to the source, so a config edit is live without a rebuild (`stack/config_conventions.md`).

- Without it, the installed copy goes stale. `roboflow_oak.yaml` kept `nn_threads: 1` for an hour after the source said 2.
- A package first built with copies needs its `build/<pkg>` and `install/<pkg>` removed before a symlink build. colcon won't swap copies for links. On the Pi, `dome2`, `dome_control`, `dome_nav`, `dome_vision_ros` and `dome_voice` have been switched (2026-11-19); the rest are still copies.

## Runtime gotchas (found 2026-11-17)

- **Use the ROS daemon for checks.** `ros2 node list --no-daemon` returned a
  different subset of nodes each time. After `ros2 daemon stop; ros2 daemon
  start`, the list was complete and stable.
- **`slam_toolbox` is a lifecycle node on Kilted** (2.9.0). Its launch file
  can fail to activate it; see `dome_nav` I13. Check with `ros2 lifecycle
  get /slam_toolbox`.
- **`foxglove_bridge` 3.4.1 speaks only `foxglove.sdk.v1`.** Older clients
  can't connect.
- **Kilted's rclpy raises `ExternalShutdownException` from `spin`** when a
  launch is stopped. Every node `main()` must catch it with
  `KeyboardInterrupt`, then `destroy_node()` and `rclpy.try_shutdown()`.
- **ALSA lists `seeed2micvoicec` even with the voice board removed**, so it
  can't be used to detect the board.

## Key design decisions

- Intent as JSON in `std_msgs/String` — easy to debug, weakly typed. Candidate for custom `Intent.msg` once schema stabilizes.
- Movement helpers block — acceptable for CLI experiments, risky inside ROS callbacks or autonomous behaviors.
- Behavior manager dispatches to handler objects — keep it thin, add handlers not branches.

## Known risks

- Some docs describe planned architecture not yet implemented (action servers, safety monitor).
- `dome_control` vs `control` naming inconsistency in older docs — `dome_control` is correct.
- Vision-control coupling must stay at ROS interface level (topics/services), not cross-package imports.

- **Stale colcon cache after a repo move:** a package that moved repos can leave `build/<pkg>` pointing at its old source folder (seen with `dome_telemetry_msgs`, moved out of `dome_vision`). Delete `build/<pkg>` and `install/<pkg>`, then rebuild.

- **colcon keeps deleted or renamed files in `install/`.** After a launch
  file is removed from source, `bl <pkg> <old name>` still runs the
  installed copy. Delete it from `install/<pkg>/share/<pkg>/launch/`, or
  rebuild clean.

## Sibling packages

`dome_control`, `dome_voice`, `dome_vision`, `dome_nav` all live under `~/ros2_ws/src/`.
