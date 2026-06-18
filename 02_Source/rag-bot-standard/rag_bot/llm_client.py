import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable, Iterator


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"
DEEPSEEK_CHAT_COMPLETIONS_URL = "https://api.deepseek.com/chat/completions"


@dataclass(frozen=True)
class OpenAICompatibleClient:
    api_key: str
    model: str
    base_url: str
    temperature: float = 0.2
    timeout: int = 60

    def _build_payload(self, prompt: str, stream: bool = False) -> dict:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": "你是一个可靠、简洁、只基于上下文回答的中文 RAG 助手。"},
                {"role": "user", "content": prompt},
            ],
        }
        if stream:
            payload["stream"] = True
        return payload

    def _build_request(self, payload: dict) -> urllib.request.Request:
        return urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

    def generate(self, prompt: str) -> str:
        request = self._build_request(self._build_payload(prompt))
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed with HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LLM request failed: {exc.reason}") from exc

        return data["choices"][0]["message"]["content"]

    def generate_stream(self, prompt: str) -> Iterator[str]:
        request = self._build_request(self._build_payload(prompt, stream=True))
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                yield from parse_stream_content(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed with HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LLM request failed: {exc.reason}") from exc


def parse_stream_content(lines: Iterable[bytes | str]) -> Iterator[str]:
    for raw_line in lines:
        if isinstance(raw_line, bytes):
            line = raw_line.decode("utf-8", errors="replace").strip()
        else:
            line = raw_line.strip()

        if not line or line.startswith(":") or not line.startswith("data:"):
            continue

        data_text = line.removeprefix("data:").strip()
        if data_text == "[DONE]":
            break

        try:
            data = json.loads(data_text)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"LLM stream returned malformed JSON: {data_text}") from exc

        choices = data.get("choices", [])
        if not choices:
            continue

        delta = choices[0].get("delta", {})
        content = delta.get("content")
        if content:
            yield content


def get_env_api_key(provider: str) -> str:
    if provider == "Groq":
        return os.getenv("GROQ_API_KEY", "")
    if provider == "DeepSeek":
        return os.getenv("DEEPSEEK_API_KEY", "")
    if provider == "OpenAI":
        return os.getenv("OPENAI_API_KEY", "")
    return os.getenv("OPENAI_COMPATIBLE_API_KEY", "")


def get_default_model(provider: str) -> str:
    if provider == "Groq":
        return "llama-3.1-8b-instant"
    if provider == "DeepSeek":
        return "deepseek-v4-pro"
    if provider == "OpenAI":
        return "gpt-4o-mini"
    return os.getenv("OPENAI_COMPATIBLE_MODEL", "")


def get_default_base_url(provider: str) -> str:
    if provider == "Groq":
        return GROQ_CHAT_COMPLETIONS_URL
    if provider == "DeepSeek":
        return DEEPSEEK_CHAT_COMPLETIONS_URL
    if provider == "OpenAI":
        return OPENAI_CHAT_COMPLETIONS_URL
    return os.getenv("OPENAI_COMPATIBLE_BASE_URL", "")
