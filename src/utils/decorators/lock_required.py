"""
This module contains custom decorators to insure node locked.
"""
from __future__ import annotations

from functools import wraps
from typing import Any
from typing import Callable

from requests import HTTPError
from requests.exceptions import ConnectionError as RequestsConnectionError

from src.utils.custom_exception import CommonException
from src.utils.endpoints import LOCK_ENDPOINT
from src.utils.helpers import check_node
from src.utils.helpers import handle_connection_error
from src.utils.helpers import handle_generic_error
from src.utils.request import Request


def call_lock() -> None:
    """Unlock the node by sending a request to the unlock endpoint."""
    try:
        response = Request.post(LOCK_ENDPOINT)
        response.raise_for_status()
    except HTTPError as exc:
        error_details = exc.response.json()
        error_message = error_details.get('error', 'Unspecified server error')
        raise CommonException(error_message) from exc
    except RequestsConnectionError as exc:
        handle_connection_error('call_lock', exc)
    except Exception as exc:
        handle_generic_error(
            'call_lock', exc, 'Decorator(call_lock): Error while calling lock API',
        )


def lock_required(method: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to ensure the node is unlocked before proceeding with the decorated method."""
    @wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not check_node('lock_required'):
            call_lock()
        return method(*args, **kwargs)

    return wrapper
