from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket + Selenium</title>
    </head>
    <body>
        <h1>WebSocket + Selenium</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
            driver = webdriver.Chrome(options=chrome_options)

            driver.get("https://www.google.com")
            await websocket.send_text(f"Opened Google: {driver.title}")

            driver.quit()
            await websocket.send_text(f"Received message: {data}")
    except WebSocketDisconnect:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)