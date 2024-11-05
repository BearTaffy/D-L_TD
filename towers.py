import viz
import vizshape
import vizmat
import vizact

from creeps import creeps
from camera import downCam, robot, camMode
import resources
from resources import (
    createTowerIcons,
    updateTowerIcons,
    set_resource_update_callback,
    tower_icons,
)
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

towerUpgrades = {
    "archer": {
        1: {"wood": 3, "stone": 2, "damage": 1.2, "range": 1.2, "speed": 1.2},
        2: {"wood": 5, "stone": 4, "damage": 1.4, "range": 1.4, "speed": 1.4},
        3: {"wood": 8, "stone": 6, "damage": 1.6, "range": 1.6, "speed": 1.6},
    },
    "cannon": {
        1: {"wood": 5, "stone": 3, "damage": 1.3, "range": 1.1, "speed": 1.2},
        2: {"wood": 8, "stone": 5, "damage": 1.6, "range": 1.2, "speed": 1.4},
        3: {"wood": 12, "stone": 8, "damage": 2.0, "range": 1.3, "speed": 1.6},
    },
    "wizard": {
        1: {"wood": 6, "stone": 4, "damage": 1.2, "range": 1.3, "speed": 1.3},
        2: {"wood": 10, "stone": 7, "damage": 1.4, "range": 1.6, "speed": 1.6},
        3: {"wood": 15, "stone": 10, "damage": 1.8, "range": 2.0, "speed": 2.0},
    },
}

towersPlaces = []
currentObject = None
removalMode = False

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

removal_mode_text = viz.addText("REMOVAL MODE", pos=[0.5, 0.9, 0], parent=viz.SCREEN)
removal_mode_text.alignment(viz.ALIGN_CENTER_TOP)
removal_mode_text.fontSize(24)
removal_mode_text.color(viz.RED)
removal_mode_text.visible(viz.OFF)


class Tower:
    def __init__(self, model, projectileClass, towerType):
        self.model = viz.add(model)
        self.projectileClass = projectileClass
        self.towerType = towerType
        self.level = 0
        self.attackRange = 5
        self.attackCooldown = 1.0
        self.lastAttackTime = 0
        self.highlighted = False
        self.baseDamage = 10

        self.levelText = viz.addText(f"Lvl {self.level}", parent=self.model)
        self.levelText.alignment(viz.ALIGN_CENTER_CENTER)
        self.levelText.setScale(0.5, 0.5, 0.5)
        self.levelText.setPosition(0, 2, 0)
        self.levelText.billboard(viz.BILLBOARD_VIEW)

        self.updateStats()

    def setPosition(self, pos):
        self.model.setPosition(pos)

    def getPosition(self):
        return self.model.getPosition()

    def remove(self):
        self.model.remove()

    def visible(self, state):
        self.model.visible(state)

    def highlight(self, state):
        if state:
            self.model.emissive([1, 0, 0, 1])
            self.highlighted = True
        else:
            self.model.emissive([0, 0, 0, 1])
            self.highlighted = False

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

    def updateStats(self):
        if self.level > 0:
            upgrade = towerUpgrades[self.towerType][self.level]
            self.attackRange = 5 * upgrade["range"]
            self.attackCooldown = 1.0 / upgrade["speed"]
            self.damage = self.baseDamage * upgrade["damage"]
        else:
            self.attackRange = 5
            self.attackCooldown = 1.0
            self.damage = self.baseDamage

        self.levelText.message(f"Lvl {self.level}")

    def canUpgrade(self):
        next_level = self.level + 1
        if next_level > 3:
            return False

        costs = towerUpgrades[self.towerType][next_level]
        return (
            resources.wood_count >= costs["wood"]
            and resources.stone_count >= costs["stone"]
        )

    def upgrade(self):
        if not self.canUpgrade():
            return False

        next_level = self.level + 1
        costs = towerUpgrades[self.towerType][next_level]

        resources.wood_count -= costs["wood"]
        resources.stone_count -= costs["stone"]
        resources.update_resources()

        self.level += 1
        self.updateStats()

        self.model.addAction(
            vizact.sequence(
                vizact.sizeTo([1.2, 1.2, 1.2], time=0.1),
                vizact.sizeTo([1.0, 1.0, 1.0], time=0.1),
            )
        )

        return True

    def remove(self):
        self.levelText.remove()
        self.model.remove()


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
        removal_mode_text.visible(viz.OFF)

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


def onMouseDown(button):
    global currentObject, removalMode
    if button == viz.MOUSEBUTTON_LEFT:
        if removalMode:
            mouseState = viz.mouse.getPosition()
            line = viz.MainWindow.screenToWorld(mouseState[0], mouseState[1])
            planePoint = [0, -1, 0]
            planeNormal = [0, 1, 0]
            intersectionPoint = intersect(line.begin, line.end, planePoint, planeNormal)

            if intersectionPoint:
                for towersPlace in towersPlaces:
                    if towersPlace["isPlaced"]:
                        towerPosition = towersPlace["towersPlace"].getPosition()
                        distance = vizmat.Distance(towerPosition, intersectionPoint)
                        if distance < 0.5:
                            removeTower(towersPlace)
                            break
        elif currentObject:
            for towersPlace in towersPlaces:
                if not towersPlace["isPlaced"]:
                    towerPosition = towersPlace["towersPlace"].getPosition()
                    distance = vizmat.Distance(
                        towerPosition, currentObject.getPosition()
                    )
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


def refundResources(towerType):
    costs = towerCosts[towerType]
    refundPer = 0.75

    resources.wood_count += int(costs["wood"] * refundPer)
    resources.stone_count += int(costs["stone"] * refundPer)
    resources.update_resources()


def removeTower(towersPlace):
    if towersPlace["tower"]:
        refundResources(towersPlace["tower"].towerType)
        towersPlace["tower"].remove()
        towersPlace["tower"] = None
        towersPlace["isPlaced"] = False


def toggleRemovalMode():
    global removalMode
    removalMode = not removalMode
    removal_mode_text.visible(removalMode)
    for towersPlace in towersPlaces:
        if towersPlace["tower"]:
            towersPlace["tower"].highlight(removalMode)


def attack(self, targetCreep):
    startPos = self.model.getPosition()
    startPos = [startPos[0], startPos[1] + 0.5, startPos[2]]

    newProjectile = self.projectileClass(startPos, targetCreep)
    if self.level > 0:
        upgrade = towerUpgrades[self.towerType][self.level]
        newProjectile.damage *= upgrade["damage"]

    projectiles.append(newProjectile)


def onKeyDown(key):
    global currentObject, camMode, removalMode
    if key == "q":
        if removalMode:
            toggleRemovalMode()
        changeCamera()
    elif key == " ":
        print(robot.getPosition())
    elif key == "x":
        if camMode == "downCam":
            toggleRemovalMode()
    elif camMode == "downCam" and not removalMode:
        if key in ["1", "2", "3"]:
            if currentObject:
                currentObject.remove()
                currentObject = None

            towerType = {"1": "archer", "2": "cannon", "3": "wizard"}.get(key)

            if checkResources(towerType):
                towerConfigs = {
                    "archer": (
                        "models/towers/archer_tower.obj",
                        ArrowProjectile,
                    ),
                    "cannon": (
                        "models/towers/canon.obj",
                        CannonballProjectile,
                    ),
                    "wizard": (
                        "models/towers/wizard_tower.obj",
                        MagicProjectile,
                    ),
                }

                model, projectile = towerConfigs[towerType]
                currentObject = Tower(model, projectile, towerType)
                currentObject.visible(viz.ON)
                updateObjectPosition()
    if key == "u" and camMode == "downCam" and not removalMode:
        mouseState = viz.mouse.getPosition()
        line = viz.MainWindow.screenToWorld(mouseState[0], mouseState[1])
        planePoint = [0, -1, 0]
        planeNormal = [0, 1, 0]
        intersectionPoint = intersect(line.begin, line.end, planePoint, planeNormal)

        if intersectionPoint:
            for towersPlace in towersPlaces:
                if towersPlace["isPlaced"] and towersPlace["tower"]:
                    towerPosition = towersPlace["towersPlace"].getPosition()
                    distance = vizmat.Distance(towerPosition, intersectionPoint)
                    if distance < 0.5:
                        towersPlace["tower"].upgrade()
                        break


vizact.onupdate(0, updateTowers)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)
set_resource_update_callback(updateTowerIcons)
