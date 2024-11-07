import viz
import random
from sounds import hurt, death

creeps = []

creepPath = [
    [18.809349060058594, -1.0, 0.31083571910858154],
    [16.636079788208008, -1.0, 0.22646713256835938],
    [15.22624397277832, -1.0, -0.14175724983215332],
    [13.780777931213379, -1.0, -0.9165828227996826],
    [10.992467880249023, -1.0, -3.197384834289551],
    [8.952933311462402, -1.0, -5.089319705963135],
    [6.861884593963623, -1.0, -6.406467437744141],
    [4.462884426116943, -1.0, -7.200170516967773],
    [1.592442274093628, -1.0, -7.142307281494141],
    [-0.5556797385215759, -1.0, -6.296799182891846],
    [-2.9634833335876465, -1.0, -4.734012126922607],
    [-2.900617837905884, -1.0, -2.350625514984131],
    [-0.006618805229663849, -1.0, 0.35103827714920044],
    [3.5906078815460205, -1.0, 1.289689064025879],
    [6.585041046142578, -1.0, 1.8609850406646729],
    [8.661240577697754, -1.0, 3.375251293182373],
    [8.862699508666992, -1.0, 5.518925189971924],
    [7.103060722351074, -1.0, 6.651098728179932],
    [3.3767549991607666, -1.0, 6.59967565536499],
    [-0.9635977745056152, -1.0, 4.025625705718994],
    [-3.3272016048431396, -1.0, 1.6044292449951172],
    [-5.421364784240723, -1.0, 0.2095268964767456],
    [-7.969363212585449, -1.0, -0.36883723735809326],
    [-10.898310661315918, -1.0, -0.13294219970703125],
    [-13.031258583068848, -1.0, 0.329778254032135],
]
creepPathShort = [
    [19.2425594329834, -1.0, 0.24015599489212036],
    [17.67222785949707, -1.0, 0.7830374836921692],
    [16.59592056274414, -1.0, 1.289398431777954],
    [14.946025848388672, -1.0, 3.104416847229004],
    [13.262649536132812, -1.0, 4.888514041900635],
    [11.005504608154297, -1.0, 6.880936145782471],
    [8.910736083984375, -1.0, 8.414070129394531],
    [6.405872821807861, -1.0, 9.728119850158691],
    [3.7270476818084717, -1.0, 10.377726554870605],
    [0.19099773466587067, -1.0, 10.079933166503906],
    [-1.5244941711425781, -1.0, 9.076233863830566],
    [-3.6002063751220703, -1.0, 6.579322814941406],
    [-5.09058952331543, -1.0, 4.087973594665527],
    [-6.053377151489258, -1.0, 1.8131310939788818],
    [-7.630855083465576, -1.0, -0.320290207862854],
    [-9.917437553405762, -1.0, -0.7944806814193726],
    [-12.676820755004883, -1.0, 0.07906234264373779],
]


class CreepType:
    def __init__(self, model_path, scale, health, speed, damage):
        self.model_path = model_path
        self.scale = scale
        self.health = health
        self.speed = speed
        self.damage = damage


creepTypes = {
    "scout": CreepType(
        model_path="models/creeps/gargoyle.osgb",
        scale=(0.15, 0.15, 0.15),
        health=45,
        speed=0.05,
        damage=8,
    ),
    "golem": CreepType(
        model_path="models/creeps/small_golem.obj",
        scale=(0.25, 0.25, 0.25),
        health=120,
        speed=0.03,
        damage=12,
    ),
    "brute": CreepType(
        model_path="models/creeps/big_golem.obj",
        scale=(0.3, 0.3, 0.3),
        health=200,
        speed=0.02,
        damage=20,
    ),
}


class Creep:
    def __init__(self, path, creep_type):
        self.model = viz.add(creep_type.model_path)
        self.model.setScale(*creep_type.scale)
        self.path = path
        self.current_waypoint = 0
        self.speed = creep_type.speed
        self.health = creep_type.health
        self.damage = creep_type.damage
        self.marked_for_removal = False

    def move(self):
        if self.marked_for_removal:
            return

        if self.current_waypoint < len(self.path):
            target = self.path[self.current_waypoint]
            direction = viz.Vector(target) - viz.Vector(self.model.getPosition())
            if direction.length() > 0.1:
                direction.normalize()
                newPos = viz.Vector(self.model.getPosition()) + direction * self.speed
                self.model.setPosition(newPos)
                self.model.lookAt(target)
            else:
                self.current_waypoint += 1
                if self.current_waypoint >= len(self.path):
                    from waves import base_health

                    base_health.takeDamage(self.damage)
                    self.marked_for_removal = True

    def take_damage(self, damage):
        self.health -= damage
        hurt.play("audio/hurt.mp3")
        if self.health <= 0:
            self.marked_for_removal = True

    def remove(self):
        if self.model:
            self.model.remove()
            self.model = None
            death.play("audio/death.mp3")


def spawnCreep():
    creep_type_name = random.choice(list(creepTypes.keys()))
    creep_type = creepTypes[creep_type_name]

    path = creepPathShort if random.random() < 0.2 else creepPath

    newCreep = Creep(path, creep_type)
    newCreep.model.setPosition(path[0])
    creeps.append(newCreep)


def updateCreeps():
    for creep in creeps:
        creep.move()

    for creep in creeps[:]:
        if creep.marked_for_removal:
            creep.remove()
            if creep in creeps:
                creeps.remove(creep)
