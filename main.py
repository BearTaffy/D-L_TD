import viz
import vizshape
import vizcam
import vizact
import vizmat
import vizinfo
import random
import math

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


# Environment
mapp = viz.add("models/map.obj")
mapp.setPosition(0, -1, 0)

day = viz.add("sky_day.osgb")
day.renderToBackground()


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

for coord in towderCoordinates:
    towersPlace = vizshape.addCube(size=0.5)
    towersPlace.setPosition(coord)
    towersPlace.alpha(0)
    towersPlaces.append({"towersPlace": towersPlace, "isPlaced": False, "tower": None})

# Models
robot = viz.add("models/robot.obj")
# golem = viz.add("models/big_golem.obj")
# robot.alpha(0)

robot.setPosition([-1, -1, 2])
robot.setScale([0.1, 0.1, 0.1])
robot.setEuler([0, 0, 0])

# Screen
viz.setMultiSample(4)
viz.fov(90)
viz.go(viz.FULLSCREEN)
viz.clearcolor(viz.SKYBLUE)

viz.mouse.setVisible(True)
viz.mouse.setTrap(viz.ON)
viz.mouse.setOverride(viz.ON)

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


def onKeyDown(key):
    if key == "q":
        changeCamera()
    if key == " ":
        print(robot.getPosition())


def changeCamera():
    global camMode
    if camMode == "robot":
        viewLink = viz.link(downCam, viz.MainView)
        viewLink.preEuler([0, 90, 0])
        camMode = "downCam"
        for towersPlace in towersPlaces[:]:
            obj = towersPlace["towersPlace"]
            towerPlaced = towersPlace["isPlaced"]
            whichTower = towersPlace["tower"]

            obj.alpha(1)

    else:
        viewLink = viz.link(robot, viz.MainView)
        viewLink.preEuler([0, 45, 0])
        viewLink.preTrans([0, 0, -3])
        viewLink.preEuler([0, -20, 0])
        camMode = "robot"
        for towersPlace in towersPlaces[:]:
            obj = towersPlace["towersPlace"]
            obj.alpha(0)


# Lights
head_light = viz.MainView.getHeadLight()
viz.MainView.getHeadLight().disable()
head_light.intensity(0.5)

dir_light = viz.addDirectionalLight(color=viz.WHITE, euler=(45, 135, 0))
dir_light = viz.addDirectionalLight(color=viz.WHITE, euler=(45, 0, 45))
dir_light.direction(0, -1, 0)
dir_light.intensity(0.5)

viz.callback(viz.KEYDOWN_EVENT, onKeyDown)

if __name__ == "__main__":
    viz.go()
