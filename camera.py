import viz
import vizshape
import vizcam

camMode = "robot"

robot = viz.add("models/robot.obj")
robot.setPosition([-1, -1, 2])
robot.setScale([0.1, 0.1, 0.1])
robot.setEuler([0, 0, 0])
robot.alpha(1)

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
