import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.websocket("/agent_ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    if agent_id:
        await manager.connect_agent(agent_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_to_clients(data)
    except WebSocketDisconnect:
        manager.disconnect_agent(agent_id)


@app.websocket("/client_ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    if client_id:
        await manager.connect_client(client_id, websocket)

    try:
        while True:
            data = json.loads(await websocket.receive_text())
            agent_id = data["agent_id"]
            await manager.send_to_agent(agent_id, json.dumps(data))

    except WebSocketDisconnect:
        manager.disconnect_client(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
