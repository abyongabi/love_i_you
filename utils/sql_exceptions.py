from enum import StrEnum


class SQLExceptions(StrEnum):
    UNIQUE_VIOLATION = "UNIQUE_VIOLATION"