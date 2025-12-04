from typing import List
from pydantic import BaseModel


# Task-related models
class TaskCreate(BaseModel):
    title: str
    status: str = "open"


class Task(BaseModel):
    id: int
    title: str
    status: str


class AddRequest(BaseModel):
    a: int
    b: int


class AddResponse(BaseModel):
    result: int
    note: str


class WebhookPayload(BaseModel):
    source: str
    payload: dict


class WebRTCOffer(BaseModel):
    sdp: str
    type: str  # usually "offer"


class WebRTCAnswer(BaseModel):
    sdp: str
    type: str  # usually "answer"
    note: str
