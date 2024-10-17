# TODO: refactor code into separate files
# TODO: camera/player
# TODO: add creeps
# TODO: add creep pathing
# TODO: material collection minigame
# TODO: add sound
# TODO: make tower placement
# When in downCam show green square where tower can be placed
# prob a dict with values like cords and is tower placed
# TODO: add tower removal
# TODO: make tower attack creeps
# ? for wizrad tower make bolt have a light that folows it

import viz
import vizshape
import vizcam
import vizact
import vizmat
import vizinfo
import random
import math
import vizproximity



# ? when selected tower make tower follow cursor and when clicked place tower if in area of a tower place

# Environment
mapp = viz.add("models/map.obj")
mapp.setPosition(0, -1, 0)

day = viz.add("sky_day.osgb")
day.renderToBackground()

tree=viz.add("models/tree.obj")
tree.setPosition(-8.4,-1,-7.7)
tree.setScale([0.5, 0.5, 0.5])


# Variables
camMode = "robot"
wood_count = 0
stone_count = 0
collecting_wood = False

# Create text for resource counters
wood_text = viz.addText(f"Wood: {wood_count}", pos=[0.1, 0.9, 0], parent=viz.SCREEN)
wood_text.fontSize(20)
wood_text.color(viz.WHITE)

stone_text = viz.addText(f"Stone: {stone_count}", pos=[0.1, 0.85, 0], parent=viz.SCREEN)
stone_text.fontSize(20)
stone_text.color(viz.WHITE)

# Function to update resource display
def update_resources():
    wood_text.message(f"Wood: {wood_count}")
    stone_text.message(f"Stone: {stone_count}")
    


# Variables
camMode = "robot"
towersPlaces = []
towderCoordinates = [
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

currentObject = None

# Models
robot = viz.add("models/robot.obj")
robot.setPosition([-1, -1, 2])
robot.setScale([0.1, 0.1, 0.1])
robot.setEuler([0, 0, 0])

def add_wood():
    global wood_count
    wood_count += 1
    update_resources()

# Proximity manager setup
manager = vizproximity.Manager()
manager.setDebug(True)
manager.addTarget(vizproximity.Target(robot))

# Enter sensor function
def onEnterSensor(e):
    global collecting_wood
    if e.sensor.name == 'Circle':
        viz.logNotice('Entered wood collection area')
        collecting_wood = True
        # Start collecting wood every 2 seconds
        vizact.ontimer2(2, 0, add_wood)  # Repeats every 2 seconds

# Exit sensor function
def onExitSensor(e):
    global collecting_wood
    if e.sensor.name == 'Circle':
        viz.logNotice('Exited wood collection area')
        collecting_wood = False

manager.onEnter(None, onEnterSensor)
manager.onExit(None, onExitSensor)

def AddSensor(shape, name):
    sensor = vizproximity.Sensor(shape, None)
    sensor.name = name
    manager.addSensor(sensor)

# Add circular sensor around the tree
shape = vizproximity.CircleArea(3, center=[-8.21, -7.7])
AddSensor(shape, 'Circle')

# Screen setup
viz.setMultiSample(4)
viz.fov(90)
viz.go(viz.FULLSCREEN)
viz.clearcolor(viz.SKYBLUE)

viz.mouse.setVisible(True)
viz.mouse.setTrap(viz.ON)
viz.mouse.setOverride(viz.ON)

# Lights
head_light = viz.MainView.getHeadLight()
viz.MainView.getHeadLight().disable()
head_light.intensity(0.5)

dir_light = viz.addDirectionalLight(color=viz.WHITE, euler=(45, 135, 0))
dir_light = viz.addDirectionalLight(color=viz.WHITE, euler=(45, 0, 45))
dir_light.direction(0, -1, 0)
dir_light.intensity(0.5)

# Cam/Movement
navigator = vizcam.addWalkNavigate(moveScale=2.0)
viz.cam.setHandler(navigator)
viz.MainView.collision(viz.OFF)

downCam = vizshape.addSphere(radius=0.1)
downCam.setPosition(0, 11, 1)

viewLink = viz.link(robot, viz.MainView)
viewLink.preEuler([0, 45, 0])
viewLink.preTrans([0, 0, -3])
viewLink.preEuler([0, -20, 0])

robotLink = viz.link(navigator, robot)
robotLink.postTrans([0, -1, 1])

for coord in towderCoordinates:
    towersPlace = vizshape.addCube(size=0.5)
    towersPlace.setPosition(coord)
    towersPlace.alpha(0)
    towersPlaces.append({"towersPlace": towersPlace, "isPlaced": False, "tower": None})


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
                currentObject = vizshape.addCube(size=0.5, color=viz.RED)
            elif key == "2":
                currentObject = vizshape.addSphere(radius=0.25, color=viz.GREEN)
            elif key == "3":
                currentObject = vizshape.addCylinder(
                    height=0.5, radius=0.25, color=viz.BLUE
                )
            currentObject.visible(viz.ON)
            updateObjectPosition()


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


viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.MOUSEDOWN_EVENT, onMouseDown)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)







if __name__ == "__main__":
    viz.go()
