import logging
import psycopg2
from psycopg2.errors import UniqueViolation
from typing import Any

from utils.application_config import app_config
from utils.sql_exceptions import SQLExceptions


def execute(query: str, params=None) -> tuple[Any, str | None]:
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(app_config.db_url)
        cursor = connection.cursor()

        cursor.execute(query, params)
        connection.commit()

        if cursor.description:
            return cursor.fetchone(), None

        return True, None
    
    except UniqueViolation as error:
        if connection:
            connection.rollback()

        return False, SQLExceptions.UNIQUE_VIOLATION + " " + str(error)
    
    except Exception as error:
        logging.error(error)
        return False, str(error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
