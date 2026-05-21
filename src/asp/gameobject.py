"""game object class and component system"""


from asp.component import Component


class GameObject:
	"""base class for everything that exists in the scene"""

	def __init__(self, engine=None):
		self.engine = engine
		self.components = []
		self._destroyed = False

	def add_component(self, component):
		component.on_attach(self)
		self.components.append(component)
		return component

	def remove_component(self, component):
		if component in self.components:
			self.components.remove(component)
			component.on_detach()

	def get_component(self, component_type):
		for component in self.components:
			if isinstance(component, component_type):
				return component
		return None

	def _update_components(self, dt):
		for component in list(self.components):
			component.update(dt)

	def destroy(self):
		self._destroyed = True
		for component in list(self.components):
			self.remove_component(component)
