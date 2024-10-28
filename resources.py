import viz
import vizact
import vizproximity
import vizshape

from towers import robot

wood_count = 0
stone_count = 0
collecting_wood = False
collecting_stone = False
tower_icons = []

# Proximity manager setup
manager = vizproximity.Manager()
manager.setDebug(True)
manager.addTarget(vizproximity.Target(robot))
wood_timer = None
stone_timer = None

# Text displays for resources
wood_text = viz.addText(f"Wood: {wood_count}", pos=[0.1, 0.9, 0], parent=viz.SCREEN)
wood_text.fontSize(20)
wood_text.color(viz.WHITE)

stone_text = viz.addText(f"Stone: {stone_count}", pos=[0.1, 0.85, 0], parent=viz.SCREEN)
stone_text.fontSize(20)
stone_text.color(viz.WHITE)

# Environmental elements for resource collection
tree = viz.add("models/environment/tree.obj")
tree.setPosition(-8.4, -1, -7.7)
tree.setScale([0.5, 0.5, 0.5])

stone = viz.add("models/environment/rock_formation.obj")
stone.setPosition(-8.87, -0.8, 7.08)
stone.setScale([0.5, 0.5, 0.5])

# Resource update callback and tower costs variable
resource_update_callback = None
callback_tower_costs = None  # Store tower_costs for callback

def set_resource_update_callback(callback, tower_costs):
    """Set the resource update callback and store tower_costs."""
    global resource_update_callback, callback_tower_costs
    resource_update_callback = callback
    callback_tower_costs = tower_costs

def update_resources():
    """Update displayed resource values and trigger the callback with tower costs."""
    wood_text.message(f"Wood: {wood_count}")
    stone_text.message(f"Stone: {stone_count}")
    if resource_update_callback:
        resource_update_callback(callback_tower_costs)

def add_wood():
    """Add wood and stone resources while collecting."""
    global wood_count, collecting_wood, stone_count, collecting_stone
    if collecting_wood:
        wood_count += 1
        update_resources()
    if collecting_stone:
        stone_count += 1
        update_resources()

def start_collecting_wood():
    """Start timers to add resources every few seconds while collecting."""
    def wood_timer():
        if collecting_wood:
            add_wood()

    def stone_timer():
        if collecting_stone:
            add_wood()

    vizact.ontimer(2, wood_timer)
    vizact.ontimer(3, stone_timer)

def onEnterSensor(e):
    """Begin resource collection when player enters sensor area."""
    global collecting_wood, collecting_stone
    if e.sensor.name == "Circle":
        collecting_wood = True
        start_collecting_wood()
    if e.sensor.name == "Circle2":
        collecting_stone = True
        start_collecting_wood()

def onExitSensor(e):
    """Stop resource collection when player leaves sensor area."""
    global collecting_wood, wood_timer, collecting_stone, stone_timer
    if e.sensor.name == "Circle":
        collecting_wood = False
        if wood_timer:
            wood_timer.remove()
            wood_timer = None
    if e.sensor.name == "Circle2":
        collecting_stone = False
        if stone_timer:
            stone_timer.remove()
            stone_timer = None

def AddSensor(shape, name):
    """Add a proximity sensor to the manager."""
    sensor = vizproximity.Sensor(shape, None)
    sensor.name = name
    manager.addSensor(sensor)

def check_resources(tower_type, tower_costs):
    """Check if enough resources are available for the specified tower type."""
    required_resources = tower_costs.get(tower_type, {"Wood": 0, "Stone": 0})
    return wood_count >= required_resources["Wood"] and stone_count >= required_resources["Stone"]

def get_resources():
    """Retrieve current wood and stone count."""
    global wood_count, stone_count
    return wood_count, stone_count

def set_resources(new_wood, new_stone):
    """Set new wood and stone counts and update resource display."""
    global wood_count, stone_count
    wood_count = new_wood
    stone_count = new_stone
    update_resources()

def createTowerIcons(tower_costs):
    """Create icons for towers and update colors based on available resources."""
    global tower_icons
    icon_paths = ["img/archer_tower.png", "img/cannon.png", "img/wizard_tower.png"]

    if tower_icons:
        for icon in tower_icons:
            icon.remove()
        tower_icons.clear()

    for i, icon_path in enumerate(icon_paths):
        icon = viz.addTexture(icon_path)
        sprite = viz.addTexQuad(texture=icon, parent=viz.SCREEN)
        sprite.setPosition([0.95, 0.90 - i * 0.1, 0])
        sprite.setScale([0.7, 0.7, 0.7])

        overlay = vizshape.addBox(size=[0.1, 0.1, 0.001], parent=viz.SCREEN)
        overlay.setPosition([0.95, 0.90 - i * 0.1, 0.01])
        overlay.setScale([0.7, 0.7, 0.7])

        tower_type = ["Archer-tower", "Cannon", "Wizard-tower"][i]
        overlay.color(viz.GREEN if check_resources(tower_type, tower_costs) else viz.RED)
        overlay.alpha(0.5)

        tower_icons.extend([overlay, sprite])

def updateTowerIcons(tower_costs):
    """Update icon colors based on current resources."""
    for i, overlay in enumerate(tower_icons[::2]):
        tower_type = ["Archer-tower", "Cannon", "Wizard-tower"][i]
        overlay.color(viz.GREEN if check_resources(tower_type, tower_costs) else viz.RED)
        overlay.alpha(0.5)

# Define and add sensors for resource collection areas
shape = vizproximity.CircleArea(3, center=[-8.21, -7.7])
AddSensor(shape, "Circle")

shape = vizproximity.CircleArea(3, center=[-8.87, 7.08])
AddSensor(shape, "Circle2")
