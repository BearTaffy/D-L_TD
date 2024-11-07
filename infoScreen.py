import viz
import viztask
import vizact
import towers
import resources

from waves import wave_manager, base_health
from creeps import creeps
from resources import wood_text, stone_text

# Global variables to hold references to screen elements for easier removal
screen_elements = []
game_started = False


def clearScreen():
    """Clear all elements on the screen."""
    global screen_elements
    for element in screen_elements:
        element.remove()
    screen_elements = []


def howToPlay():
    viztask.schedule(displayHowToPlayScreen())


def displayHowToPlayScreen():
    yield
    clearScreen()

    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)
    overlayPanel.setScale(13, 11, 1)
    screen_elements.append(overlayPanel)

    try:
        bgTexture = viz.addTexture("img/title.png")
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("Background texture 'img/title.png' not found, using solid color")

    # Add a plane behind the text for better readability
    backgroundPlane = viz.addTexQuad(parent=viz.SCREEN)
    backgroundPlane.setPosition(0.5, 0.5, 4)
    backgroundPlane.setScale(7, 5.5, 1)
    backgroundPlane.color(viz.BLACK)  # Set to black for contrast
    backgroundPlane.alpha(0.5)  # Make it semi-transparent
    screen_elements.append(backgroundPlane)

    howToPlayTitle = viz.addText("How to Play", parent=viz.SCREEN)
    howToPlayTitle.alignment(viz.ALIGN_CENTER_TOP)
    howToPlayTitle.fontSize(50)
    howToPlayTitle.color(viz.WHITE)
    howToPlayTitle.setPosition(0.5, 0.9, 0)
    screen_elements.append(howToPlayTitle)

    rulesText = viz.addText(
        "Rules and Controls:\n1. Use WASD to move.\n2. Defend your base from enemies.\n3. Collect wood and stone by standing by the tree and rocks.\n4. Press Q to go into top-down view to place towers.\n5. Select towers by pressing 1, 2, or 3.\n6. Press X to remove towers.\n7. Press U to toggle upgrade mode.",
        parent=viz.SCREEN,
    )
    rulesText.alignment(viz.ALIGN_CENTER_CENTER)
    rulesText.fontSize(24)
    rulesText.color(viz.WHITE)
    rulesText.setPosition(0.5, 0.6, 0)
    screen_elements.append(rulesText)

    # Create a back button using viz.addButton (VizCheckBox) and add a label
    backButton = viz.addButton()
    backButton.setPosition(0.5, 0.3, 0)
    backButton.setScale(4, 2)  # Adjust scale for a better fit
    screen_elements.append(backButton)

    backButtonLabel = viz.addText("Back", parent=viz.SCREEN)
    backButtonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    backButtonLabel.setPosition(0.5, 0.3, 0)
    backButtonLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(backButtonLabel)

    # Use vizact.onbuttondown to assign the onBackButton function
    vizact.onbuttondown(backButton, onBackButton)


def onBackButton():
    viztask.schedule(displayTitleScreen())


def displayTitleScreen():
    yield
    clearScreen()

    viz.MainWindow.clearcolor(viz.BLACK)

    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)
    overlayPanel.setScale(13, 11, 1)
    screen_elements.append(overlayPanel)

    try:
        bgTexture = viz.addTexture("img/title.png")
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("Background texture 'img/title.png' not found, using solid color")

    titleText = viz.addText("Tower Defense", parent=viz.SCREEN)
    titleText.alignment(viz.ALIGN_CENTER_TOP)
    titleText.fontSize(60)
    titleText.color(viz.WHITE)
    titleText.setPosition(0.5, 0.85, 0)
    screen_elements.append(titleText)

    # Create Start Game button with a label
    startButton = viz.addButton()
    startButton.setPosition(0.5, 0.55, 0)
    startButton.setScale(4, 2)  # Adjust scale for a better fit
    screen_elements.append(startButton)

    startButtonLabel = viz.addText("Start Game", parent=viz.SCREEN)
    startButtonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    startButtonLabel.setPosition(0.5, 0.55, 0)
    startButtonLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(startButtonLabel)

    # Create How to Play button with a label
    howToPlayButton = viz.addButton()
    howToPlayButton.setPosition(0.5, 0.4, 0)
    howToPlayButton.setScale(4, 2)  # Adjust scale for a better fit
    screen_elements.append(howToPlayButton)

    howToPlayButtonLabel = viz.addText("How to Play", parent=viz.SCREEN)
    howToPlayButtonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    howToPlayButtonLabel.setPosition(0.5, 0.4, 0)
    howToPlayButtonLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(howToPlayButtonLabel)

    # Use vizact.onbuttondown to assign the functions
    vizact.onbuttondown(startButton, onStartButton)
    vizact.onbuttondown(howToPlayButton, onHowToPlayButton)


def startGame():
    clearScreen()
    viz.MainWindow.clearcolor(viz.SKYBLUE)
    viz.logNotice("Game is starting...")
    wood_text.visible(viz.ON)
    stone_text.visible(viz.ON)
    wave_manager.initializeGame()
    base_health.reset()
    resetGameState()


def onStartButton():
    startGame()


def onHowToPlayButton():
    howToPlay()


# Game Over/Reset
def resetGameState():

    resources.wood_count = 15
    resources.stone_count = 12
    resources.update_resources()

    for towersPlace in towers.towersPlaces:
        if towersPlace["isPlaced"]:
            if towersPlace["tower"]:
                towersPlace["tower"].remove()
                towersPlace["tower"] = None
            towersPlace["isPlaced"] = False


def gameOver():
    for creep in creeps[:]:
        creep.remove()
    creeps.clear()
    viztask.schedule(displayGameOverScreen())


def displayGameOverScreen():
    yield
    clearScreen()

    viz.MainWindow.clearcolor(viz.BLACK)

    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)
    overlayPanel.setScale(13, 11, 1)
    screen_elements.append(overlayPanel)

    try:
        bgTexture = viz.addTexture("img/game over.jpg")
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("'img/game over.jpg' not found????????")

    # Add a black background plane behind the score text
    backgroundPlane = viz.addTexQuad(parent=viz.SCREEN)
    backgroundPlane.setPosition(0.5, 0.5, 4)
    backgroundPlane.setScale(5, 2, 1)  # Adjusted to be smaller
    backgroundPlane.color(viz.BLACK)  # Black color for contrast
    backgroundPlane.alpha(0.5)  # Semi-transparent for readability
    screen_elements.append(backgroundPlane)

    scoreText = viz.addText(
        f"You survived {wave_manager.currentWave - 1} waves!", parent=viz.SCREEN
    )
    scoreText.alignment(viz.ALIGN_CENTER_CENTER)
    scoreText.fontSize(40)
    scoreText.color(viz.WHITE)
    scoreText.setPosition(0.5, 0.5, 0)
    screen_elements.append(scoreText)

    playAgainButton = viz.addButton()
    playAgainButton.setPosition(0.5, 0.3, 0)
    playAgainButton.setScale(4, 2)
    screen_elements.append(playAgainButton)

    playAgainLabel = viz.addText("Play Again", parent=viz.SCREEN)
    playAgainLabel.alignment(viz.ALIGN_CENTER_CENTER)
    playAgainLabel.setPosition(0.5, 0.3, 0)
    playAgainLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(playAgainLabel)

    vizact.onbuttondown(playAgainButton, startGame)


viztask.schedule(displayTitleScreen())
