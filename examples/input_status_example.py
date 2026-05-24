"""Example that displays live keyboard and mouse status."""

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

from asp.engine import Engine
from asp.components import Component
from asp.gameobject import GameObject
from asp.input import InputHandler
from asp.input import keys


class InputStatusOverlay(GameObject):
	"""Simple on-screen text overlay for input state."""

	def __init__(self, engine: Engine):
		super().__init__(engine)
		self.text = OnscreenText(
			text="",
			parent=engine.aspect2d,
			pos=(-1.3, 0.92),
			align=TextNode.ALeft,
			scale=0.05,
			mayChange=True,
			fg=(0.95, 0.97, 1.0, 1.0),
			shadow=(0.0, 0.0, 0.0, 0.75),
			wordwrap=38,
		)
		self.add_component(InputStatusComponent())


class InputStatusComponent(Component):
	"""Updates the overlay with current key and mouse state."""

	def update(self, dt):
		input_state = self.game_object.engine.input
		held_keys = [key for key in InputHandler.DEFAULT_KEYS if input_state.is_held(key)]
		down_keys = [key for key in InputHandler.DEFAULT_KEYS if input_state.is_down(key)]
		released_keys = [key for key in InputHandler.DEFAULT_KEYS if input_state.is_released(key)]
		mouse_buttons = [button for button in (keys.mouse1, keys.mouse2, keys.mouse3) if input_state.mouse_held(button)]
		mouse_position = input_state.mouse_position()
		mouse_delta = input_state.mouse_delta()
		current_key = down_keys[0] if down_keys else (held_keys[0] if held_keys else "none")

		if mouse_position is None:
			mouse_position_text = "not over the window"
		else:
			mouse_position_text = f"({mouse_position.x:+.3f}, {mouse_position.y:+.3f})"

		lines = [
			"ASP input demo",
			"",
			f"Current key: {current_key}",
			f"Currently held keys: {', '.join(held_keys) if held_keys else 'none'}",
			f"Keys down this frame: {', '.join(down_keys) if down_keys else 'none'}",
			f"Keys released this frame: {', '.join(released_keys) if released_keys else 'none'}",
			f"Mouse buttons held: {', '.join(mouse_buttons) if mouse_buttons else 'none'}",
			f"Mouse position: {mouse_position_text}",
			f"Mouse delta: ({mouse_delta.x:+.3f}, {mouse_delta.y:+.3f})",
		]
		self.game_object.text.setText("\n".join(lines))


def main() -> None:
	engine = Engine()
	engine.disableMouse()
	engine.setBackgroundColor(0.06, 0.08, 0.12, 1.0)

	engine.all_entities.append(InputStatusOverlay(engine))

	engine.run()


if __name__ == "__main__":
	main()
