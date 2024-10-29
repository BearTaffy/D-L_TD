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
                height: 100vh;
                overflow: hidden;
            }
            
            h1 {
                font-size: 50px;
                color: #ffffff;
                text-align: center;
                background-color: rgba(0, 0, 0, 0.5); /* Optional background for text readability */
                padding: 1vh 2vw;
                border-radius: 10px;
                margin-top: 15%;
                margin-left: 7%;
            }
        </style>
    </head>
    <body>
        <h1>Tower Defense</h1>
        <button>test</button>
    </body>
    </html>
    """

    # Display the title screen
    vizhtml.displayCode(html)

    # Wait for "Start Game" button to be pressed
    yield viztask.waitEvent('startGame')

    # Proceed to main game
    viz.logNotice('Game is starting...')

# Schedule the task to run
viztask.schedule(TitleScreenTask())
