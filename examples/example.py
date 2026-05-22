"""Basic usage example for the ASP engine."""

from asp.engine import Engine
from asp.components import Component
from asp.gameobject import GameObject
from asp.components import Transform
from asp.types import Vector3


class SpinComponent(Component):
	"""Rotate the owning game object's model each frame."""

	def __init__(self):
		super().__init__()

	def update(self, dt):
		transform = self.game_object.get_component(Transform)
		if transform is not None:
			transform.add_rotation(Vector3(90.0 * dt, 0, 0))


class SpinningThing(GameObject):
	"""Visible game object that spins a model each frame."""

	def __init__(self, engine: Engine):
		super().__init__(engine)
		self.model = engine.loader.loadModel("models/smiley")
		self.model.reparentTo(engine.render)
		transform = self.add_component(Transform())
		transform.set_position(Vector3(0, 8, 0))
		transform.set_scale(Vector3(1.5, 1.5, 1.5))
		self.add_component(SpinComponent())


def main() -> None:
	engine = Engine()
	engine.disableMouse()
	engine.camera.setPos(0, -20, 3)
	engine.camera.lookAt(0, 8, 0)
	engine.setBackgroundColor(0.08, 0.1, 0.16, 1.0)

	engine.all_entities.append(SpinningThing(engine))

	# Stop automatically so the example is easy to run and verify.
	engine.taskMgr.doMethodLater(6.0, lambda task: engine.userExit(), "StopDemo")
	engine.run()


if __name__ == "__main__":
	main()
