import pytest
from app.core import Helpdesk, classify


def test_sla_dedup_and_wrong_channel(tmp_path):
    h = Helpdesk("sqlite:///" + str(tmp_path / "h.sqlite"))
    t = h.intake("a", "Production down", now=100)
    assert t["route"] == "urgent" and t["deadline"] == 3700
    with pytest.raises(ValueError):
        h.notify("a", "support")
    h.notify("a", "on-call")
    assert h.notify("a", "on-call")["duplicate"]
    assert len(h.inbox()) == 1 and len(h.overdue(3701)) == 1 and not h.overdue(3700)


@pytest.mark.parametrize(
    "text,route",
    [
        ("Please send my invoice", "billing"),
        ("How to change avatar", "general"),
        ("We see a 500 error", "urgent"),
    ],
)
def test_rules(text, route):
    assert classify(text)[0] == route
