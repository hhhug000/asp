# Asp

Asp is a lightweight game engine written in Python on top of Panda3D. It centers on a small component model built around `GameObject`, `Component`, `Transform`, and a few focused engine services for input, cameras, scheduling, and simple physics.

## Features

- Scene objects built from components
- Panda3D-backed rendering and window management
- Transform, camera, model, physics, collider, and task scheduler components
- Frame-based input state with key and mouse helpers
- Ready-to-run examples for spinning objects, camera control, input status, and task scheduling

## Requirements

- Python 3.9 or newer
- Panda3D 1.10.14 or newer

## Installation

Install the package from the repository root:

```bash
pip install .
```

For editable development installs:

```bash
pip install -e .
```

## Quick Start

The smallest useful setup is an engine, a game object, and a few components:

```python
from asp.engine import Engine
from asp.components import Model, Transform
from asp.gameobject import GameObject
from asp.types import Vector3


class SpinningThing(GameObject):
    def __init__(self, engine: Engine):
	 super().__init__(engine)
	 self.add_component(Model("models/smiley", "maps/smiley.rgb"))
	 transform = self.add_component(Transform())
	 transform.set_position(Vector3(0, 8, 0))


def main() -> None:
    engine = Engine(title="asp example")
    engine.disableMouse()
    engine.all_entities.append(SpinningThing(engine))
    engine.run()


if __name__ == "__main__":
    main()
```

## Core Concepts

`Engine` is the main Panda3D application class. It owns the scene update loop, tracks active entities in `engine.all_entities`, exposes `engine.input`, and keeps the active camera synchronized with its owning object's `Transform`.

`GameObject` is the base object for anything in the scene. Components are attached with `add_component(...)`, removed with `remove_component(...)`, and looked up with `get_component(...)`.

`Component` is the base class for behavior. Override `update(dt)` to run per-frame logic.

`Transform` stores position, rotation, and scale. It automatically applies changes to an attached Panda3D model when one exists.

`Model` loads a Panda3D model and optional texture, parents it to the engine render tree, and exposes the resulting node on the owning game object as `game_object.model`.

`Camera` marks a game object as the active view target. Call `camera.activate()` on a camera component to make it drive the engine view.

`InputHandler` provides key and mouse state with helpers such as `is_down`, `is_released`, `is_held`, `mouse_position`, `mouse_delta`, and logical action bindings.

`TaskScheduler` can schedule delayed or repeating callbacks with `schedule`, `schedule_once`, `schedule_repeat`, `cancel`, and `clear`.

`PhysicsComponent` provides simple velocity-based motion, optional gravity, drag, and collision resolution against `ColliderComponent` AABBs.

`ColliderComponent` defines a simple axis-aligned bounding box with `size` and `offset` and exposes `get_aabb()` plus an `on_collision(...)` callback hook.

## Input Keys

The input module exports a `keys` namespace so gameplay code can use readable names like `keys.space`, `keys.tab`, `keys.w`, and `keys.mouse1`.

Example:

```python
from asp.input import keys

if engine.input.is_held(keys.w):
    ...
```

## Examples

Run the bundled examples directly from the repository root:

```bash
python examples/example.py
python examples/input_status_example.py
python examples/task_scheduler_example.py
python examples/physics_example.py
```

The main example demonstrates a spinning object and camera control. The dedicated input and task scheduler examples are intentionally self-contained so they are easy to run and verify.

## Project Layout

- `src/asp/engine.py` - main engine loop and window setup
- `src/asp/gameobject.py` - scene object container and component management
- `src/asp/input.py` - keyboard and mouse input handling
- `src/asp/components/` - component implementations
- `examples/` - runnable demos

## License

See [LICENSE](LICENSE) for details.
