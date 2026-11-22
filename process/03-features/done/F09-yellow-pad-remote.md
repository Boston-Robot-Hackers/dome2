# F09 — The Yellow Pad as dome_pad, across robot and remote, with button A telling a joke

**Priority**: Medium

**Date Created:** 2026-11-22

**Done:** yes (2026-11-22)

**Tasks File Created:** yes

**Tests Written:** yes

**Test Passing:** yes (unit tests on the Mac; the robot and VM run in TF09.6, confirmed by the user)

**Description**: The Yellow Pad (an ESP32 touchscreen BLE gamepad) becomes
a DOME package, **`dome_pad`**, in its own repo
`Boston-Robot-Hackers/dome_pad`, split across both computers. It replaces
the `yellow_pad` repo.

## Scope

- **One repo holds everything for the pad:** the firmware (moved from
  `yellow_pad` with its history), the factory backup, and the ROS package.
  `arrows_v1.cpp`, the first design, is dropped.
- **Robot side (`pad` subsystem, robot.launch.py):** `joy_node` and
  `teleop_twist_joy`. These stay on the Pi: the pad pairs over Bluetooth with
  the Pi, and driving and the dead-man button mustn't depend on the VM or on
  Wi-Fi to it.
- **Remote side (`pad` subsystem, remote.launch.py):**
  - `rosbridge_server`, which feeds the pad's ROS tab. The firmware's
    `ROSBRIDGE_HOST` moves from the Pi to the VM.
  - A new `pad_buttons` node, which turns the pad's buttons into actions.
- **Button A** (joy button 1) publishes `"Tell me a robot joke."` on
  `/voice/llm_text`. dome_voice's existing LLM path does the rest: `llm_node`
  on the VM asks Claude, `voice_input` on the robot relays the reply to
  `/announcement`, and `speech_output` says it.
- **B and C stay unassigned.** The button table makes adding them a one-line
  change.

## Decisions

- **New repo, not an existing package.** dome_control runs only on the
  robot; dome_voice and dome_viz don't fit a gamepad. dome_telemetry (one
  device, split out) is the model.
- **Name `dome_pad`**, after the device, like the other DOME packages are
  named for what they do. The dome2 subsystem is `pad` on both launchers
  (was `yellow` on the robot).
- **The button node lives in `dome_pad`, not dome2.** dome2's spec is
  launch orchestration only.
- **`yellow_pad.launch.py` is removed.** It's replaced by `robot.launch.py`
  and `remote.launch.py`, both better_launch, per
  `stack/launch_conventions.md`.
- **A press fires once.** The button node acts on the press (released →
  pressed), not while the button is held.

## Out of scope

- Talking to DDS directly from the pad, without rosbridge.
- Installing the voice runtime on the Pi (Piper and friends). It's blocked
  separately (see `current.md`), and the demo can't be *heard* until it's
  done. `/announcement` can still be checked.
- Archiving the `yellow_pad` GitHub repo and removing its submodule from
  `esp32-c6-demo`: done by the user, or on request, once dome_pad is
  confirmed on the robot.

## How to Demo

**Setup**:
- dome_pad cloned and built on the Pi and the VM (`make clone`, `rosdep
  install`, `colcon build`). On the Pi, the old `~/ros2_ws/src/yellow_joy`
  copy removed.
- The pad flashed with `secrets.h`'s `ROSBRIDGE_HOST` set to the VM's
  address, and paired with the Pi.
- `ANTHROPIC_API_KEY` is set in the VM's shell.
- Pi: `bl dome2 robot.launch.py --options "d vo p"`
- VM: `bl dome2 remote.launch.py --options "vo p"`

**Steps**:
1. Hold an arrow on the pad's Drive tab. The robot moves; on release it stops.
2. Open the pad's ROS tab. It connects (green dot) and lists topics.
3. Tap A once, with `ros2 topic echo /voice/llm_text` running.

**Expected output**:
- Step 3: one `/voice/llm_text` message, then a joke on `/voice/llm_reply`
  and `/announcement`. The robot says it, once the voice runtime is
  installed on the Pi.
- Holding A sends one request, not a stream of them.

## Process Gate

After creating this feature file and the corresponding task file, **stop and present the plan to the user**. Do not write any code or content until the user gives explicit approval to proceed.
