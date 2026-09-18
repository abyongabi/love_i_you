from utils.sql_manager import execute
from utils.request_context import get_user_id


def main(room_id: int | None, goal_id: int | None) -> dict:
    if room_id:
        query: str = 'SELECT id, title, budget, room_id, progress, priority FROM "Goal" WHERE room_id = %s AND user_id = %s'
        result, _ = execute(query, (room_id, get_user_id()))
    elif goal_id:
        query: str = 'SELECT id, title, budget, room_id, progress, priority FROM "Goal" WHERE id = %s AND user_id = %s'
        result, _ = execute(query, (goal_id, get_user_id()))
    else:
        query: str = 'SELECT id, title, budget, room_id, progress, priority FROM "Goal" WHERE active = TRUE'
        result, _ = execute(query, ())

    return result
