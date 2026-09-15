from models.common_model import StandardResponse
from models.user_model import CreateUserRequest
from utils.crypto import hash_value
from utils.sql_manager import execute

def main(request: CreateUserRequest) -> StandardResponse:
    hashed_password: str = hash_value(request.password)

    query: str = 'INSERT INTO "Users"(username, password, email) VALUES (%s, %s, %s)'
    result, message = execute(query, (request.username, hashed_password, request.email))

    return StandardResponse(success=result is not None, message=message)
