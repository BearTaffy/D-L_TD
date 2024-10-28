import viz
import vizhtml
import viztask

viz.fov(60)
viz.go()

# Display the title screen with an image and text
def TitleScreenTask():
    html = """
    <html>
    <head>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                position: relative;
            }
            .container {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                background: #000;
                flex-direction: column;
            }
            h1 {
                font-size: 8vw;
                color: white;
                margin-bottom: 2vh;
            }
            img {
                width: 80%;
                height: auto;
                max-width: 1000px;
                max-height: 60vh;
            }
            button {
                font-size: 4vw;
                padding: 1vw 2vw;
                margin-top: 2vh;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Tower Defense</h1>
            <img src="img/title.png" alt="Tower Defense">
            <button onclick="window.location.href='javascript:parent.viz.sendEvent(\\'startGame\\')'">Start Game</button>
        </div>
    </body>
    </html>
    """

    # Display the title screen
    vizhtml.displayCode(html)

    # Wait for "Start Game" button to be pressed
    yield viztask.waitEvent('startGame')

    # Proceed to main game
    viz.logNotice('Game is starting...')

# viztask.schedule(TitleScreenTask())
