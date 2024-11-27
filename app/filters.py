import re
from enum import StrEnum

from pydantic import BaseModel

# Split on commas, but ignore commas inside parentheses
pattern_split = re.compile(
    r","  # Match a comma
    r"(?!"  # Negative lookahead - make sure what follows is not...
    r"[^(]*"  # Any number of non-opening-parentheses characters
    r"\)"  # Followed by a closing parenthesis
    r")"
)

# Common patterns
FIELD_PATTERN = r"(?P<field>\w+)"
VALUE_PATTERN = r"(?P<value>[\w .-]+)"

# Match simple equality filters (field=value)
pattern_equal = re.compile(
    r"^"  # Start
    f"{FIELD_PATTERN}"  # Field name
    r"="
    f"{VALUE_PATTERN}"  # Value
    r"$"  # End
)

# Match comparison operators (field[gt]=value)
pattern_comparison = re.compile(
    r"^"  # Start
    f"{FIELD_PATTERN}"  # Field name
    r"\[(?P<operator>gt|gte|lt|lte)]"  # Operator
    r"="
    f"{VALUE_PATTERN}"  # Value
    r"$"  # End
)

# Match IN/NIN filters (field[in]=(val1,val2))
pattern_in = re.compile(
    r"^"  # Start
    f"{FIELD_PATTERN}"  # Field name
    r"\[(?P<operator>in|nin)]"  # IN/NIN operator
    r"="
    r"\("  # Opening parenthesis
    r"(?P<value>[\w .-]+(,[\w .-]+)*)"  # One or more values separated by commas
    r"\)"  # Closing parenthesis
    r"$"  # End
)


class FiltersParsingError(Exception):
    pass


class FilterOperator(StrEnum):
    EQ = "eq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"


class FilterEntity(BaseModel):
    field: str
    value: str | list[str]
    operator: FilterOperator = FilterOperator.EQ


def parse_filters(filters: str) -> list[FilterEntity]:
    """Parse the filter query parameter string according to the query language

    Each filter is format as `[field][operator][value]` and is separated by a comma `,`
    The operator must be one of the following:
        `=` for equality
        `[gt]=` for greater than
        `[gte]=` for greater or equal than
        `[lt]=` for less than
        `[lte]=` for less or equal than
        `[in]=(value1,value2,value3)` for inclusion in values
        `[nin]=(value1,value2,value3)` for exclusion from values
    """
    return [parse_filter(string.strip()) for string in re.split(pattern_split, filters)]


def parse_filter(string: str) -> FilterEntity:
    if "[in]=" in string or "[nin]=" in string:
        return parse_in_nin_filter(string)

    if "[" in string and "]" in string:
        return parse_comparison_filter(string)

    if "=" in string:
        return parse_equal_filter(string)

    raise FiltersParsingError("Invalid filter format.")


def parse_equal_filter(string: str) -> FilterEntity:
    if not (match := pattern_equal.match(string)):
        raise FiltersParsingError("Invalid format for equality operator.")

    return FilterEntity.model_validate(match.groupdict())


def parse_comparison_filter(string: str) -> FilterEntity:
    if not (match := pattern_comparison.match(string)):
        raise FiltersParsingError("Invalid format for comparison operator.")

    return FilterEntity.model_validate(match.groupdict())


def parse_in_nin_filter(string: str) -> FilterEntity:
    if not (match := pattern_in.match(string)):
        raise FiltersParsingError("Invalid format for IN/NIN operator.")

    groups = match.groupdict()
    values = [v.strip() for v in groups["value"].split(",")]

    return FilterEntity(
        field=groups["field"], operator=FilterOperator(groups["operator"]), value=values
    )
