"""Transform component inside the components package."""

from asp.types import Vector3
from asp.components.component import Component


class Transform(Component):
	"""stores position rotation and scale for a game object."""

	def __init__(self):
		super().__init__()
		self.position = Vector3()
		self.rotation = Vector3()
		self.scale = Vector3(1, 1, 1)

	def _resolve_vector(self, value, y=None, z=None):
		if y is None and z is None and hasattr(value, "x") and hasattr(value, "y") and hasattr(value, "z"):
			return value.x, value.y, value.z

		return value, y, z

	def set_position(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.position.set(x, y, z)
		self._apply()

	def add_position(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.position.add(Vector3(x, y, z))
		self._apply()

	def set_rotation(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.rotation.set(x, y, z)
		self._apply()

	def add_rotation(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.rotation.add(Vector3(x, y, z))
		self._apply()

	def set_scale(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.scale.set(x, y, z)
		self._apply()

	def add_scale(self, x, y=None, z=None):
		x, y, z = self._resolve_vector(x, y, z)
		self.scale.add(Vector3(x, y, z))
		self._apply()

	def set_position_vector(self, position):
		self.position.set(position.x, position.y, position.z)
		self._apply()

	def add_position_vector(self, position):
		self.position.add(position)
		self._apply()

	def set_rotation_vector(self, rotation):
		self.rotation.set(rotation.x, rotation.y, rotation.z)
		self._apply()

	def add_rotation_vector(self, rotation):
		self.rotation.add(rotation)
		self._apply()

	def set_scale_vector(self, scale):
		self.scale.set(scale.x, scale.y, scale.z)
		self._apply()

	def add_scale_vector(self, scale):
		self.scale.add(scale)
		self._apply()

	def move_position_x(self, amount):
		self.position.x += amount
		self._apply()

	def move_position_y(self, amount):
		self.position.y += amount
		self._apply()

	def move_position_z(self, amount):
		self.position.z += amount
		self._apply()

	def move_rotation_x(self, amount):
		self.rotation.x += amount
		self._apply()

	def move_rotation_y(self, amount):
		self.rotation.y += amount
		self._apply()

	def move_rotation_z(self, amount):
		self.rotation.z += amount
		self._apply()

	def move_scale_x(self, amount):
		self.scale.x += amount
		self._apply()

	def move_scale_y(self, amount):
		self.scale.y += amount
		self._apply()

	def move_scale_z(self, amount):
		self.scale.z += amount
		self._apply()

	def _apply(self):
		if self.game_object is None:
			return

		model = getattr(self.game_object, "model", None)
		if model is None:
			return

		model.setPos(self.position.x, self.position.y, self.position.z)
		model.setHpr(self.rotation.x, self.rotation.y, self.rotation.z)
		model.setScale(self.scale.x, self.scale.y, self.scale.z)
