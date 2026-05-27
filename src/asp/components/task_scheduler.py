"""Task scheduling component for game objects."""

from dataclasses import dataclass, field
from itertools import count
from typing import Any, Callable

from asp.components.component import Component


@dataclass
class _ScheduledTask:
	task_id: int
	remaining: float
	callback: Callable[..., Any]
	args: tuple[Any, ...] = ()
	kwargs: dict[str, Any] = field(default_factory=dict)
	repeat: bool = False
	interval: float = 0.0


class TaskScheduler(Component):
	"""Schedules delayed and repeating callbacks for an attached game object."""

	def __init__(self):
		super().__init__()
		self._next_task_id = count(1)
		self._tasks: dict[int, _ScheduledTask] = {}

	def schedule(self, delay, callback, *args, repeat=False, interval=None, **kwargs):
		"""Schedule a callback to run after a delay."""
		if delay < 0:
			raise ValueError("delay must be non-negative")

		if repeat:
			if interval is None:
				interval = delay
			if interval <= 0:
				raise ValueError("repeat interval must be greater than zero")

		task_id = next(self._next_task_id)
		self._tasks[task_id] = _ScheduledTask(
			task_id=task_id,
			remaining=delay,
			callback=callback,
			args=args,
			kwargs=dict(kwargs),
			repeat=repeat,
			interval=interval if interval is not None else 0.0,
		)
		return task_id

	def schedule_once(self, delay, callback, *args, **kwargs):
		"""Schedule a callback to run once after a delay."""
		return self.schedule(delay, callback, *args, **kwargs)

	def schedule_repeat(self, interval, callback, *args, delay=None, **kwargs):
		"""Schedule a callback to repeat every interval seconds."""
		if delay is None:
			delay = interval

		return self.schedule(delay, callback, *args, repeat=True, interval=interval, **kwargs)

	def cancel(self, task_id):
		"""Cancel a scheduled task."""
		return self._tasks.pop(task_id, None) is not None

	def clear(self):
		"""Cancel all scheduled tasks."""
		self._tasks.clear()

	def has_task(self, task_id):
		"""Return true when a task is still scheduled."""
		return task_id in self._tasks

	def on_detach(self):
		self.clear()
		super().on_detach()

	def update(self, dt):
		if not self._tasks:
			return

		for task in list(self._tasks.values()):
			if task.task_id not in self._tasks:
				continue

			task.remaining -= dt
			while task.task_id in self._tasks and task.remaining <= 0:
				task.callback(*task.args, **task.kwargs)

				if task.task_id not in self._tasks:
					break

				if not task.repeat:
					self._tasks.pop(task.task_id, None)
					break

				task.remaining += task.interval
