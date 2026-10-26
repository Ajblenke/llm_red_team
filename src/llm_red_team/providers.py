"""One chat interface over Gemini and OpenAI, so each test is written once and runs on both.

A provider takes a system prompt and a list of turns and returns the reply text.
A turn is {"role": "user" or "model", "text": str, "image": bytes or None}.
"""

import base64
from typing import Protocol

from google import genai
from google.genai import types


class Chat(Protocol):
    name: str
    settings: dict

    def reply(self, system: str | None, turns: list[dict]) -> str: ...


class GeminiChat:
    def __init__(self, model: str):
        self.client = genai.Client()
        self.name = model
        # The earlier runs used the API defaults, so these stay on defaults to remain comparable.
        self.settings = {"provider": "gemini", "generation": "API defaults"}

    def reply(self, system: str | None, turns: list[dict]) -> str:
        contents = []
        for turn in turns:
            parts = [types.Part.from_text(text=turn["text"])]
            if turn.get("image"):
                parts.insert(
                    0, types.Part.from_bytes(data=turn["image"], mime_type="image/png")
                )
            contents.append(types.Content(role=turn["role"], parts=parts))
        config = types.GenerateContentConfig(system_instruction=system)
        response = self.client.models.generate_content(
            model=self.name, contents=contents, config=config
        )
        return response.text or ""


class OpenAIChat:
    # The smallest effort the model accepts, to match a lite tier model answering directly.
    EFFORT = "none"

    def __init__(self, model: str):
        from openai import OpenAI

        self.client = OpenAI()
        self.name = model
        self.settings = {"provider": "openai", "reasoning_effort": self.EFFORT}

    def reply(self, system: str | None, turns: list[dict]) -> str:
        messages = [{"role": "system", "content": system}] if system else []
        for turn in turns:
            role = "assistant" if turn["role"] == "model" else "user"
            if turn.get("image"):
                url = (
                    "data:image/png;base64," + base64.b64encode(turn["image"]).decode()
                )
                content = [
                    {"type": "image_url", "image_url": {"url": url}},
                    {"type": "text", "text": turn["text"]},
                ]
            else:
                content = turn["text"]
            messages.append({"role": role, "content": content})
        response = self.client.chat.completions.create(
            model=self.name, messages=messages, reasoning_effort=self.EFFORT
        )
        return response.choices[0].message.content or ""


def make_chat(provider: str, model: str) -> Chat:
    return GeminiChat(model) if provider == "gemini" else OpenAIChat(model)
