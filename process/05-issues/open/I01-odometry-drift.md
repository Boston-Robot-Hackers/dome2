# I01 Wheel/EKF odometry drifts a lot

Raised from `dome_semantic`'s TF33.0 and TF36.7 robot runs.

## Symptom

SLAM has to correct odometry heavily during short teleop drives. The size
of that correction is `map → odom`:

- **2026-11-12** (`f33slam`): `map → odom` grew to (−0.12, 0.97 m, −25°)
  in one session.
- **2026-11-13** (`f36run6`, 387 s, about 4 min of driving):
  `map → odom` grew to (−1.10, 0.16 m, 6.7°).

The semantic map isn't affected now that it no longer re-bases targets
(`dome_semantic` F36). Nav2 and anything else that uses `odom` directly
will see the drift.

## What has been checked

Nothing in `dome2` yet. The numbers come from replaying the bags
`~/bags/f36run6` (has `/odom`, `/tf`, `/scan`) and the TF33.0 run logs in
`dome_semantic`'s `process/02-doc/current.md`.

Another detail from the bags: the EKF's `odom` once started at yaw −179.8°
rather than 0 (`~/bags/f36drive`, 2026-11-13).

## Theory

Not yet investigated. Candidates are wheel radius or track width
calibration, wheel slip, and IMU yaw drift or weighting in the EKF config.
A calibration drive is a good first check: straight 2 m, then an in-place
360°, comparing `/odom` with tape and the lidar.
