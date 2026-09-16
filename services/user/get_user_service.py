from utils.sql_manager import execute


def main(request: int) -> list:
    query: str = 'SELECT * FROM "Users" WHERE id = %s'
    result, _ = execute(query, (request, ))

    return result
