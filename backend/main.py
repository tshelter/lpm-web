import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/agent_ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    await manager.connect_agent(agent_id, websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            client_id = json.loads(msg).get("client_id")
            await manager.send_to_clients(msg, client_id=client_id)

    except WebSocketDisconnect:
        manager.disconnect_agent(agent_id)


@app.websocket("/client_ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect_client(client_id, websocket)

    try:
        while True:
            msg = await websocket.receive_text()
            agent_id = json.loads(msg)["agent_id"]
            await manager.send_to_agent(agent_id, msg)

    except WebSocketDisconnect:
        manager.disconnect_client(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
