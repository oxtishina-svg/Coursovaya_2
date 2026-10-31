import pytest

from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes_by_country,
    get_top_aeroplanes,
    parse_top_n,
    sort_aeroplanes_by_altitude,
)


def make_aeroplanes() -> list[Aeroplane]:
    return [
        Aeroplane(
            "FIN1",
            "Finland",
            200,
            5000,
        ),
        Aeroplane(
            "GER1",
            "Germany",
            250,
            12000,
        ),
        Aeroplane(
            "FIN2",
            "Finland",
            180,
            8000,
        ),
    ]


def test_filter_aeroplanes_by_country() -> None:
    aeroplanes = make_aeroplanes()

    result = filter_aeroplanes_by_country(
        aeroplanes,
        ["Finland"],
    )

    assert len(result) == 2
    assert all(aeroplane.origin_country == "Finland" for aeroplane in result)


def test_filter_is_case_insensitive() -> None:
    result = filter_aeroplanes_by_country(
        make_aeroplanes(),
        ["fInLaNd"],
    )

    assert len(result) == 2


def test_filter_multiple_countries() -> None:
    result = filter_aeroplanes_by_country(
        make_aeroplanes(),
        [
            "Finland",
            "Germany",
        ],
    )

    assert len(result) == 3


def test_filter_empty_country_list_returns_all() -> None:
    aeroplanes = make_aeroplanes()

    result = filter_aeroplanes_by_country(
        aeroplanes,
        [],
    )

    assert result == aeroplanes


def test_sort_aeroplanes_by_altitude() -> None:
    result = sort_aeroplanes_by_altitude(make_aeroplanes())

    assert [aeroplane.altitude for aeroplane in result] == [
        12000.0,
        8000.0,
        5000.0,
    ]


def test_get_top_aeroplanes() -> None:
    result = get_top_aeroplanes(
        make_aeroplanes(),
        2,
    )

    assert len(result) == 2
    assert result[0].callsign == "GER1"
    assert result[1].callsign == "FIN2"


def test_get_top_aeroplanes_invalid_number() -> None:
    with pytest.raises(ValueError):
        get_top_aeroplanes(
            make_aeroplanes(),
            0,
        )


def test_parse_top_n() -> None:
    assert parse_top_n("5") == 5


def test_parse_top_n_invalid_string() -> None:
    with pytest.raises(
        ValueError,
        match="Введите целое число",
    ):
        parse_top_n("abc")


def test_parse_top_n_negative_number() -> None:
    with pytest.raises(
        ValueError,
        match="больше нуля",
    ):
        parse_top_n("-1")
