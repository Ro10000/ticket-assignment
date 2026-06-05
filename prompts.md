# Prompt Experiments

## Version 1

Convert the customer message into JSON.

### Result

The model often returned explanations and invalid JSON.

---

## Version 2

Return only JSON.

### Result

Fewer explanations, but sometimes invalid values such as "High" instead of "high".

---

## Version 3

Return ONLY valid JSON matching this schema:

{
"category": "string",
"urgency": "low|medium|high",
"summary": "string",
"sentiment": "positive|neutral|negative"
}

Do not use markdown.
Do not add text before or after the JSON.

### Result

Most reliable output with the fewest retries and valid schema-compliant responses.
