from pydantic import BaseModel
from typing import Literal


class Ticket(BaseModel):

    category: str
    category_confidence: float

    urgency: Literal[
        "low",
        "medium",
        "high"
    ]
    urgency_confidence: float

    summary: str
    summary_confidence: float

    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ]
    sentiment_confidence: float

    human_review: bool