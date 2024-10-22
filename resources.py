import viz
import vizact
import vizproximity

from towers import robot


wood_count = 0
stone_count = 0
collecting_wood = False
collecting_stone = False

wood_text = viz.addText(f"Wood: {wood_count}", pos=[0.1, 0.9, 0], parent=viz.SCREEN)
wood_text.fontSize(20)
wood_text.color(viz.WHITE)

stone_text = viz.addText(f"Stone: {stone_count}", pos=[0.1, 0.85, 0], parent=viz.SCREEN)
stone_text.fontSize(20)
stone_text.color(viz.WHITE)

tree = viz.add("models/environment/tree.obj")
tree.setPosition(-8.4, -1, -7.7)
tree.setScale([0.5, 0.5, 0.5])

stone = viz.add("models/environment/rock_formation.obj")
stone.setPosition(-8.87, -0.8, 7.08)
stone.setScale([0.5, 0.5, 0.5])

resource_update_callback = None

def set_resource_update_callback(callback):
    global resource_update_callback
    resource_update_callback = callback

def update_resources():
    wood_text.message(f"Wood: {wood_count}")
    stone_text.message(f"Stone: {stone_count}")
    if resource_update_callback:
        resource_update_callback()  

# Proximity manager setup
manager = vizproximity.Manager()
manager.setDebug(True)
manager.addTarget(vizproximity.Target(robot))
wood_timer = None
stone_timer = None





def add_wood():
    global wood_count, collecting_wood, stone_count, collecting_stone
    if collecting_wood:
        wood_count += 1
        update_resources()
    if collecting_stone:
        stone_count += 1
        update_resources()


def start_collecting_wood():
    # This will call add_wood every 2 seconds as long as collecting_wood is True
    def wood_timer():
        if collecting_wood:
            add_wood()

    def stone_timer():
        if collecting_stone:
            add_wood()

    vizact.ontimer(2, wood_timer)
    vizact.ontimer(3, stone_timer)


# Enter sensor function
def onEnterSensor(e):
    global collecting_wood, collecting_stone
    if e.sensor.name == "Circle":
        # viz.logNotice("Entered wood collection area")
        collecting_wood = True
        start_collecting_wood()  # Start the repeating timer when entering the area
    if e.sensor.name == "Circle2":
        # viz.logNotice("Entered stone collection area")
        collecting_stone = True
        start_collecting_wood()  # Start the repeating timer when entering the area


# Exit sensor function
def onExitSensor(e):
    global collecting_wood, wood_timer, collecting_stone, stone_timer
    if e.sensor.name == "Circle":
        # viz.logNotice("Left wood collection area")
        collecting_wood = False
        if wood_timer:
            wood_timer.remove()
            wood_timer = None
    if e.sensor.name == "Circle2":
        # viz.logNotice("Left stone collection area")
        collecting_stone = False
        if stone_timer:
            stone_timer.remove()
            stone_timer = None


def AddSensor(shape, name):
    sensor = vizproximity.Sensor(shape, None)
    sensor.name = name
    manager.addSensor(sensor)


# Add circular sensor around the tree
shape = vizproximity.CircleArea(3, center=[-8.21, -7.7])
AddSensor(shape, "Circle")

shape = vizproximity.CircleArea(3, center=[-8.87, 7.08])
AddSensor(shape, "Circle2")
