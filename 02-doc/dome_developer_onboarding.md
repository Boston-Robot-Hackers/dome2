# Dome ROS2 System: Developer Onboarding Guide

## Purpose

This guide explains how the Dome ROS2 codebase is organized and how a new developer should extend it. It is intentionally architectural rather than file-by-file. The key mental model is: **inputs produce normalized intents, the control layer interprets them, behavior handlers act on them, and output nodes announce results.**

## High-level architecture

The uploaded workspace is organized around four major packages:

```text
dome2              Top-level launch orchestrator
dome_control       CLI, intent routing, robot movement/control, behavior manager
dome_voice         Wake word + offline STT + intent mapping + speech output
dome_vision        OAK-D / Roboflow vision, ROS bridge, semantic map, scene services
```

There are also expected external packages such as `linorobot2_bringup`, `robot_localization`, `foxglove_bridge`, and base driver packages. `dome2` does not own robot behavior; it composes the subsystem launch files.

## Runtime data flow

The core flow is:

```text
voice / CLI / future REST / button
        ↓
JSON intent on /intent
        ↓
behavior_manager
        ↓
MotionBehavior / PerceptionBehavior / future handlers
        ↓
/cmd_vel, /describe_scene service, vision topics, map services, etc.
        ↓
/announcement
        ↓
speech output / CLI reply / future display or LEDs
```

The important design choice is that commands are not supposed to remain tied to one UI. Voice, CLI, and future APIs should all converge on the same normalized intent path whenever possible.

## Package roles

### `dome2`: launch composition

`dome2` is the system launcher. It launches combinations of control, vision, voice, base driver, EKF, URDF state publisher, and Foxglove telemetry. Treat this package as orchestration glue.

Typical extension work here:

- Add a new subsystem launch include.
- Add a launch argument or environment-controlled mode.
- Adjust robot-vs-remote launch behavior.
- Wire a new node into the full robot startup.

Do not put robot logic in `dome2`.

### `dome_control`: command and behavior layer

`dome_control` is the main control package. It contains three related but distinct layers:

```text
Command registry / CLI
        ↓
RobotController methods and ROS2 API wrappers
        ↓
BehaviorManager intent router
```

There are two ways commands currently enter the system:

1. **Direct command dispatch**, used by the CLI for commands like `move.forward`, `robot.stop`, `config.get`, `system.topics`.
2. **Intent dispatch**, used for higher-level semantic commands like `describe_scene`, `list_objects`, `explore`, and voice-originated commands.

The direct command registry is built from small command-definition modules. Each command maps a command name to a `RobotController` method plus typed parameters. The dispatcher parses text, expands abbreviations, validates parameters, and invokes the method.

The behavior manager subscribes to `/intent`, parses JSON intent messages, and sends them to behavior handler objects such as `MotionBehavior` and `PerceptionBehavior`.

### `dome_voice`: audio input and spoken output

`dome_voice` is the offline voice interface. Its input node runs wake word detection and Vosk STT, maps transcripts to normalized intent dictionaries, and publishes JSON strings on `/intent`.

The key point for developers: **voice should not directly control motors.** It should publish an intent and let `dome_control` decide what to do.

To add a voice phrase, update the grammar/runtime vocabulary and the phrase-to-intent mapper. Then make sure the resulting intent is handled by `dome_control`.

### `dome_vision`: vision and semantic perception

`dome_vision` has a Python vision library plus a ROS-facing package, `dome_vision_ros`. The ROS nodes publish OAK-D images, detections, 3D detections, markers, performance diagnostics, and semantic-map outputs.

The semantic map node exposes `/describe_scene` as a `std_srvs/Trigger` service. `dome_control` calls this service from `PerceptionBehavior` when it receives `describe_scene`.

The current perception command path is therefore:

```text
voice says "describe" or CLI publishes describe_scene
        ↓
/intent { name: "describe_scene", source: ..., slots: {} }
        ↓
behavior_manager
        ↓
PerceptionBehavior
        ↓
/describe_scene service
        ↓
/announcement with response text
```

## Important ROS interfaces

### Topics

```text
/intent                         std_msgs/String containing JSON intent
/announcement                   dome_control/Announcement
/cmd_vel                        geometry_msgs/Twist
/odom                           nav_msgs/Odometry
/voice/state                    std_msgs/String
/oak/detections                 vision_msgs/Detection2DArray
/oak/detections_3d              vision_msgs/Detection3DArray
/oak/image_raw                  sensor_msgs/Image
/oak/image_annotated            sensor_msgs/Image
/oak/image_compressed           sensor_msgs/CompressedImage
/oak/image_annotated_compressed sensor_msgs/CompressedImage
/oak/perf                       std_msgs/String JSON diagnostics, optional
/targets/confirmed              std_msgs/String
/targets/markers                visualization_msgs/MarkerArray
/targets/assoc_diag             std_msgs/String
```

### Services

```text
/describe_scene                 std_srvs/Trigger
```

### Custom message

`dome_control/msg/Announcement.msg` is the structured output contract. It carries:

```text
text
priority
stamp
source
dedup_key
```

This is the right mechanism for speech/display/LED output to consume robot responses without knowing who requested them.

## Theory of operation

### Intent messages

The system uses JSON in `std_msgs/String` for intents. The shape is:

```json
{
  "name": "describe_scene",
  "source": "voice",
  "slots": {}
}
```

This is simple and easy to debug with `ros2 topic echo /intent`, but it is looser than a custom ROS message. If this codebase matures, a custom `Intent.msg` would be a good cleanup.

### Behavior manager

The behavior manager is the brain-like router. It does not currently implement a full action-server architecture; instead it dispatches to handler objects.

Current handler pattern:

```python
class SomeBehavior:
    def handles(self, intent_name: str) -> bool:
        ...

    def execute(self, intent, node) -> None:
        ...
```

Use this pattern for new semantic behaviors. Keep the behavior manager thin: add handlers, but avoid stuffing behavior logic directly into `on_intent`.

### Direct CLI commands

The CLI command path uses `CommandDef` objects:

```python
CommandDef(
    method_name="move_forward",
    parameters=[ParameterDef("meters", float, True, None, "Distance in meters")],
    description="Move robot forward by distance",
    group="movement",
)
```

The dispatcher converts text into command names and positional arguments. If the last parameter is a string, extra tokens are joined; this is why a command like `robot speak hello world` can work naturally.

### Movement

Movement is implemented by publishing `Twist` messages to `/cmd_vel`. Time-based movement blocks in `cmd_vel_helper`, publishes velocity at 10 Hz for the requested duration, then publishes zero velocity.

This is acceptable for manual CLI experiments, but long-running autonomous behaviors should not block a ROS callback. Use timers, actions, or separate behavior nodes for anything longer or more complex.

### Vision lifecycle nodes

The OAK-D vision nodes are lifecycle nodes. They configure publishers and model resources during `on_configure`, open devices and start threads in `on_activate`, and shut down in lifecycle callbacks. This is the right pattern for hardware-heavy nodes.

## How to add a new direct CLI command

Use this path for low-level developer commands such as diagnostics, calibration, maps, process inspection, or one-shot movement.

### 1. Add a `RobotController` method

Example:

```python
def get_battery_status(self) -> CommandResponse:
    return self.power_api.get_battery_status()
```

If you need ROS interaction, add or reuse a `ros2_api/*_api.py` wrapper and have `RobotController` delegate to it.

### 2. Add a command definition

Add it to the right command module, or create a new one if it is a new domain.

```python
"robot.battery": CommandDef(
    method_name="get_battery_status",
    parameters=[],
    description="Report battery voltage and status",
    group="control",
)
```

### 3. Ensure the dispatcher imports that command set

`CommandDispatcher._build_command_registry()` merges command dictionaries. If you create a new command module, import it and call its builder there.

### 4. Add docs and tests

Add a small help text file under `docs/` if this follows the existing pattern. Add a test that checks command registration and dispatch.

### 5. Try it

```bash
ros2 run dome_control run
# then inside CLI:
robot battery
```

## How to add a new voice command

Use this path when a spoken phrase should trigger behavior.

### 1. Choose the normalized intent

Example:

```text
name: list_objects
source: voice
slots: {}
```

Do not use the spoken phrase as the behavior name. Use stable intent names.

### 2. Add the phrase to `dome_voice`

Extend the mapper phrase table:

```python
(("what do you see", "objects"), "list_objects")
```

Also add the necessary words or phrases to the constrained Vosk grammar in the voice runtime config. If the grammar does not include the phrase vocabulary, recognition quality will be poor or impossible.

### 3. Handle the intent in `dome_control`

If an existing behavior handles it, add the new intent name to that behavior’s intent set. Otherwise add a new behavior handler.

For perception commands, follow the `PerceptionBehavior` model. For movement commands, follow `MotionBehavior`.

### 4. Publish an announcement

If the command has a human-facing result, publish an `Announcement` on `/announcement`. Let the speech output node speak it.

### 5. Test without audio first

Before testing the microphone path, publish the intent directly:

```bash
ros2 topic pub --once /intent std_msgs/msg/String \
  "{data: '{\"name\": \"list_objects\", \"source\": \"test\", \"slots\": {}}'}"
```

Then test via CLI, then via voice.

## How to add a new semantic behavior

Use this path for higher-level robot capabilities: explore, find object, go to room, survey, return home.

### 1. Create a behavior handler

```python
class BatteryBehavior:
    def handles(self, intent_name: str) -> bool:
        return intent_name == "battery_status"

    def execute(self, intent, node) -> None:
        ...
```

### 2. Register it in `BehaviorManagerNode`

Add it to the `self.handlers` list.

```python
self.handlers = [
    MotionBehavior(rc),
    PerceptionBehavior(self),
    BatteryBehavior(self),
]
```

### 3. Keep ROS details inside the behavior or a ROS API wrapper

If it calls services, create clients on the node. If it publishes commands, use a clear output topic. If it is long-running, do not block the callback; use an action server or timer-driven state machine.

### 4. Return status through `/announcement`

This keeps CLI, speech, display, and logs consistent.

## How to add new vision functionality

Use this path for new perception products: object counts, target lists, room summaries, tracked-object queries, etc.

### 1. Decide whether it belongs in library code or ROS glue

Put reusable perception logic in `dome_vision/dome_vision/*`. Put publishers, subscribers, services, TF, lifecycle, and ROS message conversion in `dome_vision_ros`.

### 2. Add or extend a ROS interface

Options:

- Add a new topic if data streams continuously.
- Add a new service if the control layer asks a query.
- Add an action if the operation is long-running and cancellable.

For example, `count_objects` probably wants either:

```text
/count_objects service
```

or a richer semantic-map query service, rather than duplicating detection parsing inside `dome_control`.

### 3. Wire control to vision through services or topics

Avoid importing deep vision internals directly into `dome_control` except for lightweight config helpers. Prefer ROS interfaces.

## How to add a new launchable node

### 1. Add a console script entry point

In the package `setup.py`:

```python
entry_points={
    "console_scripts": [
        "my_node = my_package.my_module:main",
    ],
}
```

### 2. Add launch file wiring

For subsystem launch, add it to that package’s launch file. For full robot launch, include it through `dome2`.

### 3. Rebuild and source

```bash
cd ~/ros2_ws
colcon build --packages-select <package_name>
source install/setup.bash
```

### 4. Verify ROS graph

```bash
ros2 node list
ros2 topic list
ros2 service list
```

## Development workflow

Recommended loop:

```bash
cd ~/ros2_ws
colcon build --packages-select dome_control dome_voice dome_vision_ros
source install/setup.bash
pytest src/dome_control/test
pytest src/dome_voice/test
pytest src/dome_vision/dome_vision_ros/tests
```

For runtime debugging:

```bash
ros2 topic echo /intent
ros2 topic echo /announcement
ros2 topic echo /voice/state
ros2 topic echo /oak/detections
ros2 service call /describe_scene std_srvs/srv/Trigger {}
```

Use the CLI to isolate control behavior before involving voice or vision hardware.

## Extension decision guide

```text
Need a developer-only command?        Add CommandDef + RobotController method.
Need a spoken command?                Add voice phrase → intent → behavior handler.
Need a robot behavior?                Add behavior handler, maybe later action server.
Need continuous perception data?      Add/extend a vision topic.
Need query-style perception result?   Add/extend a service.
Need startup composition?             Add launch wiring in subsystem package, then dome2.
Need human-facing robot output?       Publish /announcement.
```

## Current architectural strengths

- Clear separation between launch orchestration, control, voice, and vision.
- Normalized `/intent` topic lets multiple inputs share behavior logic.
- `/announcement` is a clean output contract for speech/display/UI.
- Vision lifecycle nodes are appropriate for hardware startup/shutdown.
- CLI command registry is easy to extend and test.
- Tests exist across control, voice, and vision packages.

## Current design risks and cleanup opportunities

1. **Intent is JSON in `std_msgs/String`.** Easy to debug, but weakly typed. Consider a custom `Intent.msg` once the schema stabilizes.
2. **Some docs mention planned architecture not fully implemented.** The documentation talks about action servers and safety monitor concepts, but current code mostly uses direct behavior handlers and services.
3. **Movement helpers block.** Fine for simple CLI movement, risky inside ROS callbacks or future autonomous behaviors.
4. **Behavior manager can become a god object.** Keep adding behavior classes rather than adding branches directly into `on_intent`.
5. **Control package naming looks inconsistent in docs.** Some docs refer to `control`; the package appears to be `dome_control`.
6. **ROS distro references are mixed.** Some docs say Humble, others say Jazzy. Developers should verify the actual target environment before chasing build issues.
7. **Vision-control coupling should remain ROS-level.** Avoid reaching across packages into internals when a service/topic/action is cleaner.

## Suggested next feature: implement `count_objects`

The code already has placeholders for `count_objects`. A clean implementation would be:

1. Add a service in `semantic_map_node`, for example `/count_objects`, or extend `/describe_scene` if a quick text-only answer is enough.
2. In `PerceptionBehavior`, replace the warning with a service call.
3. Publish the result as an announcement.
4. Add `count` / `how many` phrases to the voice mapper and grammar.
5. Add tests for intent mapping and behavior routing.
6. Validate with direct `/intent` publishing before testing the voice path.

This path exercises the intended architecture without requiring motor movement.
