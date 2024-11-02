import viz
import viztask
import vizact
import vizshape

def startGame():
    # Remove the overlay when starting the game
    if 'overlayPanel' in globals():
        overlayPanel.remove()
    viz.MainWindow.clearcolor(viz.SKYBLUE)  # Restore the original environment color
    viz.logNotice('Game is starting...')
    # Add your game-starting code here

def howToPlay():
    viztask.schedule(displayHowToPlayScreen())

def displayHowToPlayScreen():
    yield  # Make it a generator function for viztask compatibility

    # Clear screen and set up a new color for How-to-Play screen
    viz.MainWindow.clearcolor(viz.DARKGRAY)

    # Title for How-to-Play screen
    howToPlayTitle = viz.addText('How to Play', parent=viz.SCREEN)
    howToPlayTitle.alignment(viz.ALIGN_CENTER_TOP)
    howToPlayTitle.fontSize(50)
    howToPlayTitle.color(viz.WHITE)
    howToPlayTitle.setPosition(0.5, 0.9, 0)

    # Rules and controls description
    rulesText = viz.addText('Rules and Controls:\n1. Use WASD to move.\n2. Press SPACE to shoot.\n3. Defend your base from enemies.', parent=viz.SCREEN)
    rulesText.alignment(viz.ALIGN_CENTER_CENTER)
    rulesText.fontSize(24)
    rulesText.color(viz.WHITE)
    rulesText.setPosition(0.5, 0.6, 0)

    # Add a Back button to return to the title screen
    backButton, backButtonLabel = createButton('Back', [0.5, 0.3, 0], fontSize=24, scale=[0.3, 0.1, 1])

    # Define Back button callback
    def onBackButton():
        howToPlayTitle.remove()
        rulesText.remove()
        backButton.remove()
        backButtonLabel.remove()
        viztask.schedule(displayTitleScreen())

    # Attach callback to Back button
    vizact.onbuttondown(backButton, onBackButton)

def displayTitleScreen():
    yield  # Make it a generator function for viztask compatibility

    # Set the window clear color for a consistent background
    viz.MainWindow.clearcolor(viz.BLACK)

    # Create a full-screen overlay panel to cover the entire view
    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)  # Center the quad on the screen
    overlayPanel.setScale(13, 11, 1)  # Scale to cover the entire screen

    # Apply the background texture from img/title.png
    try:
        bgTexture = viz.addTexture('img/title.png')
        overlayPanel.texture(bgTexture)
    except:
        viz.logNotice("Background texture 'img/title.png' not found, using solid color")

    # Display title text at the top
    titleText = viz.addText('Tower Defense', parent=viz.SCREEN)
    titleText.alignment(viz.ALIGN_CENTER_TOP)
    titleText.fontSize(60)
    titleText.color(viz.WHITE)
    titleText.setPosition(0.5, 0.85, 0)

    # Create Start Game button in the center
    startButton, startButtonLabel = createButton('Start Game', [0.5, 0.55, 0], fontSize=30, scale=[2, 1, 0.8])

    # Create How to Play button below Start Game button
    howToPlayButton, howToPlayButtonLabel = createButton('How to Play', [0.5, 0.4, 0], fontSize=30, scale=[2, 1, 0.8])

    # Define button callbacks
    def onStartButton():
        titleText.remove()
        startButton.remove()
        startButtonLabel.remove()
        howToPlayButton.remove()
        howToPlayButtonLabel.remove()
        if 'overlayPanel' in globals():
            overlayPanel.remove()
        startGame()

    def onHowToPlayButton():
        titleText.remove()
        startButton.remove()
        startButtonLabel.remove()
        howToPlayButton.remove()
        howToPlayButtonLabel.remove()
        if 'overlayPanel' in globals():
            overlayPanel.remove()
        howToPlay()

    # Attach callbacks to buttons
    vizact.onbuttondown(startButton, onStartButton)
    vizact.onbuttondown(howToPlayButton, onHowToPlayButton)

# Function to create a button with a more appealing look
def createButton(text, position, fontSize=24, scale=[0.3, 0.1, 1]):
    buttonQuad = viz.addTexQuad(parent=viz.SCREEN)
    buttonQuad.color(viz.SKYBLUE)  # Set button color
    buttonQuad.setPosition(position)
    buttonQuad.setScale(scale)  # Set button size

    buttonLabel = viz.addText(text, parent=viz.SCREEN)
    buttonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    buttonLabel.fontSize(fontSize)
    buttonLabel.color(viz.BLACK)
    buttonLabel.setPosition(position)

    return buttonQuad, buttonLabel

# Schedule the title screen to display
viztask.schedule(displayTitleScreen())
