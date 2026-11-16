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

## Theory

Unexplained. One suspect is a DDS publish blocking on a slow subscriber,
for example the laptop's RViz over Wi-Fi. If it recurs, note whether RViz
was connected, and check `ros2 topic hz /odom` and the EKF's input topics
at the time.
