import viz
import viztask
import vizact

# Global variables to hold references to screen elements for easier removal
screen_elements = []
game_started=False

def clearScreen():
    """Clear all elements on the screen."""
    global screen_elements
    for element in screen_elements:
        element.remove()
    screen_elements = []

def startGame():
    global game_started
    clearScreen()
    viz.MainWindow.clearcolor(viz.SKYBLUE)
    viz.logNotice('Game is starting...')
    game_started=True
    return game_started

gameIsStart = startGame()
    

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
        bgTexture = viz.addTexture('img/title.png')
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("Background texture 'img/title.png' not found, using solid color")

    howToPlayTitle = viz.addText('How to Play', parent=viz.SCREEN)
    howToPlayTitle.alignment(viz.ALIGN_CENTER_TOP)
    howToPlayTitle.fontSize(50)
    howToPlayTitle.color(viz.WHITE)
    howToPlayTitle.setPosition(0.5, 0.9, 0)
    screen_elements.append(howToPlayTitle)

    rulesText = viz.addText('Rules and Controls:\n1. Use WASD to move.\n2. Press SPACE to shoot.\n3. Defend your base from enemies.', parent=viz.SCREEN)
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

    backButtonLabel = viz.addText('Back', parent=viz.SCREEN)
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
        bgTexture = viz.addTexture('img/title.png')
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("Background texture 'img/title.png' not found, using solid color")

    titleText = viz.addText('Tower Defense', parent=viz.SCREEN)
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

    startButtonLabel = viz.addText('Start Game', parent=viz.SCREEN)
    startButtonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    startButtonLabel.setPosition(0.5, 0.55, 0)
    startButtonLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(startButtonLabel)

    # Create How to Play button with a label
    howToPlayButton = viz.addButton()
    howToPlayButton.setPosition(0.5, 0.4, 0)
    howToPlayButton.setScale(4, 2)  # Adjust scale for a better fit
    screen_elements.append(howToPlayButton)

    howToPlayButtonLabel = viz.addText('How to Play', parent=viz.SCREEN)
    howToPlayButtonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    howToPlayButtonLabel.setPosition(0.5, 0.4, 0)
    howToPlayButtonLabel.setScale(0.2, 0.2, 0)
    screen_elements.append(howToPlayButtonLabel)

    # Use vizact.onbuttondown to assign the functions
    vizact.onbuttondown(startButton, onStartButton)
    vizact.onbuttondown(howToPlayButton, onHowToPlayButton)

def onStartButton():
    startGame()

def onHowToPlayButton():
    howToPlay()

# Schedule the title screen to display
viztask.schedule(displayTitleScreen())