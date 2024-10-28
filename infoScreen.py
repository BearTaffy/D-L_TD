import viz
import vizhtml
import viztask



# Display the title screen with an image and text
def TitleScreenTask():
    html = """
    <html>
    <head>
        <style>
            html {
                margin: 0;
                padding: 0;
                width: 50px;
                height: 943px;
                overflow: hidden;
                position: relative;
            }
    
            .container {
                position: absolute;
                top: 0;
                left: 0;
                width: 50px;
                height: 943px;
                align-items: center;
                flex-direction: column;
                background: url('img/title.png') no-repeat center center fixed;
                background-size: cover;
            }
            h1 {
                font-size: 8vw;
                color: white;
                margin-bottom: 2vh;
            }
            img {
                width: 50px;
                height: 943px;
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
