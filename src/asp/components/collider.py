"""Collider component: provides a simple AABB collider for GameObjects."""

from asp.components.component import Component
from asp.types import Vector3


class ColliderComponent(Component):
    """Axis-aligned bounding box collider.

    - size: Vector3 size of the box
    - offset: Vector3 local offset from the transform position
    """

    def __init__(self, size=None, offset=None):
        super().__init__()
        self.size = size if size is not None else Vector3(1, 1, 1)
        self.offset = offset if offset is not None else Vector3(0, 0, 0)

    def get_aabb(self):
        """Return (min, max) Vector3s in world space for the collider."""
        if self.game_object is None:
            return Vector3(), Vector3()

        from asp.components.transform import Transform
        transform = self.game_object.get_component(Transform)

        # center = transform.position + offset
        cx = transform.position.x + self.offset.x
        cy = transform.position.y + self.offset.y
        cz = transform.position.z + self.offset.z

        half_x = self.size.x / 2.0
        half_y = self.size.y / 2.0
        half_z = self.size.z / 2.0

        min_v = Vector3(cx - half_x, cy - half_y, cz - half_z)
        max_v = Vector3(cx + half_x, cy + half_y, cz + half_z)
        return min_v, max_v

    def on_collision(self, other_collider):
        """Callback invoked when this collider collides with another.

        Override or attach behavior by subclassing or monkey-patching on the instance.
        """
        return None
