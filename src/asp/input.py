"""Input handling for the ASP engine."""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, Dict, Set


class _Keys:
	"""Common Panda3D key names exposed as a simple namespace."""

	space = "space"
	tab = "tab"
	enter = "enter"
	escape = "escape"
	backspace = "backspace"
	shift = "shift"
	lshift = "lshift"
	rshift = "rshift"
	control = "control"
	lcontrol = "lcontrol"
	rcontrol = "rcontrol"
	alt = "alt"
	lalt = "lalt"
	ralt = "ralt"
	arrow_left = "arrow_left"
	arrow_right = "arrow_right"
	arrow_up = "arrow_up"
	arrow_down = "arrow_down"
	mouse1 = "mouse1"
	mouse2 = "mouse2"
	mouse3 = "mouse3"
	wheel_up = "wheel_up"
	wheel_down = "wheel_down"

	a = "a"
	b = "b"
	c = "c"
	d = "d"
	e = "e"
	f = "f"
	g = "g"
	h = "h"
	i = "i"
	j = "j"
	k = "k"
	l = "l"
	m = "m"
	n = "n"
	o = "o"
	p = "p"
	q = "q"
	r = "r"
	s = "s"
	t = "t"
	u = "u"
	v = "v"
	w = "w"
	x = "x"
	y = "y"
	z = "z"

	zero = "0"
	one = "1"
	two = "2"
	three = "3"
	four = "4"
	five = "5"
	six = "6"
	seven = "7"
	eight = "8"
	nine = "9"


keys = _Keys()


class InputHandler:
	"""Tracks key state and dispatches bound actions."""

	DEFAULT_KEYS = tuple(
		getattr(keys, attribute)
		for attribute in dir(keys)
		if not attribute.startswith("_") and isinstance(getattr(keys, attribute), str)
	)

	def __init__(self, engine):
		self.engine = engine
		self._held_keys: Set[str] = set()
		self._pressed_keys: Set[str] = set()
		self._released_keys: Set[str] = set()
		self._key_bindings: DefaultDict[str, Set[Callable[[], None]]] = defaultdict(set)
		self._key_up_bindings: DefaultDict[str, Set[Callable[[], None]]] = defaultdict(set)
		self._action_bindings: DefaultDict[str, Set[str]] = defaultdict(set)
		self._action_down_handlers: Dict[str, list[Callable[[], None]]] = defaultdict(list)
		self._action_up_handlers: Dict[str, list[Callable[[], None]]] = defaultdict(list)
		self._bound_keys: Set[str] = set()
		self._register_default_keys()

	def update(self):
		"""Clear transient state at the end of a frame."""
		self._pressed_keys.clear()
		self._released_keys.clear()

	def bind_key_down(self, key: str, callback: Callable[[], None]):
		"""Call a function every time a key is pressed."""
		self._ensure_key_hook(key)
		self._key_bindings[key].add(callback)

	def bind_key_up(self, key: str, callback: Callable[[], None]):
		"""Call a function every time a key is released."""
		self._ensure_key_hook(key)
		self._key_up_bindings[key].add(callback)

	def bind_key(self, key: str, callback: Callable[[], None]):
		"""Compatibility alias for bind_key_down."""
		self.bind_key_down(key, callback)

	def bind_action(self, action: str, key: str):
		"""Bind a logical action name to a physical key."""
		self._ensure_key_hook(key)
		self._action_bindings[action].add(key)

	def on_action_down(self, action: str, callback: Callable[[], None]):
		"""Call a function when a bound action is pressed."""
		self._action_down_handlers[action].append(callback)

	def on_action_up(self, action: str, callback: Callable[[], None]):
		"""Call a function when a bound action is released."""
		self._action_up_handlers[action].append(callback)

	def is_down(self, key: str) -> bool:
		"""Return True on the frame the key was pressed."""
		return key in self._pressed_keys

	def is_released(self, key: str) -> bool:
		"""Return True on the frame the key was released."""
		return key in self._released_keys

	def is_held(self, key: str) -> bool:
		"""Return True while the key remains pressed."""
		return key in self._held_keys

	def action_down(self, action: str) -> bool:
		"""Return True when any key bound to the action was pressed this frame."""
		for key in self._action_bindings.get(action, ()):
			if key in self._pressed_keys:
				return True

		return False

	def action_released(self, action: str) -> bool:
		"""Return True when any key bound to the action was released this frame."""
		for key in self._action_bindings.get(action, ()):
			if key in self._released_keys:
				return True

		return False

	def action_held(self, action: str) -> bool:
		"""Return True while any key bound to the action remains pressed."""
		for key in self._action_bindings.get(action, ()):
			if key in self._held_keys:
				return True

		return False

	def _ensure_key_hook(self, key: str):
		if key in self._bound_keys:
			return

		self._bound_keys.add(key)
		self.engine.accept(key, self._handle_key_down, [key])
		self.engine.accept(f"{key}-up", self._handle_key_up, [key])

	def _register_default_keys(self):
		for key in self.DEFAULT_KEYS:
			self._ensure_key_hook(key)

	def _handle_key_down(self, key: str):
		if key in self._held_keys:
			return

		self._held_keys.add(key)
		self._pressed_keys.add(key)

		for callback in self._key_bindings.get(key, ()):
			callback()

		for action, keys in self._action_bindings.items():
			if key in keys:
				for callback in self._action_down_handlers.get(action, ()):
					callback()

	def _handle_key_up(self, key: str):
		if key not in self._held_keys:
			return

		self._held_keys.remove(key)
		self._released_keys.add(key)

		for callback in self._key_up_bindings.get(key, ()):
			callback()

		for action, keys in self._action_bindings.items():
			if key in keys:
				for callback in self._action_up_handlers.get(action, ()):
					callback()