"""Physics component: handles gravity, velocity, and simple collision resolution."""

from asp.components.component import Component
from asp.types import Vector3


class PhysicsComponent(Component):
    """Basic physics integration for a GameObject.

    Properties:
    - mass: mass of the body (for future use)
    - velocity: Vector3 velocity in world space
    - acceleration: Vector3 external acceleration applied each frame
    - use_gravity: whether to apply gravity
    - gravity: Vector3 gravity acceleration (default downwards on Z)
    - drag: simple linear drag coefficient
    """

    def __init__(self, mass=1.0, use_gravity=True, gravity=None, drag=0.0):
        super().__init__()
        self.mass = mass
        self.velocity = Vector3()
        self.acceleration = Vector3()
        self.use_gravity = use_gravity
        self.gravity = gravity if gravity is not None else Vector3(0, 0, -9.81)
        self.drag = drag

    def _vec_mul(self, v: Vector3, scalar: float):
        return Vector3(v.x * scalar, v.y * scalar, v.z * scalar)

    def _vec_add(self, a: Vector3, b: Vector3):
        return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)

    def _vec_sub(self, a: Vector3, b: Vector3):
        return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)

    def update(self, dt: float):
        if self.game_object is None:
            return

        # clamp dt to avoid large jumps on frame hiccups
        max_dt = 0.05
        if dt > max_dt:
            dt = max_dt

        from asp.components.transform import Transform
        transform = self.game_object.get_component(Transform)

        if transform is None:
            return

        # compute acceleration (including gravity)
        total_acc = Vector3(self.acceleration.x, self.acceleration.y, self.acceleration.z)
        if self.use_gravity:
            total_acc.x += self.gravity.x
            total_acc.y += self.gravity.y
            total_acc.z += self.gravity.z

        # integrate velocity
        self.velocity.x += total_acc.x * dt
        self.velocity.y += total_acc.y * dt
        self.velocity.z += total_acc.z * dt

        # apply linear drag
        if self.drag and self.drag > 0:
            factor = max(0.0, 1.0 - self.drag * dt)
            self.velocity.x *= factor
            self.velocity.y *= factor
            self.velocity.z *= factor

        # integrate position
        transform.position.x += self.velocity.x * dt
        transform.position.y += self.velocity.y * dt
        transform.position.z += self.velocity.z * dt

        # basic collision detection: check other colliders and resolve overlaps
        # using an impulse-based collision response with restitution and friction
        # requires the game object to belong to an engine
        engine = getattr(self.game_object, "engine", None)
        if engine is None:
            return

        from asp.components.collider import ColliderComponent
        my_collider = self.game_object.get_component(ColliderComponent)
        if my_collider is None:
            return

        # physical parameters
        restitution = getattr(self, "restitution", 0.0)  # bounciness
        friction = getattr(self, "friction", 0.3)

        # helpers
        def dot(a: Vector3, b: Vector3):
            return a.x * b.x + a.y * b.y + a.z * b.z

        def length(v: Vector3):
            return (v.x * v.x + v.y * v.y + v.z * v.z) ** 0.5

        def normalize(v: Vector3):
            l = length(v)
            if l == 0:
                return Vector3(0, 0, 0)
            return Vector3(v.x / l, v.y / l, v.z / l)

        def mul(v: Vector3, s: float):
            return Vector3(v.x * s, v.y * s, v.z * s)

        # iterate others and solve collisions using impulses
        for other in list(engine.all_entities):
            if other is self.game_object:
                continue

            other_collider = other.get_component(ColliderComponent)
            if other_collider is None:
                continue

            # get AABBs
            a_min, a_max = my_collider.get_aabb()
            b_min, b_max = other_collider.get_aabb()

            # check overlap
            overlap_x = min(a_max.x, b_max.x) - max(a_min.x, b_min.x)
            overlap_y = min(a_max.y, b_max.y) - max(a_min.y, b_min.y)
            overlap_z = min(a_max.z, b_max.z) - max(a_min.z, b_min.z)

            if overlap_x <= 0 or overlap_y <= 0 or overlap_z <= 0:
                continue

            # compute centers
            a_center = Vector3((a_min.x + a_max.x) * 0.5, (a_min.y + a_max.y) * 0.5, (a_min.z + a_max.z) * 0.5)
            b_center = Vector3((b_min.x + b_max.x) * 0.5, (b_min.y + b_max.y) * 0.5, (b_min.z + b_max.z) * 0.5)

            # contact normal (from A to B)
            normal = normalize(Vector3(b_center.x - a_center.x, b_center.y - a_center.y, b_center.z - a_center.z))
            if length(normal) == 0:
                # fallback to smallest axis normal
                if overlap_x <= overlap_y and overlap_x <= overlap_z:
                    normal = Vector3(1, 0, 0)
                elif overlap_y <= overlap_x and overlap_y <= overlap_z:
                    normal = Vector3(0, 1, 0)
                else:
                    normal = Vector3(0, 0, 1)

            # penetration depth (approximate as minimum overlap)
            penetration = min(overlap_x, overlap_y, overlap_z)

            # find physics components and masses
            other_phys = other.get_component(PhysicsComponent)
            inv_mass_a = 0.0 if getattr(self, "mass", None) is None else (1.0 / self.mass if self.mass > 0 else 0.0)
            inv_mass_b = 0.0
            if other_phys is not None:
                inv_mass_b = 1.0 / other_phys.mass if other_phys.mass > 0 else 0.0

            # relative velocity
            va = self.velocity
            vb = other_phys.velocity if other_phys is not None else Vector3(0, 0, 0)
            rv = Vector3(vb.x - va.x, vb.y - va.y, vb.z - va.z)

            # relative velocity along normal
            vel_along_normal = dot(rv, normal)

            # do not resolve if moving apart
            if vel_along_normal > 0:
                # notify colliders for separation case too
                try:
                    my_collider.on_collision(other_collider)
                except Exception:
                    pass
                continue

            # restitution: use the smaller (more inelastic) of the two bodies if available
            e = restitution
            if other_phys is not None and hasattr(other_phys, "restitution"):
                e = min(e, getattr(other_phys, "restitution", e))

            # compute impulse scalar
            j_denom = inv_mass_a + inv_mass_b
            if j_denom == 0:
                continue

            j = -(1 + e) * vel_along_normal
            j = j / j_denom

            # apply normal impulse
            impulse = mul(normal, j)
            if inv_mass_a > 0:
                self.velocity.x -= impulse.x * inv_mass_a
                self.velocity.y -= impulse.y * inv_mass_a
                self.velocity.z -= impulse.z * inv_mass_a
            if inv_mass_b > 0:
                other_phys.velocity.x += impulse.x * inv_mass_b
                other_phys.velocity.y += impulse.y * inv_mass_b
                other_phys.velocity.z += impulse.z * inv_mass_b

            # friction (Coulomb)
            # recompute relative velocity after normal impulse
            va = self.velocity
            vb = other_phys.velocity if other_phys is not None else Vector3(0, 0, 0)
            rv = Vector3(vb.x - va.x, vb.y - va.y, vb.z - va.z)

            # tangent
            tangent = Vector3(rv.x - normal.x * dot(rv, normal), rv.y - normal.y * dot(rv, normal), rv.z - normal.z * dot(rv, normal))
            tangent_norm = length(tangent)
            if tangent_norm > 1e-6:
                tangent = Vector3(tangent.x / tangent_norm, tangent.y / tangent_norm, tangent.z / tangent_norm)

                jt = -dot(rv, tangent)
                jt = jt / j_denom

                # Coulomb friction
                mu = friction
                if other_phys is not None and hasattr(other_phys, "friction"):
                    mu = (mu + getattr(other_phys, "friction", mu)) * 0.5

                # clamp magnitude
                if abs(jt) > j * mu:
                    jt = -j * mu if jt < 0 else j * mu

                friction_impulse = mul(tangent, jt)
                if inv_mass_a > 0:
                    self.velocity.x -= friction_impulse.x * inv_mass_a
                    self.velocity.y -= friction_impulse.y * inv_mass_a
                    self.velocity.z -= friction_impulse.z * inv_mass_a
                if inv_mass_b > 0:
                    other_phys.velocity.x += friction_impulse.x * inv_mass_b
                    other_phys.velocity.y += friction_impulse.y * inv_mass_b
                    other_phys.velocity.z += friction_impulse.z * inv_mass_b

            # positional correction to avoid sinking (Baumgarte)
            percent = 0.2  # usually 20% to 80%
            slop = 0.01
            correction_mag = max(penetration - slop, 0.0) / j_denom * percent
            correction = mul(normal, correction_mag)
            if inv_mass_a > 0:
                transform.position.x -= correction.x * inv_mass_a
                transform.position.y -= correction.y * inv_mass_a
                transform.position.z -= correction.z * inv_mass_a
            if inv_mass_b > 0:
                # move other object if dynamic
                from asp.components.transform import Transform
                other_transform = other.get_component(Transform)
                if other_transform is not None:
                    other_transform.position.x += correction.x * inv_mass_b
                    other_transform.position.y += correction.y * inv_mass_b
                    other_transform.position.z += correction.z * inv_mass_b

            # notify colliders
            try:
                my_collider.on_collision(other_collider)
            except Exception:
                pass

        # apply transform to visual/model after physics & collision resolution
        try:
            transform._apply()
        except Exception:
            pass
