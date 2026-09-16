from utils.sql_manager import execute


def main(request: int | None) -> bool:
    if request:
        query: str = 'SELECT roomname FROM "Room" WHERE id = %s AND active = true'
        result, _ = execute(query, (request, ))
    else:
        query: str = 'SELECT * FROM "Room" WHERE active = true'
        result, _ = execute(query, ())

    return result
