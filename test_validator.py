from validator import Ticket
from pydantic import ValidationError
import pytest


def test_valid_ticket():

    ticket = Ticket(
        category="billing",
        urgency="high",
        summary="Customer charged twice",
        sentiment="negative"
    )

    assert ticket.urgency == "high"


def test_invalid_urgency():

    with pytest.raises(ValidationError):

        Ticket(
            category="billing",
            urgency="urgent",
            summary="Customer charged twice",
            sentiment="negative"
        )


def test_invalid_sentiment():

    with pytest.raises(ValidationError):

        Ticket(
            category="billing",
            urgency="high",
            summary="Customer charged twice",
            sentiment="angry"
        )