import viz
import vizshape
import vizcam

camMode = "robot"

robot = viz.add("models/robot.obj")
robot.setPosition([-1, -1, 2])
robot.setScale([0.1, 0.1, 0.1])
robot.setEuler([0, 0, 0])
robot.alpha(0)

navigator = vizcam.addWalkNavigate(moveScale=2.0)
viz.cam.setHandler(navigator)
viz.MainView.collision(viz.OFF)


viewLink = viz.link(robot, viz.MainView)
viewLink.preEuler([0, 45, 0])
viewLink.preTrans([0, 0, -3])
viewLink.preEuler([0, -20, 0])

robotLink = viz.link(navigator, robot)
robotLink.postTrans([0, -1, 1])

downCam = vizshape.addSphere(radius=0.1)
downCam.alpha(0)
downCam.setPosition(0, 11, 1)


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
