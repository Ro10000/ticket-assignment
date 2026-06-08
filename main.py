import json
import re
from ollama import chat
from validator import Ticket
from pydantic import ValidationError

MAX_RETRIES = 3


def classify_message(message):

    prompt = f"""
You are a customer support classifier.

Return ONLY a valid JSON object.

DO NOT explain.
DO NOT use markdown.
DO NOT add any text before or after JSON.

Provide confidence scores between 0 and 1.

Schema:
{{
    "category": "string",
    "category_confidence": 0.95,

    "urgency": "low|medium|high",
    "urgency_confidence": 0.95,

    "summary": "string",
    "summary_confidence": 0.95,

    "sentiment": "positive|neutral|negative",
    "sentiment_confidence": 0.95
}}

Message:
{message}
"""

    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def process_message(message):

    for attempt in range(MAX_RETRIES):

        try:

            result = classify_message(
                message
            )

            print("\nRAW RESPONSE:")
            print(result)
            print("-" * 50)

            match = re.search(
                r"\{.*\}",
                result,
                re.DOTALL
            )

            if not match:
                raise ValueError(
                    "No JSON found"
                )

            json_text = match.group()

            ticket = json.loads(
                json_text
            )

            ticket["urgency"] = (
                str(
                    ticket.get(
                        "urgency",
                        "low"
                    )
                )
                .strip()
                .lower()
            )

            ticket["sentiment"] = (
                str(
                    ticket.get(
                        "sentiment",
                        "neutral"
                    )
                )
                .strip()
                .lower()
            )

            if ticket["urgency"] in [
                "none",
                "neutral",
                "null",
                ""
            ]:
                ticket["urgency"] = "low"

            if (
                ticket.get("category")
                is None
            ):
                ticket["category"] = (
                    "general"
                )

            if (
                ticket.get("summary")
                is None
            ):
                ticket["summary"] = (
                    "No summary provided"
                )

            ticket.setdefault(
                "category_confidence",
                0.50
            )

            ticket.setdefault(
                "urgency_confidence",
                0.50
            )

            ticket.setdefault(
                "summary_confidence",
                0.50
            )

            ticket.setdefault(
                "sentiment_confidence",
                0.50
            )

            average_confidence = (
                float(
                    ticket[
                        "category_confidence"
                    ]
                )
                + float(
                    ticket[
                        "urgency_confidence"
                    ]
                )
                + float(
                    ticket[
                        "summary_confidence"
                    ]
                )
                + float(
                    ticket[
                        "sentiment_confidence"
                    ]
                )
            ) / 4

            ticket["human_review"] = (
                average_confidence
                < 0.70
            )

            validated = Ticket(
                **ticket
            )

            return (
                validated.model_dump()
            )

        except (
            json.JSONDecodeError,
            ValidationError,
            ValueError,
            KeyError
        ) as error:

            print(
                f"Retry {attempt + 1} for:"
            )

            print(message)
            print(error)

    return {
        "category": "unknown",
        "category_confidence": 0.0,

        "urgency": "low",
        "urgency_confidence": 0.0,

        "summary":
            "Could not classify message",
        "summary_confidence": 0.0,

        "sentiment": "neutral",
        "sentiment_confidence": 0.0,

        "human_review": True
    }


def load_messages():

    with open(
        "messages.txt",
        "r",
        encoding="utf-8"
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def save_results(tickets):

    with open(
        "tickets.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            tickets,
            file,
            indent=4
        )


def main():

    messages = load_messages()

    total_tokens = 0

    for message in messages:

        total_tokens += len(
            message.split()
        )

    tickets = []

    print(
        f"Found {len(messages)} messages\n"
    )

    for message in messages:

        print(
            f"Processing: {message}"
        )

        ticket = process_message(
            message
        )

        tickets.append(ticket)

    save_results(tickets)

    human_review_count = sum(
        1
        for ticket in tickets
        if ticket[
            "human_review"
        ]
    )

    print("\nDone!")

    print(
        f"Processed {len(tickets)} tickets."
    )

    print(
        f"Human Review Needed: {human_review_count}"
    )

    print(
        "Results saved to tickets.json"
    )

    print("\nUsage Report")

    print(
        f"Estimated Tokens: {total_tokens}"
    )

    print(
        "Estimated Cost: $0.00"
    )

    print(
        "(Local Ollama Model)"
    )


if __name__ == "__main__":
    main()