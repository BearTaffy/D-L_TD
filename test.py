import viz
import vizshape
import vizmat
import vizact

from creeps import creeps
from camera import changeCamera, downCam, robot, camMode
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

towersPlaces = []
currentObject = None
camMode = "robot"
removalMode = False

# ... [previous tower coordinates and other code remains the same] ...

class Tower:
    def __init__(self, model, scale, projectileClass, towerType):
        self.model = viz.add(model)
        self.model.setScale(scale)
        self.projectileClass = projectileClass
        self.towerType = towerType
        self.attackRange = 5
        self.attackCooldown = 1.0
        self.lastAttackTime = 0
        self.highlighted = False

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
            self.model.emissive([1,0,0,1])  # Red highlight for removal
            self.highlighted = True
        else:
            self.model.emissive([0,0,0,1])  # Remove highlight
            self.highlighted = False

    # ... [rest of Tower class methods remain the same] ...

def refundResources(towerType):
    """Refund a portion of the resources when removing a tower"""
    costs = towerCosts[towerType]
    refund_ratio = 0.75  # Refund 75% of the original cost
    
    resources.wood_count += int(costs["wood"] * refund_ratio)
    resources.stone_count += int(costs["stone"] * refund_ratio)
    resources.update_resources()

def removeTower(towersPlace):
    """Remove a tower and refund resources"""
    if towersPlace["tower"]:
        refundResources(towersPlace["tower"].towerType)
        towersPlace["tower"].remove()
        towersPlace["tower"] = None
        towersPlace["isPlaced"] = False

def toggleRemovalMode():
    """Toggle tower removal mode on/off"""
    global removalMode
    removalMode = not removalMode
    
    # Highlight/unhighlight all placed towers
    for towersPlace in towersPlaces:
        if towersPlace["tower"]:
            towersPlace["tower"].highlight(removalMode)

def onMouseDown(button):
    global currentObject, removalMode
    if button == viz.MOUSEBUTTON_LEFT:
        if removalMode:
            # Handle tower removal
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
            # Original placement logic
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

def onKeyDown(key):
    global currentObject, camMode, removalMode
    if key == "q":
        if removalMode:
            toggleRemovalMode()  # Turn off removal mode when switching camera
        changeCamera()
    elif key == " ":
        print(robot.getPosition())
    elif key == "x":
        if camMode == "downCam":
            toggleRemovalMode()
    elif camMode == "downCam" and not removalMode:  # Only allow tower placement when not in removal mode
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