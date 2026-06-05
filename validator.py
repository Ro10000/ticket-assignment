from pydantic import BaseModel
from typing import Literal


class Ticket(BaseModel):
    category: str
    urgency: Literal[
        "low",
        "medium",
        "high"
    ]
    summary: str
    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ]