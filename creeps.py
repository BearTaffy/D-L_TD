import viz

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


class Creep:
    def __init__(self, path):
        self.model = viz.add("models/creeps/ICE.obj")
        self.model.setScale(0.2, 0.2, 0.2)
        self.path = path
        self.current_waypoint = 0
        self.speed = 0.1
        self.health = 100

    def move(self):
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
        else:
            self.remove()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.remove()

    def remove(self):
        self.model.remove()
        creeps.remove(self)


def spawnCreep():
    newCreep = Creep(creepPath)
    newCreep.model.setPosition(creepPath[0])
    creeps.append(newCreep)


def updateCreeps():
    for creep in creeps:
        creep.move()
