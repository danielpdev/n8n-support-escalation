from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.core import Helpdesk

app = FastAPI(title="Synthetic helpdesk and local notification inbox")


@lru_cache
def service():
    return Helpdesk()


class TicketIn(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=4000)


class Notify(BaseModel):
    ticket_id: str
    channel: str


@app.post("/api/classify")
def classify(b: TicketIn):
    try:
        return service().intake(b.id, b.text)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.post("/api/notify")
def notify(b: Notify):
    try:
        return service().notify(b.ticket_id, b.channel)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.get("/api/inbox")
def inbox():
    return service().inbox()


@app.get("/api/overdue")
def overdue():
    return service().overdue()
