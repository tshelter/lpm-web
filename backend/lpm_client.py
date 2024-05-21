import asyncio
import logging
import uuid

import websockets
from schemas import Action, Request, Response

URL = "ws://localhost:8000/client_ws/client1"


async def handle_incoming(socket: websockets.WebSocketClientProtocol):
    while True:
        data = await socket.recv()
        response = Response.parse_raw(data)
        print(response)


async def send_requests(socket: websockets.WebSocketClientProtocol):
    while True:
        request = Request(
            uuid=str(uuid.uuid4()),
            payload=Action(action="restart", service="service1"),
            agent_id="agent1",
        )
        print(f"Sending {request}")
        await socket.send(request.json())
        await asyncio.sleep(10)


async def main():
    # It will connect to the websocket server,
    # Generate fake logs every 1 second
    # Also it listens for messages from the server and prints them
    # Also it returns result after 0.5 seconds
    async with websockets.connect(URL) as socket:
        asyncio.create_task(handle_incoming(socket))
        asyncio.create_task(send_requests(socket))
        await asyncio.Event().wait()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
