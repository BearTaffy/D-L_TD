import viz
import vizact
import vizshape
import vizmat
import math


class Projectile:
    def __init__(self, start_pos, target, speed, damage, model):
        self.model = viz.add(model)
        self.model.setPosition(start_pos)
        self.model.setScale(0.05, 0.05, 0.05)
        self.target = target
        self.speed = speed
        self.damage = damage
        self.is_active = True

    def update(self):
        if not self.is_active or not self.target:
            self.remove()
            return True

        if not hasattr(self.target, "model") or not self.target.model:
            self.remove()
            return True

        current_pos = viz.Vector(self.model.getPosition())
        target_pos = viz.Vector(self.target.model.getPosition())
        direction = target_pos - current_pos

        if direction.length() < 0.2:
            self.hit()
            return True

        direction.normalize()
        new_pos = current_pos + direction * self.speed
        self.model.setPosition(new_pos)
        self.model.lookAt(target_pos)
        angle = math.atan2(direction[0], direction[2])
        angle_degrees = math.degrees(angle)
        self.model.setEuler([45 - angle_degrees, 0, 0])

        return False

    def hit(self):
        if self.target and hasattr(self.target, "take_damage"):
            self.target.take_damage(self.damage)
        self.remove()

    def remove(self):
        self.is_active = False
        self.model.remove()


class ArrowProjectile(Projectile):
    def __init__(self, start_pos, target):
        super().__init__(
            start_pos,
            target,
            speed=0.5,
            damage=20,
            model="models/projectiles/arrow.obj",
        )
        if not self.model:
            self.model = vizshape.addCone(height=0.2, radius=0.05)
            self.model.setPosition(start_pos)
            self.model.color(viz.YELLOW)


class CannonballProjectile(Projectile):
    def __init__(self, start_pos, target):
        super().__init__(
            start_pos,
            target,
            speed=0.2,
            damage=40,
            model="models/projectiles/cannon_ball.obj",
        )
        if not self.model:
            self.model = vizshape.addSphere(radius=0.1)
            self.model.setPosition(start_pos)
            self.model.color(viz.BLACK)


class MagicProjectile(Projectile):
    def __init__(self, start_pos, target):
        super().__init__(
            start_pos,
            target,
            speed=0.25,
            damage=30,
            model="models/projectiles/wizard_bolt.obj",
        )
        if not self.model:
            self.model = vizshape.addSphere(radius=0.08)
            self.model.setPosition(start_pos)
            self.model.color(viz.BLUE)
            self.model.emissive([0, 0, 1])


projectiles = []


def update_projectiles():
    for i in range(len(projectiles) - 1, -1, -1):
        if i < len(projectiles):
            projectile = projectiles[i]
            if projectile.update():
                if projectile in projectiles:
                    projectiles.remove(projectile)


vizact.onupdate(0, update_projectiles)
