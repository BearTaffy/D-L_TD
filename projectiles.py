import viz
import vizact
import vizshape
import vizmat
import math


projectiles = []


class Projectile:
    def __init__(self, startPos, target, speed, damage, model, sound):
        self.model = viz.add(model)
        self.model.setPosition(startPos[0], 0.5, startPos[2])
        self.model.setScale(0.1, 0.1, 0.1)
        self.target = target
        self.speed = speed
        self.damage = damage
        self.is_active = True
        self.sound = sound

    def update(self):
        player = viz.addSoundMixer()
        player.play(self.sound, viz.SOUND_PRELOAD)
        if not self.is_active or not self.target:
            self.remove()
            return True

        if not hasattr(self.target, "model") or not self.target.model:
            self.remove()
            return True

        currentPos = viz.Vector(self.model.getPosition())
        targetPos = viz.Vector(self.target.model.getPosition())
        direction = targetPos - currentPos

        if direction.length() < 0.2:
            self.hit()
            player.play(self.sound)
            return True

        direction.normalize()
        new_pos = currentPos + direction * self.speed
        self.model.setPosition(new_pos)
        self.model.lookAt(targetPos)

        direction = viz.Vector(targetPos) - viz.Vector(currentPos)
        direction.normalize()
        angle = math.atan2(direction[0], direction[2])
        angleDegrees = math.degrees(angle)
        self.model.setEuler([45 - angleDegrees, 0, 0])

        return False

    def hit(self):
        if self.target and hasattr(self.target, "take_damage"):
            self.target.take_damage(self.damage)
        self.remove()

    def remove(self):
        self.is_active = False
        self.model.remove()


class ArrowProjectile(Projectile):
    def __init__(self, startPos, target):
        super().__init__(
            startPos,
            target,
            speed=1.0,
            damage=15,
            model="models/projectiles/arrow.obj",
            sound="audio/arrow.mp3",
        )
        if not self.model:
            self.model = vizshape.addCone(height=0.2, radius=0.05)
            self.model.setPosition(startPos)
            self.model.color(viz.YELLOW)


class CannonballProjectile(Projectile):
    def __init__(self, startPos, target):
        super().__init__(
            startPos,
            target,
            speed=0.6,
            damage=45,
            model="models/projectiles/cannon_ball.obj",
            sound="audio/cannon.mp3",
        )
        if not self.model:
            self.model = vizshape.addSphere(radius=0.1)
            self.model.setPosition(startPos)
            self.model.color(viz.BLACK)


class MagicProjectile(Projectile):
    def __init__(self, startPos, target):
        super().__init__(
            startPos,
            target,
            speed=0.7,
            damage=35,
            model="models/projectiles/wizard_bolt.obj",
            sound="audio/wizard.mp3",
        )
        if not self.model:
            self.model = vizshape.addSphere(radius=0.08)
            self.model.setPosition(startPos)
            self.model.color(viz.BLUE)
            self.model.emissive([0, 0, 1])


def updateProjectiles():
    for i in range(len(projectiles) - 1, -1, -1):
        if i < len(projectiles):
            projectile = projectiles[i]
            if projectile.update():
                if projectile in projectiles:
                    projectiles.remove(projectile)


vizact.onupdate(0, updateProjectiles)
