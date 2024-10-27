from enum import Enum


class DateFilterType(Enum):
    EQUAL = "EQUAL"
    AFTER = "AFTER"
    BEFORE = "BEFORE"