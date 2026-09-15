from models.common_model import StandardResponse
from models.user_model import LoginRequest
from utils.crypto import verify_value, create_access_token
from utils.sql_manager import execute


def main(request: LoginRequest):
    query: str = 'SELECT id, password FROM "Users" WHERE username = %s'
    result, _ = execute(query, (request.username, ))

    id, stored_password = result if result else (None, None)
    status: bool = bool(stored_password) and verify_value(request.password, stored_password)
    message: str = create_access_token(get_token_payload(request, id)) if status else "Invalid credentials, please try again."

    return StandardResponse(success=status, message=message)


def get_token_payload(request: LoginRequest, id: int):
    # to be updated with user settings like audit etc
    return {
        "username": request.username,
        "user_id": id
    }