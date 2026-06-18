import os
from dataclasses import dataclass
from typing import Mapping


DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "ragbot"


@dataclass(frozen=True)
class LoginConfig:
    username: str
    password: str
    uses_default_password: bool


def get_login_config(env: Mapping[str, str] | None = None) -> LoginConfig:
    values = env if env is not None else os.environ
    username = values.get("RAG_BOT_USERNAME", DEFAULT_USERNAME)
    password = values.get("RAG_BOT_PASSWORD", DEFAULT_PASSWORD)

    return LoginConfig(
        username=username,
        password=password,
        uses_default_password=(
            username == DEFAULT_USERNAME
            and password == DEFAULT_PASSWORD
            and "RAG_BOT_USERNAME" not in values
            and "RAG_BOT_PASSWORD" not in values
        ),
    )


def authenticate(username: str, password: str, config: LoginConfig) -> bool:
    if not username or not password:
        return False
    return username == config.username and password == config.password
