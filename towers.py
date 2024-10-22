import viz
import vizshape
import vizmat
import vizact

from creeps import creeps
from camera import changeCamera, downCam, robot, camMode
from projectiles import (
    ArrowProjectile,
    CannonballProjectile,
    MagicProjectile,
    projectiles,
)

towersPlaces = []
currentObject = None
camMode = "robot"


class Tower:
    def __init__(self, model, scale, projectile_class):
        self.model = viz.add(model)
        self.model.setScale(scale)
        self.projectile_class = projectile_class
        self.attack_range = 5
        self.attack_cooldown = 1.0
        self.last_attack_time = 0

    def setPosition(self, pos):
        self.model.setPosition(pos)

    def getPosition(self):
        return self.model.getPosition()

    def remove(self):
        self.model.remove()

    def visible(self, state):
        self.model.visible(state)

    def update(self, current_time):
        if current_time - self.last_attack_time >= self.attack_cooldown:
            closest_creep = None
            min_distance = float("inf")
            tower_pos = self.model.getPosition()

            for creep in creeps:
                if creep.model:
                    creep_pos = creep.model.getPosition()
                    distance = vizmat.Distance(tower_pos, creep_pos)
                    if distance < self.attack_range and distance < min_distance:
                        min_distance = distance
                        closest_creep = creep

            if closest_creep:
                self.attack(closest_creep)
                self.last_attack_time = current_time

    def attack(self, target_creep):
        start_pos = self.model.getPosition()
        start_pos = [start_pos[0], start_pos[1] + 0.5, start_pos[2]]

        new_projectile = self.projectile_class(start_pos, target_creep)
        projectiles.append(new_projectile)

        # self.model.lookAt(target_creep.model.getPosition())


towerCoordinates = [
    [12.7, -1.0, 1.1],
    [10.6, -1.0, 5.0],
    [7.0, -1.0, 8.0],
    [1.6, -1.0, 8.0],
    [-3.1, -1.0, 3.5],
    [-7.3, -1.0, 3.5],
    [-5.1, -1.0, 6.8],
    [-2.5, -1.0, 9.8],
    [1.1, -1.0, 11.7],
    [5.4, -1.0, 11.8],
    [8.5, -1.0, 10.9],
    [12.1, -1.0, 9.0],
    [14.6, -1.0, 7.1],
    [15.6, -1.0, -0.8],
    [12.8, -1.0, -3.8],
    [9.7, -1.0, -6.8],
    [6.0, -1.0, -8.3],
    [1.1, -1.0, -8.3],
    [-5.0, -1.0, -3.7],
    [-7.8, -1.0, -2.2],
    [-4.4, -1.0, -0.8],
    [7.7, -1.0, -3.8],
    [4.8, -1.0, -5.3],
    [1.0, -1.0, -5.3],
    [-1.0, -1.0, -3.4],
    [10.0, -1.0, -1.1],
    [0.5, -1.0, 2.0],
    [3.5, -1.0, 3.1],
    [6.0, -1.0, 4.2],
    [0.8, -1.0, -1.1],
    [6.3, -1.0, -0.1],
    [-2.8, -1.0, -6.7],
]

for coord in towerCoordinates:
    towersPlace = vizshape.addCube(size=0.5)
    towersPlace.setPosition(coord)
    towersPlace.alpha(0)
    towersPlaces.append({"towersPlace": towersPlace, "isPlaced": False, "tower": None})


def changeCamera():
    global camMode, currentObject
    if camMode == "robot":
        viewLink = viz.link(downCam, viz.MainView)
        viewLink.preEuler([0, 90, 0])
        camMode = "downCam"
        for towersPlace in towersPlaces:
            towersPlace["towersPlace"].alpha(1)
    else:
        viewLink = viz.link(robot, viz.MainView)
        viewLink.preEuler([0, 45, 0])
        viewLink.preTrans([0, 0, -3])
        viewLink.preEuler([0, -20, 0])
        camMode = "robot"
        for towersPlace in towersPlaces:
            towersPlace["towersPlace"].alpha(0)
        if currentObject:
            currentObject.remove()
            currentObject = None


def intersect(lineStart, lineEnd, planePoint, planeNormal):
    lineDir = viz.Vector(lineEnd) - viz.Vector(lineStart)
    lineDir.normalize()
    planeNormal = viz.Vector(planeNormal)
    planeNormal.normalize()

    linePoint = viz.Vector(lineStart) - viz.Vector(planePoint)
    linePointOfDir = -planeNormal.dot(linePoint) / planeNormal.dot(lineDir)
    intersection = viz.Vector(lineStart) + linePointOfDir * lineDir
    return intersection


def updateObjectPosition():
    global currentObject
    if currentObject and camMode == "downCam":
        mouseState = viz.mouse.getPosition()
        line = viz.MainWindow.screenToWorld(mouseState[0], mouseState[1])
        planePoint = [0, -1, 0]
        planeNormal = [0, 1, 0]

        intersectionPoint = intersect(line.begin, line.end, planePoint, planeNormal)

        if intersectionPoint:
            currentObject.setPosition(intersectionPoint)


def update_towers():
    current_time = viz.tick()
    for towersPlace in towersPlaces:
        if towersPlace["isPlaced"] and towersPlace["tower"]:
            towersPlace["tower"].update(current_time)


def onMouseDown(button):
    global currentObject
    if button == viz.MOUSEBUTTON_LEFT:
        for towersPlace in towersPlaces:
            if not towersPlace["isPlaced"]:
                tower_position = towersPlace["towersPlace"].getPosition()
                if (
                    currentObject
                    and vizmat.Distance(tower_position, currentObject.getPosition())
                    < 0.5
                ):
                    towersPlace["isPlaced"] = True
                    towersPlace["tower"] = currentObject
                    currentObject.setPosition(tower_position)
                    currentObject = None
                    break


def onKeyDown(key):
    global currentObject, camMode
    if key == "q":
        changeCamera()
    elif key == " ":
        print(robot.getPosition())
    elif camMode == "downCam":
        if key in ["1", "2", "3"]:
            if currentObject:
                currentObject.remove()
            if key == "1":
                currentObject = Tower(
                    "models/towers/archer_tower.obj", [0.2, 0.2, 0.2], ArrowProjectile
                )
            elif key == "2":
                currentObject = Tower(
                    "models/towers/canon.obj", [0.25, 0.25, 0.25], CannonballProjectile
                )
            elif key == "3":
                currentObject = Tower(
                    "models/towers/wizard_tower.obj", [0.2, 0.2, 0.2], MagicProjectile
                )
            currentObject.visible(viz.ON)
            updateObjectPosition()


vizact.onupdate(0, update_towers)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)
