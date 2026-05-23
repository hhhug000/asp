"""Camera component for game objects."""

from asp.components.component import Component


class Camera(Component):
	"""Marks a game object as a camera that can drive the active view."""

	def activate(self):
		if self.game_object is None or self.game_object.engine is None:
			raise ValueError("camera is not attached to an engine")

		self.game_object.engine._set_active_camera(self)

	def deactivate(self):
		if self.game_object is None or self.game_object.engine is None:
			return

		if self.game_object.engine.active_camera is self:
			self.game_object.engine._set_active_camera(None)