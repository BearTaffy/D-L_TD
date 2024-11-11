import viz
import vizact
import vizproximity

from towers import robot


wood_count = 15
stone_count = 12
collecting_wood = False
collecting_stone = False
tower_icons = []

# Proximity manager setup
manager = vizproximity.Manager()
manager.setDebug(True)
manager.addTarget(vizproximity.Target(robot))
wood_timer = None
stone_timer = None

wood_text = viz.addText(f"Wood: {wood_count}", pos=[0.03, 0.95, 0], parent=viz.SCREEN)
wood_text.fontSize(20)
wood_text.color(viz.WHITE)
wood_text.visible(viz.OFF)

stone_text = viz.addText(f"Stone: {stone_count}", pos=[0.03, 0.90, 0], parent=viz.SCREEN)
stone_text.fontSize(20)
stone_text.color(viz.WHITE)
stone_text.visible(viz.OFF)

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
    updateTowerIcons()  # Update icon colors based on current resources


def add_wood():
    global wood_count, collecting_wood, stone_count, collecting_stone
    if collecting_wood:
        wood_count += 1
        update_resources()
    if collecting_stone:
        stone_count += 1
        update_resources()


def start_collecting_wood():
    global wood_timer, stone_timer

    # Clear any existing timers to avoid duplication
    if wood_timer:
        wood_timer.remove()
        wood_timer = None

    if stone_timer:
        stone_timer.remove()
        stone_timer = None

    # Define a function for repeated collection
    def wood_collection_timer():
        if collecting_wood:
            add_wood()  # Add wood every 2 seconds if in the area

    def stone_collection_timer():
        if collecting_stone:
            add_wood()  # Add stone every 3 seconds if in the area

    # Set new timers
    wood_timer = vizact.ontimer(1, wood_collection_timer)
    stone_timer = vizact.ontimer(1.5, stone_collection_timer)

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
    sensor = vizproximity.Sensor(shape, None)
    sensor.name = name
    manager.addSensor(sensor)


def check_resources():
    required_wood = 5
    required_stone = 3
    return wood_count >= required_wood and stone_count >= required_stone


def createTowerIcons():
    global tower_icons

    # Import towerCosts here to avoid circular import at the top
    from towers import towerCosts

    # Define the icons and their positions
    icon_paths = ["img/archer_tower.png", "img/cannon.png", "img/wizard_tower.png"]
    tower_types = ["archer", "cannon", "wizard"]

    # Clear existing icons if they are present
    if tower_icons:
        for icon in tower_icons:
            icon.remove()
        tower_icons.clear()

    # Add the icons and cost labels to the top-right of the screen
    for i, (icon_path, tower_type) in enumerate(zip(icon_paths, tower_types)):
        # Add the tower icon
        icon = viz.addTexture(icon_path)
        sprite = viz.addTexQuad(texture=icon, parent=viz.SCREEN)
        sprite.setPosition([0.95, 0.955 - i * 0.1, 0])  # Adjust position as needed
        sprite.setScale([0.5, 0.5, 0.5])  # Ensure all icons are the same size
        sprite.color(
            viz.RED if not check_resources() else viz.GREEN
        )  # Set initial color based on resources
        sprite.alpha(
            0.5
        )  # Set opacity to 50% (0.0 = fully transparent, 1.0 = fully opaque)
        tower_icons.append(sprite)

        # Add the cost label next to the icon
        costs = towerCosts[tower_type]
        cost_text = f"Wood: {costs['wood']} Stone: {costs['stone']}"
        cost_label = viz.addText(cost_text, parent=viz.SCREEN)
        cost_label.setPosition([0.82, 0.95 - i * 0.1, 0])  # Position next to the icon
        cost_label.fontSize(15)
        cost_label.color(viz.WHITE)
        tower_icons.append(cost_label)


def updateTowerIcons():
    from towers import towerCosts  # Import towerCosts here to get individual costs
    
    # Loop over icons and cost labels in pairs (icon and label for each tower)
    for i in range(0, len(tower_icons), 2):
        icon = tower_icons[i]
        label = tower_icons[i + 1]  # Get the associated label
        tower_type = ["archer", "cannon", "wizard"][i // 2]
        costs = towerCosts[tower_type]
        
        # Check if the player has enough resources for this tower type
        has_resources = wood_count >= costs['wood'] and stone_count >= costs['stone']
        
        if has_resources:
            icon.color(viz.GREEN)  # Make icon green if resources are sufficient
            label.color(viz.GREEN)  # Make label green to match icon
            icon.alpha(1.0)  # Fully opaque
        else:
            icon.color(viz.RED)  # Make icon red if resources are insufficient
            label.color(viz.RED)  # Make label red to match icon
            icon.alpha(0.5)  # Semi-transparent


# Add circular sensor around the tree
shape = vizproximity.CircleArea(3, center=[-8.21, -7.7])
AddSensor(shape, "Circle")

shape = vizproximity.CircleArea(3, center=[-8.87, 7.08])
AddSensor(shape, "Circle2")
