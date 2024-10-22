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
from resources import set_resource_update_callback
from resources import wood_count, stone_count

towersPlaces = []
tower_icons = []
currentObject = None
camMode = "robot"


class Tower:
    def __init__(self, model, scale, projectileClass):
        self.model = viz.add(model)
        self.model.setScale(scale)
        self.projectileClass = projectileClass
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





def check_resources():
    required_wood = 5
    required_stone = 3
    return wood_count >= required_wood and stone_count >= required_stone

def createTowerIcons():
    global tower_icons

    # Define the icons and their positions
    icon_paths = [
        "img/archer_tower.png",
        "img/cannon.png",
        "img/wizard_tower.png"
    ]
    
    # Clear existing icons if they are present
    if tower_icons:
        for icon in tower_icons:
            icon.remove()
        tower_icons.clear()
    
    # Add the icons to the top-right of the screen
    for i, icon_path in enumerate(icon_paths):
        icon = viz.addTexture(icon_path)
        sprite = viz.addTexQuad(texture=icon, parent=viz.SCREEN)
        sprite.setPosition([0.85, 0.85 - i * 0.1, 0])  # Adjust position as needed
        sprite.setScale([0.5, 0.5, 0.5])  # Ensure all icons are the same size
        sprite.color(viz.RED if not check_resources() else viz.GREEN)  # Set initial color based on resources
        sprite.alpha(0.5)  # Set opacity to 50% (0.0 = fully transparent, 1.0 = fully opaque)
        tower_icons.append(sprite)

def updateTowerIcons():
    for icon in tower_icons:
        if check_resources():
            icon.color(viz.GREEN)
            icon.alpha(1.0)  # Make it fully opaque if there are enough resources
        else:
            icon.color(viz.RED)
            icon.alpha(0.5)  # Make it semi-transparent if there are not enough resources





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
        
        # Create tower icons when switching to top-down view
        if not tower_icons:
            createTowerIcons()

        # Update the icons' visibility and color
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

        # Hide tower icons when switching back to the robot view
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
    global currentObject
    if button == viz.MOUSEBUTTON_LEFT:
        for towersPlace in towersPlaces:
            if not towersPlace["isPlaced"]:
                towerPosition = towersPlace["towersPlace"].getPosition()
                if (
                    currentObject
                    and vizmat.Distance(towerPosition, currentObject.getPosition())
                    < 0.5
                ):
                    towersPlace["isPlaced"] = True
                    towersPlace["tower"] = currentObject
                    currentObject.setPosition(towerPosition)
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


vizact.onupdate(0, updateTowers)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)


            
set_resource_update_callback(updateTowerIcons)