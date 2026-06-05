from ollama import chat


def summarize(text):

    stream = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": f"Summarize:\n\n{text}"
            }
        ],
        stream=True
    )

    for chunk in stream:

        print(
            chunk["message"]["content"],
            end="",
            flush=True
        )


if __name__ == "__main__":

    webpage = """
    Artificial Intelligence is changing industries.
    Companies use AI for automation,
    customer support,
    data analysis,
    and software development.
    """

    summarize(webpage)
    