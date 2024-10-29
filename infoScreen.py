import viz
import vizhtml
import viztask

# Display the title screen with an image and text
def TitleScreenTask():
    html = """
    <html>
    <head>
        <style>
            body {
                background: url('img/title.png') no-repeat center center;
                background-size: cover;
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                height: 100vh;
                overflow: hidden;
            }
            
            h1 {
                font-size: 50px;
                color: #ffffff;
                text-align: center;
                padding: 1vh 2vw;
                border-radius: 10px;
                margin-top: 15%;
                margin-left: 7%;
                text-shadow: 2px 2px 4px #000000;
            }

            button {
                font-size: 30px;
                padding: 10px 20px;
                color: #ffffff;
                background-color: #9d99a3;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                text-shadow: 1px 1px 3px #000000;
                margin-left:42%;
                margin-top: 3%;
            }

            
        </style>
    </head>
    <body>
        <h1>Tower Defense</h1>
        <button onclick="window.location.href='javascript:parent.viz.sendEvent(\\'startGame\\')'">Start Game</button>
        <button onclick="window.location.href='javascript:parent.viz.sendEvent(\\'howToPlay\\')'">How to play</button>
    </body>
    </html>
    """

    # Display the title screen
    vizhtml.displayCode(html)

    # Wait for either "Start Game" or "How to play" event
    while True:
        event = yield viztask.waitAny([viztask.waitEvent('startGame'), viztask.waitEvent('howToPlay')])
        
        if event.condition == 'startGame':
            viz.logNotice('Game is starting...')
            break
        elif event.condition == 'howToPlay':
            yield howToPlayTask()  # Call howToPlayTask when 'How to play' is clicked

    # Proceed to main game
    viz.logNotice('Game is starting...')


def howToPlayTask():
    html = """
    <html>
    <head>
        <style>
            body {
                background: url('img/title.png') no-repeat center center;
                background-size: cover;
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                height: 100vh;
                overflow: hidden;
            }
            
            h1 {
                font-size: 50px;
                color: #ffffff;
                text-align: center;
                padding: 1vh 2vw;
                border-radius: 10px;
                margin-top: 15%;
                margin-left: 7%;
                text-shadow: 2px 2px 4px #000000;
            }

            button {
                font-size: 30px;
                padding: 10px 20px;
                color: #ffffff;
                background-color: #9d99a3;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                text-shadow: 1px 1px 3px #000000;
                margin-left:42%;
                margin-top: 3%;
            }

            
        </style>
    </head>
    <body>
        <h1>How to play</h1>
    </body>
    </html>
    """

    # Display the title screen
    vizhtml.displayCode(html)

    # Proceed to main game
    viz.logNotice('Game is starting...')


# Schedule the task to run
viztask.schedule(TitleScreenTask())
