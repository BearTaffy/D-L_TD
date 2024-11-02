import viz
import viztask

def startGame():
    if 'overlayPanel' in globals():
        overlayPanel.remove()
    viz.MainWindow.clearcolor(viz.SKYBLUE)
    viz.logNotice('Game is starting...')

def howToPlay():
    viztask.schedule(displayHowToPlayScreen())

def displayHowToPlayScreen():
    yield

    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)
    overlayPanel.setScale(13, 11, 1)

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

    rulesText = viz.addText('Rules and Controls:\n1. Use WASD to move.\n2. Press SPACE to shoot.\n3. Defend your base from enemies.', parent=viz.SCREEN)
    rulesText.alignment(viz.ALIGN_CENTER_CENTER)
    rulesText.fontSize(24)
    rulesText.color(viz.WHITE)
    rulesText.setPosition(0.5, 0.6, 0)

    backButton, backButtonLabel = createButton('Back', [0.5, 0.3, 0], fontSize=24, scale=[0.3, 0.1, 1])

    def onBackButton():
        howToPlayTitle.remove()
        rulesText.remove()
        backButton.remove()
        backButtonLabel.remove()
        if 'overlayPanel' in globals():
            overlayPanel.remove()
        viztask.schedule(displayTitleScreen())

    registerButtonClick(backButton, onBackButton)

def displayTitleScreen():
    yield

    viz.MainWindow.clearcolor(viz.BLACK)

    global overlayPanel
    overlayPanel = viz.addTexQuad(parent=viz.SCREEN)
    overlayPanel.setPosition(0.5, 0.5, 0)
    overlayPanel.setScale(13, 11, 1)

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

    startButton, startButtonLabel = createButton('Start Game', [0.5, 0.55, 0], fontSize=30, scale=[2, 1, 0.8])
    howToPlayButton, howToPlayButtonLabel = createButton('How to Play', [0.5, 0.4, 0], fontSize=30, scale=[2, 1, 0.8])

    # Define button callbacks separately
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

    # Register the individual button clicks with their callbacks
    registerButtonClick(startButton, onStartButton)
    registerButtonClick(howToPlayButton, onHowToPlayButton)

def createButton(text, position, fontSize=24, scale=[0.3, 0.1, 1]):
    buttonQuad = viz.addTexQuad(parent=viz.SCREEN)
    buttonQuad.color(viz.SKYBLUE)
    buttonQuad.setPosition(position)
    buttonQuad.setScale(scale)

    buttonLabel = viz.addText(text, parent=viz.SCREEN)
    buttonLabel.alignment(viz.ALIGN_CENTER_CENTER)
    buttonLabel.fontSize(fontSize)
    buttonLabel.color(viz.BLACK)
    buttonLabel.setPosition(position)

    return buttonQuad, buttonLabel

def registerButtonClick(button, callback):
    def onClick(e):
        pos = button.getPosition(mode=viz.SCREEN)
        scale = button.getScale()

        minX, maxX = pos[0] - scale[0] / 2, pos[0] + scale[0] / 2
        minY, maxY = pos[1] - scale[1] / 2, pos[1] + scale[1] / 2

        mousePos = viz.mouse.getPosition()

        if minX <= mousePos[0] <= maxX and minY <= mousePos[1] <= maxY:
            callback()

    viz.callback(viz.MOUSEDOWN_EVENT, onClick)

# Schedule the title screen to display
viztask.schedule(displayTitleScreen())
