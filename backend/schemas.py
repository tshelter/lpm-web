from pydantic import BaseModel


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
