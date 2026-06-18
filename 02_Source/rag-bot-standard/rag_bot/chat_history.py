MESSAGE_KEY = "messages"
ALLOWED_ROLES = {"user", "assistant"}


def get_messages(state) -> list[dict[str, str]]:
    if MESSAGE_KEY not in state:
        state[MESSAGE_KEY] = []
    return state[MESSAGE_KEY]


def add_message(state, role: str, content: str) -> None:
    if role not in ALLOWED_ROLES:
        raise ValueError("Message role must be 'user' or 'assistant'.")
    if not content or not content.strip():
        raise ValueError("Message content cannot be empty.")

    get_messages(state).append({"role": role, "content": content.strip()})


def clear_messages(state) -> None:
    state[MESSAGE_KEY] = []
