import asyncio
import logging
import uuid

import websockets
from schemas import ActionRequest, AgentRequest, AgentResponse

URL = "ws://localhost:8000/client_ws/client1"
AGENT_ID = "test_agent"
ACTION = "restart"
SERVICE = "http"


async def handle_incoming(socket: websockets.WebSocketClientProtocol):
    while True:
        data = await socket.recv()
        response = AgentResponse.parse_raw(data)
        print(f"Received {response}")


async def send_requests(socket: websockets.WebSocketClientProtocol):
    while True:
        await asyncio.sleep(3)
        request = AgentRequest(
            uuid=str(uuid.uuid4()),
            action=ActionRequest(action=ACTION, service=SERVICE),
            agent_id=AGENT_ID,
        )
        print(f"Sending {request}")
        await socket.send(request.json(exclude_none=True))
        await asyncio.sleep(7)


async def main():
    async with websockets.connect(URL) as socket:
        asyncio.create_task(handle_incoming(socket))
        asyncio.create_task(send_requests(socket))
        await asyncio.Event().wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
