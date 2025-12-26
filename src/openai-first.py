import os

from dotenv import load_dotenv
from openai import OpenAI


def chat_completion(
    messages,
    model="gpt-4o-mini",
    temperature=0.9,
    max_tokens=None,
    top_p=1.0,
    presence_penalty=0.0,
    frequency_penalty=0.0,
    response_format=None,
):
    """Small helper to send a chat request with a few knobs exposed."""

    # Load environment variables from a local .env file if present
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY first.")

    client = OpenAI(api_key=api_key)

    extras = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
    }

    if response_format:  # e.g. "json_object"
        extras["response_format"] = {"type": response_format}

    resp = client.chat.completions.create(
        model=model,
        messages=list(messages),
        **extras,
    )

    return resp.choices[0].message.content


if __name__ == "__main__":
    sample = [{"role": "user", "content": "Say one short fun fact about space."}]
    print(chat_completion(sample))
