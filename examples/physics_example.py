"""Simple physics demo: a falling box onto a static ground plane.

Run with a working Panda3D installation.
"""

from asp.engine import Engine
from asp.gameobject import GameObject
from asp.components import Transform, PhysicsComponent, ColliderComponent, Model, Camera
from asp.types import Vector3
from asp.components import Component


def main():
    engine = Engine("Physics Example")
    # configure renderer and camera like other examples
    engine.disableMouse()
    engine.setBackgroundColor(0.08, 0.1, 0.16, 1.0)

    # camera rig (uses Camera component API from examples)
    cam_rig = GameObject(engine)
    cam_transform = cam_rig.add_component(Transform())
    cam_transform.set_position(Vector3(0, -20, 6))
    cam_transform.set_rotation(Vector3(10, 0, 0))
    cam = cam_rig.add_component(Camera())
    engine.all_entities.append(cam_rig)
    cam.activate()

    # ground (static collider)
    ground = GameObject(engine)
    ground_transform = ground.add_component(Transform())
    ground_transform.set_position(0, 0, -1)
    ground_collider = ground.add_component(ColliderComponent(size=Vector3(20, 20, 2)))
    engine.all_entities.append(ground)

    # falling box
    box = GameObject(engine)
    box_transform = box.add_component(Transform())
    box_transform.set_position(0, 0, 5)
    box_collider = box.add_component(ColliderComponent(size=Vector3(1, 1, 1)))
    physics = box.add_component(PhysicsComponent(use_gravity=True, drag=0.1))
    physics.velocity = Vector3(0, 0, 0)
    engine.all_entities.append(box)

    # attach Model components so visuals are loaded using the project's Model API
    ground_model_comp = ground.add_component(Model("models/box"))
    # ensure transform applied after model attach
    ground_transform._apply()

    box_model_comp = box.add_component(Model("models/smiley", "maps/smiley.rgb"))
    box_transform._apply()

    # second ball placed above the first to collide with it
    ball2 = GameObject(engine)
    ball2_transform = ball2.add_component(Transform())
    # offset on X so collision is off-center and causes rolling
    ball2_transform.set_position(Vector3(0.8, 0, 9))
    ball2_collider = ball2.add_component(ColliderComponent(size=Vector3(1, 1, 1)))
    ball2_physics = ball2.add_component(PhysicsComponent(use_gravity=True, drag=0.05))
    ball2_physics.velocity = Vector3(0, 0, 0)
    # give a small sideways velocity so the balls collide off-center and roll apart
    ball2_physics.velocity.x = -0.5
    ball2_model = ball2.add_component(Model("models/smiley", "maps/smiley.rgb"))
    ball2_transform._apply()
    engine.all_entities.append(ball2)

    # simple logger to print positions each frame for debugging
    class PosLogger(Component):
        def update(self, dt):
            t1 = box.get_component(Transform)
            t2 = ball2.get_component(Transform)
            print(f"dt={dt:.4f} box z={t1.position.z:.3f}, ball2 z={t2.position.z:.3f}, v1={physics.velocity.z:.3f}, v2={ball2_physics.velocity.z:.3f}")

    logger = GameObject(engine)
    logger.add_component(PosLogger())
    engine.all_entities.append(logger)

    engine.run()


if __name__ == "__main__":
    main()
