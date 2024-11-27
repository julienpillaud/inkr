import pytest

from app.filters import (
    FilterEntity,
    FilterOperator,
    FiltersParsingError,
    parse_filter,
    parse_filters,
)


def assert_filter(
    result: FilterEntity,
    expected_field: str,
    expected_value: str | list[str],
    expected_operator: FilterOperator,
) -> None:
    assert result.field == expected_field
    assert result.value == expected_value
    assert result.operator == expected_operator


def test_parse_simple_equal() -> None:
    result = parse_filter("status=active")
    assert_filter(result, "status", "active", FilterOperator.EQ)


@pytest.mark.parametrize(
    "filter_str,field,value,operator",
    [
        ("price[gt]=100", "price", "100", FilterOperator.GT),
        ("price[gte]=100", "price", "100", FilterOperator.GTE),
        ("price[lt]=100", "price", "100", FilterOperator.LT),
        ("price[lte]=100", "price", "100", FilterOperator.LTE),
    ],
)
def test_parse_comparison_operators(
    filter_str: str, field: str, value: str, operator: FilterOperator
) -> None:
    result = parse_filter(filter_str)
    assert_filter(result, field, value, operator)


def test_parse_in_operator() -> None:
    result = parse_filter("status[in]=(active,pending)")
    assert_filter(result, "status", ["active", "pending"], FilterOperator.IN)


def test_parse_nin_operator() -> None:
    result = parse_filter("status[nin]=(deleted,archived)")
    assert_filter(result, "status", ["deleted", "archived"], FilterOperator.NIN)


def test_parse_multiple_filters() -> None:
    filters = "status[in]=(active,pending),price[gt]=100,category=books"
    results = parse_filters(filters)

    assert_filter(results[0], "status", ["active", "pending"], FilterOperator.IN)
    assert_filter(results[1], "price", "100", FilterOperator.GT)
    assert_filter(results[2], "category", "books", FilterOperator.EQ)


@pytest.mark.parametrize(
    "filter_str,expected_message",
    [
        # Invalid format for IN/NIN filter
        ("field[in]=value", "Invalid format for IN/NIN operator."),
        ("field[in]=()", "Invalid format for IN/NIN operator."),
        ("field[in]=(,)", "Invalid format for IN/NIN operator."),
        ("[in]=(value)", "Invalid format for IN/NIN operator."),
        ("@field[in]=(value)", "Invalid format for IN/NIN operator."),
        ("field[in]=(value,)", "Invalid format for IN/NIN operator."),
        ("field[in]=(,value)", "Invalid format for IN/NIN operator."),
        # Invalid format for comparison filter
        ("field[invalid]=value", "Invalid format for comparison operator."),
        ("field[gt]=", "Invalid format for comparison operator."),
        ("[gt]=value", "Invalid format for comparison operator."),
        ("field[]=value", "Invalid format for comparison operator."),
        ("field[gt]value", "Invalid format for comparison operator."),
        ("@field[gt]=value", "Invalid format for comparison operator."),
        # Invalid format for equality filter
        ("=value", "Invalid format for equality operator."),
        ("field=", "Invalid format for equality operator."),
        ("field==value", "Invalid format for equality operator."),
        ("field=value=", "Invalid format for equality operator."),
        ("@field=value", "Invalid format for equality operator."),
        ("field=@", "Invalid format for equality operator."),
    ],
)
def test_invalid_filters(filter_str: str, expected_message: str) -> None:
    with pytest.raises(FiltersParsingError) as exc_info:
        parse_filter(filter_str)

    assert str(exc_info.value) == expected_message
