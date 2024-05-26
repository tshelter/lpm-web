from pydantic import BaseModel


class LogResponse(BaseModel):
    message: str
    service: str


class ActionRequest(BaseModel):
    action: str
    service: str


class ActionResponse(BaseModel):
    response: str


class StatusRequest(BaseModel):
    service: str | None = None


class Service(BaseModel):
    name: str
    is_active: bool
    is_enabled: bool
    memory: str


class StatusResponse(BaseModel):
    services: list[Service]


class AgentRequest(BaseModel):
    uuid: str
    agent_id: str

    action: ActionRequest | None = None
    status: StatusRequest | None = None


class AgentResponse(BaseModel):
    uuid: str | None = None
    agent_id: str

    action: ActionResponse | None = None
    log: LogResponse | None = None
    status: StatusResponse | None = None
