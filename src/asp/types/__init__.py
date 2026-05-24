"""shared value types"""


class Vector2:
	"""Simple 2D vector with x and y values."""

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def set(self, x, y):
		self.x = x
		self.y = y
		return self

	def add(self, other):
		self.x += other.x
		self.y += other.y
		return self


class Vector3:
	"""Simple 3D vector with x, y, and z values."""

	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		return self

	def add(self, other):
		self.x += other.x
		self.y += other.y
		self.z += other.z
		return self
