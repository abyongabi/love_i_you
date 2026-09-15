from fastapi import HTTPException
from starlette.requests import Request

from services.auth_service import decode_token
from utils.request_context import reset_request_context, set_request_context


async def populate_request_context(request: Request, call_next):
    context_token = None
    authorization = request.headers.get("Authorization", "")
    scheme, _, access_token = authorization.partition(" ")

    if scheme.lower() == "bearer" and access_token:
        try:
            claims = decode_token(access_token)
            user_id = claims.get("user_id")
            if isinstance(user_id, int):
                context_token = set_request_context(claims)
        except HTTPException:
            # Protected routes perform the authoritative token validation.
            pass

    try:
        return await call_next(request)
    finally:
        if context_token is not None:
            reset_request_context(context_token)
