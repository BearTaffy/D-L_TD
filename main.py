import viz
import vizshape
import vizcam
import vizact
import vizmat
import vizinfo
import random
import math

# TODO: refactor code

viz.mouse.setVisible(False)


mapp = viz.add("models/map.obj")
mapp.setPosition(0, -1, 0)

day = viz.add("sky_day.osgb")
day.renderToBackground()
camMode = "robot"


robot = viz.add("models/robot.obj")
# golem = viz.add("models/big_golem.obj")


robot.setPosition([-1, -1, 2])
robot.setScale([0.1, 0.1, 0.1])
robot.setEuler([0, 0, 0])

# Screen
viz.setMultiSample(4)
viz.fov(90)
viz.go(viz.FULLSCREEN)
viz.clearcolor(viz.SKYBLUE)

# Cam/Movement

navigator = vizcam.addWalkNavigate(moveScale=2.0)
viz.cam.setHandler(navigator)
viz.MainView.collision(viz.OFF)

viz.MainView.setPosition(0, 0, 0)
viz.MainView.setEuler(0, 0, 0)


downCam = vizshape.addSphere(radius=0.1)
downCam.setPosition(0, 11, 1)

viewLink = viz.link(robot, viz.MainView)
viewLink.preEuler([0, 45, 0])
viewLink.preTrans([0, 0, -3])
viewLink.preEuler([0, -20, 0])
# viewLink.preEuler([0, 90, 0])


def onKeyDown(key):
    if key == "q":
        changeCamera()
        # print("Camera changed")
        # print(viz.MainView)
        # print(viewLink)


def changeCamera():
    global camMode
    if camMode == "robot":
        viewLink = viz.link(downCam, viz.MainView)
        viewLink.preEuler([0, 90, 0])
        camMode = "downCam"
    else:
        viewLink = viz.link(robot, viz.MainView)
        viewLink.preEuler([0, 45, 0])
        viewLink.preTrans([0, 0, -3])
        viewLink.preEuler([0, -20, 0])
        camMode = "robot"


robotLink = viz.link(navigator, robot)
robotLink.postTrans([0, -1, 1])

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
