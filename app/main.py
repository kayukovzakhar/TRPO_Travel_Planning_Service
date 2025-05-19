from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Получен запрос: {data}")

            suggestions = [
                {
                    "name": f"Музей в {data}",
                    "description": "Интересный музей для посещения.",
                    "tags": ["искусство", "история"]
                },
                {
                    "name": f"Парк в {data}",
                    "description": "Красивый парк для отдыха и прогулок.",
                    "tags": ["природа", "отдых"]
                },
            ]

            await websocket.send_json(suggestions)
    except WebSocketDisconnect:
        print("Клиент отключился")