import viz
import vizshape
import vizmat

from camera import changeCamera, downCam, robot, camMode

towersPlaces = []
currentObject = None

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

from resources import wood_count, stone_count

def check_resources():
    required_wood = 5
    required_stone = 3

    # Check if enough resources for tower
    can_build = wood_count >= required_wood and stone_count >= required_stone

    return can_build
tower_icons = []

def createTowerIcons():
    global tower_icons
    tower_names = ["Archer", "Canon", "Wizard"]

    # Create and position the tower icons
    for i, name in enumerate(tower_names):
        icon = viz.addText(name, pos=[0.85, 0.85 - i * 0.05, 0], parent=viz.SCREEN)
        icon.fontSize(18)
        icon.color(viz.RED if not check_resources() else viz.GREEN)
        tower_icons.append(icon)

from resources import set_resource_update_callback

def updateTowerIcons():
    global tower_icons
    for icon in tower_icons:
        icon.color(viz.RED if not check_resources() else viz.GREEN)

# Set the callback
set_resource_update_callback(updateTowerIcons)

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
                currentObject = viz.add("models/towers/archer_tower.obj")
                currentObject.setScale([0.2, 0.2, 0.2])
                currentObject.setEuler([0, 0, 0])
            elif key == "2":
                currentObject = viz.add("models/towers/canon.obj")
                currentObject.setScale([0.25, 0.25, 0.25])
                currentObject.setEuler([0, 0, 0])
            elif key == "3":
                currentObject = viz.add("models/towers/wizard_tower.obj")
                currentObject.setScale([0.2, 0.2, 0.2])
                currentObject.setEuler([0, 0, 0])
            currentObject.visible(viz.ON)
            updateObjectPosition()
