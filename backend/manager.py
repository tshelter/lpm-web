from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_agents: dict[str, WebSocket] = {}
        self.active_clients: dict[str, WebSocket] = {}

    async def connect_agent(self, agent_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_agents[agent_id] = websocket

    async def send_to_clients(self, message: str, /, client_id: str | None = None):
        if client_id and (client := self.active_clients.get(client_id)):
            await client.send_text(message)
            return

        for client in self.active_clients.values():
            await client.send_text(message)

    async def send_to_agent(self, agent_id: str, message: str):
        if agent := self.active_agents.get(agent_id):
            await agent.send_text(message)

    def disconnect_agent(self, agent_id: str):
        self.active_agents.pop(agent_id)

    async def connect_client(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_clients[client_id] = websocket

    def disconnect_client(self, client_id: str):
        self.active_clients.pop(client_id)
