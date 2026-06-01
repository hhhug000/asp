"""Model component for loading and parenting 3D assets."""

from asp.components.component import Component
from asp.components.transform import Transform


class Model(Component):
	"""Loads a Panda3D model, optionally applies a texture, and exposes it on the game object."""

	def __init__(self, model_path=None, texture_path=None):
		super().__init__()
		self.model_path = model_path
		self.texture_path = texture_path
		self.model = None
		self.texture = None

	def _load_model(self):
		if self.game_object is None or self.game_object.engine is None:
			raise ValueError("model component is not attached to an engine")

		if self.model_path is None:
			raise ValueError("model_path is required")

		return self.game_object.engine.loader.loadModel(self.model_path)

	def _load_texture(self):
		if self.game_object is None or self.game_object.engine is None:
			raise ValueError("model component is not attached to an engine")

		if self.texture_path is None:
			return None

		return self.game_object.engine.loader.loadTexture(self.texture_path)

	def _apply_transform(self):
		if self.game_object is None:
			return

		transform = self.game_object.get_component(Transform)
		if transform is not None:
			transform._apply()

	def _attach_model(self):
		self.model = self._load_model()
		self.model.reparentTo(self.game_object.engine.render)
		self.game_object.model = self.model

		self.texture = self._load_texture()
		if self.texture is not None:
			self.model.setTexture(self.texture, 1)

		self._apply_transform()

	def _detach_model(self):
		if self.game_object is not None and getattr(self.game_object, "model", None) is self.model:
			self.game_object.model = None

		if self.model is not None:
			self.model.removeNode()

		self.model = None
		self.texture = None

	def on_attach(self, game_object):
		super().on_attach(game_object)
		self._attach_model()

	def on_detach(self):
		self._detach_model()
		super().on_detach()

	def set_model(self, model_path):
		self.model_path = model_path
		if self.game_object is None:
			return

		self._detach_model()
		self._attach_model()

	def set_texture(self, texture_path):
		self.texture_path = texture_path
		if self.model is None:
			return

		self.texture = self._load_texture()
		if self.texture is None:
			self.model.clearTexture()
			return

		self.model.setTexture(self.texture, 1)

	def clear_texture(self):
		self.texture_path = None
		self.texture = None
		if self.model is not None:
			self.model.clearTexture()