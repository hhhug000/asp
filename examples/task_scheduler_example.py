"""Standalone example for the task scheduler component."""

from asp.components import TaskScheduler
from asp.engine import Engine
from asp.gameobject import GameObject


class ScheduledMessageDemo(GameObject):
	"""Shows the task scheduler running on an attached component."""

	def __init__(self, engine: Engine):
		super().__init__(engine)
		scheduler = self.add_component(TaskScheduler())
		scheduler.schedule_once(1.0, self._announce_once)
		scheduler.schedule_repeat(2.0, self._announce_repeat, delay=2.0)

	def _announce_once(self):
		print("task scheduler fired once")

	def _announce_repeat(self):
		print("task scheduler repeating")


def main() -> None:
	engine = Engine()
	engine.disableMouse()
	engine.setBackgroundColor(0.08, 0.1, 0.16, 1.0)
	engine.all_entities.append(ScheduledMessageDemo(engine))

	# Stop automatically so the example is easy to run and verify.
	engine.taskMgr.doMethodLater(6.0, lambda task: engine.userExit(), "StopTaskSchedulerDemo")
	engine.run()


if __name__ == "__main__":
	main()