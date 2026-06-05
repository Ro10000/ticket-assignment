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
DO NOT add any text before or after the JSON.

Schema:
{{
    "category": "string",
    "urgency": "low|medium|high",
    "summary": "string",
    "sentiment": "positive|neutral|negative"
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
            result = classify_message(message)

            print("\nRAW RESPONSE:")
            print(result)
            print("-" * 50)

            match = re.search(
                r"\{.*\}",
                result,
                re.DOTALL
            )

            if not match:
                raise ValueError("No JSON found")

            json_text = match.group()

            ticket = json.loads(json_text)

            # Normalize values
            ticket["urgency"] = (
                str(ticket.get("urgency", "low"))
                .strip()
                .lower()
            )

            ticket["sentiment"] = (
                str(ticket.get("sentiment", "neutral"))
                .strip()
                .lower()
            )

            # Fix common model mistakes
            if ticket["urgency"] in [
                "none",
                "neutral",
                "null",
                ""
            ]:
                ticket["urgency"] = "low"

            if ticket.get("category") is None:
                ticket["category"] = "general"

            if ticket.get("summary") is None:
                ticket["summary"] = "No summary provided"

            validated = Ticket(**ticket)

            return validated.model_dump()

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
        "urgency": "low",
        "summary": "Could not classify message",
        "sentiment": "neutral"
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

    print("\nDone!")

    print(
        f"Processed {len(tickets)} tickets."
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