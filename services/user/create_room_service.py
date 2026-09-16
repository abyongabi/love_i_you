from models.common_model import StandardResponse
from models.user_model import CreateRoomRequest
from utils.sql_manager import execute

def main(request: CreateRoomRequest) -> StandardResponse:
    query: str = 'INSERT INTO "Room"(roomname) VALUES (%s)'
    result, message = execute(query, (request.roomname,))

    return StandardResponse(success=result is not None, message=message)
