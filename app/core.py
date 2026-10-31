import json
import tempfile
import time
from pathlib import Path
from sqlalchemy import String, Float, select
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base, database


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str]
    route: Mapped[str]
    deadline: Mapped[float] = mapped_column(Float)


class Notification(Base):
    __tablename__ = "local_inbox"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    body: Mapped[str]


def classify(text):
    t = text.lower()
    if any(w in t for w in ["outage", "production down", "cannot log in", "500 error"]):
        return "urgent", 3600
    if any(w in t for w in ["invoice", "refund", "billing"]):
        return "billing", 86400
    return "general", 172800


class Helpdesk:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)

    def intake(self, tid, text, now=None):
        if not tid.strip() or not text.strip():
            raise ValueError("ticket ID and text required")
        route, sla = classify(text)
        with self.sessions.begin() as s:
            old = s.get(Ticket, tid)
            if old:
                if old.text != text:
                    raise ValueError("ticket ID reused for different content")
                return self.view(old)
            t = Ticket(id=tid, text=text, route=route, deadline=(time.time() if now is None else now) + sla)
            s.add(t)
            return self.view(t)

    @staticmethod
    def view(t):
        return dict(id=t.id, text=t.text, route=t.route, deadline=t.deadline)

    def notify(self, tid, channel):
        with self.sessions.begin() as s:
            t = s.get(Ticket, tid)
            if not t:
                raise ValueError("unknown ticket")
            expected = "on-call" if t.route == "urgent" else "support"
            if channel != expected:
                raise ValueError("incorrect notification route")
            key = tid + ":" + channel
            if s.get(Notification, key):
                return {"duplicate": True}
            s.add(Notification(id=key, body=json.dumps(dict(ticket=self.view(t), channel=channel))))
            return {"duplicate": False}

    def inbox(self):
        with self.sessions() as s:
            return [json.loads(n.body) for n in s.scalars(select(Notification))]

    def overdue(self, now=None):
        now = time.time() if now is None else now
        with self.sessions() as s:
            return [self.view(t) for t in s.scalars(select(Ticket).where(Ticket.deadline < now))]


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        s = Helpdesk("sqlite:///" + str(Path(d) / "support.sqlite"))
        ticket = s.intake("DEMO-1", "Production down: checkout outage", now=100)
        s.notify(ticket["id"], "on-call")
        retry = s.notify(ticket["id"], "on-call")
        return dict(ticket=ticket, retry=retry, inbox=s.inbox(), overdue=s.overdue(now=4000))


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(
        passed=r["ticket"]["route"] == "urgent" and r["retry"]["duplicate"] and len(r["inbox"]) == 1,
        scenario=r,
    )
