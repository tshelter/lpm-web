import uuid

import asyncio
import logging
import websockets
from pydantic import BaseModel

URL = "ws://localhost:8000/agent_ws/agent1"


class Log(BaseModel):
    message: str
    service: str


class Action(BaseModel):
    action: str
    service: str


class Request(BaseModel):
    uuid: str | None
    payload: Log | Action
    agent_id: str


class Response(BaseModel):
    uuid: str | None
    payload: dict
    agent_id: str


async def send_logs(socket: websockets.WebSocketClientProtocol):
    while True:
        log = Log(message="This is a log message", service="service1")
        await socket.send(Request(
            uuid=None,
            payload=log,
            agent_id="agent1",
        ).json())
        await asyncio.sleep(1)


async def handle_request(socket: websockets.WebSocketClientProtocol):
    while True:
        try:
            request = Request.parse_raw(await socket.recv())
        except Exception as e:
            logging.exception(e)
            continue

        print(request)
        if isinstance(request.payload, Log):
            print(f"Received log: {request.payload}")
        elif isinstance(request.payload, Action):
            print(f"Received action: {request.payload}")
            response = Response(
                payload={"status": "ok", "uuid": request.uuid},
                uuid=str(uuid.uuid4()),
                agent_id="agent1",
            )
            await socket.send(response.json())


async def main():
    async with websockets.connect(URL) as socket:
        asyncio.create_task(handle_request(socket))
        asyncio.create_task(send_logs(socket))
        await asyncio.Event().wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
