import viz
import vizact

from towers import updateObjectPosition, onMouseDown, onKeyDown
from resources import onEnterSensor, onExitSensor, manager
from creeps import spawnCreep, updateCreeps
from waves import updateWaveSystem

# Environment
mapp = viz.add("models/environment/map.obj")
mapp.setPosition(0, -1, 0)

day = viz.add("sky_day.osgb")
day.renderToBackground()

portal = viz.add("models/environment/portal.obj")
portal.setPosition(19, -0.8, 0.5)
portal.setScale([0.5, 0.5, 0.5])

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

# Function calls
manager.onEnter(None, onEnterSensor)
manager.onExit(None, onExitSensor)
viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
viz.callback(viz.MOUSEDOWN_EVENT, onMouseDown)
vizact.onupdate(viz.PRIORITY_INPUT, updateObjectPosition)   
# vizact.ontimer(5, spawnCreep)
vizact.onupdate(0, updateCreeps)
vizact.onupdate(0, updateWaveSystem)

if __name__ == "__main__":
    viz.go()
