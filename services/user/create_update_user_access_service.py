from models.common_model import StandardResponse
from models.user_model import CreateUpdateUserAccessRequest
from services.user import get_room_service


def main(request: CreateUpdateUserAccessRequest) -> StandardResponse:
    valid_rooms: dict = {}

    for room in request.room_access:
        room_detail: list = get_room_service.main(room)
        if len(room_detail) > 0:
            valid_rooms[room] = True
        else:
            valid_rooms[room] = False

    # Step 2: Check if user exists

    # Step 3: Update
