from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn


app = FastAPI()

html = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }
        .chat-container {
            width: 400px;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>Chat</h1>
        <textarea id="messageInput" placeholder="Write your message..."></textarea>
        <button id="sendButton">Send</button>
    </div>

    <script>
        const socket = new WebSocket("ws://localhost:8000/ws");

        socket.onopen = function() {
            console.log("Connected to the WebSocket server.");
        };

        socket.onmessage = function(event) {
            console.log("Message from server: " + event.data);
        };

        socket.onclose = function() {
            console.log("Disconnected from the WebSocket server.");
        };

        document.getElementById("sendButton").addEventListener("click", function() {
            const message = document.getElementById("messageInput").value;
            if (message) {
                socket.send(message);
                document.getElementById("messageInput").value = ""; // Clear the textarea after sending
            }
        });
    </script>
</body>
</html>

"""


@app.get("/")
async def endpoint1():
    return HTMLResponse(html)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"hello websocket: {data}")


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)