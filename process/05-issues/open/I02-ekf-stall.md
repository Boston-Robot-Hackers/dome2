# I02 EKF stalled for 10.65 s

Raised from `dome_semantic`'s TF33.0 robot run, 2026-11-12.

## Symptom

At 17:06:45 on 2026-11-12, `ekf_filter_node` logged "Failed to meet update
rate" and published nothing for **10.65 s**. Everything downstream of
`odom → base_footprint` stalls with it, including SLAM and the semantic
map's TF lookups.

## What has been checked

- Load, temperature, memory and throttling were all normal at the time.
- It happened once and hasn't been reproduced. Runs on 2026-11-13 didn't
  show it.

## Recurrence: 2026-11-17

During a `bl dome2 robot.launch.py --options "d f"` run, `ekf_node`
logged "Failed to meet update rate" three times:

- 20:22:45, took **2.35 s**
- 20:22:50, took **3.37 s**
- 20:22:53, took **1.48 s**

Log: `~/.ros/log/2026-11-17-20-20-12-397506-dome-R1-4425/launch.log`.

**Context at the time:**

- Load was about 0.6, 13 GB of memory was free, and `vcgencmd
  get_throttled` read `0x0`.
- No Foxglove client connection is logged, so foxglove_bridge had no
  subscriber.
- The top kernel thread was the Wi-Fi worker (`brcmf_wq/mmc1`).
- The kernel logged a lidar USB timeout earlier the same day (`cp210x
  ttyUSB0: failed set request 0x12 status: -110`, 17:10), in an earlier
  boot.

**What it looked like from outside:** in the same window the better_launch
TUI took a minute or more to respond to keys over ssh with `tmux -CC`. Keys
sent locally through `tmux send-keys` were handled at once. So that lag was
on the terminal/network path, and it may or may not share a cause with the
EKF stall.

**This weakens the slow-subscriber theory below.** No remote client was
attached to foxglove_bridge.

## Theory

Unexplained. One suspect is a DDS publish blocking on a slow subscriber,
for example the laptop's RViz over Wi-Fi. If it recurs, note whether RViz
was connected, and check `ros2 topic hz /odom` and the EKF's input topics
at the time.
