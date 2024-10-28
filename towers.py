import viz
import vizshape
import vizmat
import vizact

from creeps import creeps
from camera import changeCamera, downCam, robot, camMode
from resources import (
    createTowerIcons,
    updateTowerIcons,
    set_resource_update_callback,
    tower_icons,
    wood_count,
    stone_count,
)
import resources

from projectiles import (
    ArrowProjectile,
    CannonballProjectile,
    MagicProjectile,
    projectiles,
)

towerCosts = {
    "archer": {"wood": 5, "stone": 3},
    "cannon": {"wood": 8, "stone": 5},
    "wizard": {"wood": 10, "stone": 8},
}

towersPlaces = []
currentObject = None
camMode = "robot"

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


class Tower:
    def __init__(self, model, scale, projectileClass, towerType):
        self.model = viz.add(model)
        self.model.setScale(scale)
        self.projectileClass = projectileClass
        self.towerType = towerType
        self.attackRange = 5
        self.attackCooldown = 1.0
        self.lastAttackTime = 0

    def setPosition(self, pos):
        self.model.setPosition(pos)

    def getPosition(self):
        return self.model.getPosition()

    def remove(self):
        self.model.remove()

    def visible(self, state):
        self.model.visible(state)

    def update(self, currentTime):
        if currentTime - self.lastAttackTime >= self.attackCooldown:
            closestCreep = None
            minDistance = float("inf")
            towerPos = self.model.getPosition()

            for creep in creeps:
                if creep.model:
                    creepPos = creep.model.getPosition()
                    distance = vizmat.Distance(towerPos, creepPos)
                    if distance < self.attackRange and distance < minDistance:
                        minDistance = distance
                        closestCreep = creep

            if closestCreep:
                self.attack(closestCreep)
                self.lastAttackTime = currentTime

    def attack(self, targetCreep):
        startPos = self.model.getPosition()
        startPos = [startPos[0], startPos[1] + 0.5, startPos[2]]

        newProjectile = self.projectileClass(startPos, targetCreep)
        projectiles.append(newProjectile)

        # self.model.lookAt(targetCreep.model.getPosition())


for coord in towerCoordinates:
    towersPlace = vizshape.addCube(size=0.5)
    towersPlace.setPosition(coord)
    towersPlace.alpha(0)
    towersPlaces.append({"towersPlace": towersPlace, "isPlaced": False, "tower": None})


def changeCamera():
    global camMode, currentObject, tower_icons
    if camMode == "robot":
        viewLink = viz.link(downCam, viz.MainView)
        viewLink.preEuler([0, 90, 0])
        camMode = "downCam"

        for towersPlace in towersPlaces:
            towersPlace["towersPlace"].alpha(1)

        if not tower_icons:
            createTowerIcons()

        for icon in tower_icons:
            icon.visible(viz.ON)
        updateTowerIcons()

    else:
        viewLink = viz.link(robot, viz.MainView)
        viewLink.preEuler([0, 45, 0])
        viewLink.preTrans([0, 0, -3])
        viewLink.preEuler([0, -20, 0])
        camMode = "robot"

        for towersPlace in towersPlaces:
            towersPlace["towersPlace"].alpha(0)

        if tower_icons:
            for icon in tower_icons:
                icon.visible(viz.OFF)

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


def updateTowers():
    currentTime = viz.tick()
    for towersPlace in towersPlaces:
        if towersPlace["isPlaced"] and towersPlace["tower"]:
            towersPlace["tower"].update(currentTime)

cost={
    "Tower": "Archer-tower" "Cannon" "Wizard-tower",
    "Wood": "5" "5" "8",
    "Stone": "3" "8" "12"
}


def onMouseDown(button):
    global currentObject
    if button == viz.MOUSEBUTTON_LEFT and currentObject:
        for towersPlace in towersPlaces:
            if not towersPlace["isPlaced"]:
                towerPosition = towersPlace["towersPlace"].getPosition()
                distance = vizmat.Distance(towerPosition, currentObject.getPosition())
                if distance < 0.5:
                    if checkResources(currentObject.towerType):
                        towersPlace["isPlaced"] = True
                        towersPlace["tower"] = currentObject
                        currentObject.setPosition(towerPosition)
                        removeResources(currentObject.towerType)
                        currentObject = None
                        break
                    else:
                        currentObject.remove()
                        currentObject = None
                        break


def checkResources(towerType):
    costs = towerCosts[towerType]
    hasEnough = (
        resources.wood_count >= costs["wood"]
        and resources.stone_count >= costs["stone"]
    )
    return hasEnough


def removeResources(towerType):
    costs = towerCosts[towerType]
    resources.wood_count -= costs["wood"]
    resources.stone_count -= costs["stone"]
    resources.update_resources()


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
                currentObject = None

            towerType = {"1": "archer", "2": "cannon", "3": "wizard"}.get(key)

            if checkResources(towerType):
                towerConfigs = {
                    "archer": (
                        "models/towers/archer_tower.obj",
                        [0.2, 0.2, 0.2],
                        ArrowProjectile,
                    ),
                    "cannon": (
                        "models/towers/canon.obj",
                        [0.25, 0.25, 0.25],
                        CannonballProjectile,
                    ),
                    "wizard": (
                        "models/towers/wizard_tower.obj",
                        [0.2, 0.2, 0.2],
                        MagicProjectile,
                    ),
                }

                model, scale, projectile = towerConfigs[towerType]
                currentObject = Tower(model, scale, projectile, towerType)
                currentObject.visible(viz.ON)
                updateObjectPosition()


vizact.onupdate(0, updateTowers)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)
set_resource_update_callback(updateTowerIcons)