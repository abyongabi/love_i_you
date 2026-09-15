from contextvars import ContextVar, Token
from typing import Any, Mapping


_request_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "request_context",
    default=None,
)


def set_request_context(context: Mapping[str, Any]) -> Token:
    return _request_context.set(dict(context))


def get_request_context() -> dict[str, Any]:
    return dict(_request_context.get() or {})


def get_context_value(field: str, default: Any = None) -> Any:
    return get_request_context().get(field, default)


def get_user_id() -> int | None:
    user_id = get_context_value("user_id")
    return user_id if isinstance(user_id, int) else None


def reset_request_context(token: Token) -> None:
    _request_context.reset(token)
