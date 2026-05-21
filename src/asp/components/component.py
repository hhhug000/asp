"""Component base implementation inside the components package."""


class Component:
	"""base class for components, so they can be attached to game objects"""

	def __init__(self):
		self.game_object = None

	def on_attach(self, game_object):
		self.game_object = game_object

	def on_detach(self):
		self.game_object = None

	def update(self, dt):
		"""Override in subclasses to run per-frame logic."""
		return None
