import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_initialization() -> None:
    aeroplane = Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=250.5,
        altitude=10000.0,
        longitude=24.9,
        latitude=60.1,
    )

    assert aeroplane.callsign == "FIN123"
    assert aeroplane.origin_country == "Finland"
    assert aeroplane.velocity == 250.5
    assert aeroplane.altitude == 10000.0
    assert aeroplane.longitude == 24.9
    assert aeroplane.latitude == 60.1


def test_empty_text_replaced_with_unknown() -> None:
    aeroplane = Aeroplane(
        callsign="   ",
        origin_country="",
        velocity=100,
        altitude=5000,
    )

    assert aeroplane.callsign == "Неизвестно"
    assert aeroplane.origin_country == "Неизвестно"


def test_invalid_text_type() -> None:
    with pytest.raises(TypeError):
        Aeroplane(
            callsign=123,  # type: ignore[arg-type]
            origin_country="Finland",
            velocity=100,
            altitude=5000,
        )


def test_invalid_number_type() -> None:
    with pytest.raises(TypeError):
        Aeroplane(
            callsign="FIN123",
            origin_country="Finland",
            velocity="fast",  # type: ignore[arg-type]
            altitude=5000,
        )


def test_none_number_becomes_zero() -> None:
    aeroplane = Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=None,  # type: ignore[arg-type]
        altitude=None,  # type: ignore[arg-type]
    )

    assert aeroplane.velocity == 0.0
    assert aeroplane.altitude == 0.0


def test_aeroplanes_comparison() -> None:
    slower = Aeroplane(
        callsign="ONE",
        origin_country="Finland",
        velocity=100,
        altitude=5000,
    )
    faster = Aeroplane(
        callsign="TWO",
        origin_country="Finland",
        velocity=200,
        altitude=6000,
    )

    assert slower < faster
    assert not faster < slower


def test_aeroplanes_equality() -> None:
    first = Aeroplane(
        callsign="ONE",
        origin_country="Finland",
        velocity=200,
        altitude=6000,
    )
    second = Aeroplane(
        callsign="TWO",
        origin_country="Germany",
        velocity=200,
        altitude=6000,
    )

    assert first == second


def test_string_representation() -> None:
    aeroplane = Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=250,
        altitude=10000,
    )

    result = str(aeroplane)

    assert "FIN123" in result
    assert "Finland" in result
    assert "250.00" in result
    assert "10000.00" in result


def test_repr() -> None:
    aeroplane = Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=250,
        altitude=10000,
    )

    result = repr(aeroplane)

    assert "Aeroplane" in result
    assert "FIN123" in result


def test_from_opensky_state() -> None:
    state = [
        "icao24",
        " FIN123 ",
        "Finland",
        None,
        None,
        24.9,
        60.1,
        10000.0,
        False,
        250.0,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]

    aeroplane = Aeroplane.from_opensky_state(state)

    assert aeroplane.callsign == "FIN123"
    assert aeroplane.origin_country == "Finland"
    assert aeroplane.velocity == 250.0
    assert aeroplane.altitude == 10000.0


def test_from_opensky_state_with_missing_values() -> None:
    state = [
        "icao24",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        False,
        None,
        None,
        None,
        None,
        None,
    ]

    aeroplane = Aeroplane.from_opensky_state(state)

    assert aeroplane.callsign == "Неизвестно"
    assert aeroplane.origin_country == "Неизвестно"
    assert aeroplane.velocity == 0.0
    assert aeroplane.altitude == 0.0


def test_from_opensky_state_invalid_data() -> None:
    with pytest.raises(ValueError):
        Aeroplane.from_opensky_state(["too", "short"])


def test_cast_to_object_list() -> None:
    valid_state = [
        "icao24",
        "FIN123",
        "Finland",
        None,
        None,
        24.9,
        60.1,
        10000.0,
        False,
        250.0,
        None,
        None,
        None,
        None,
    ]

    invalid_state = ["invalid"]

    result = Aeroplane.cast_to_object_list(
        [
            valid_state,
            invalid_state,
        ]
    )

    assert len(result) == 1
    assert result[0].callsign == "FIN123"


def test_to_dict() -> None:
    aeroplane = Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=250,
        altitude=10000,
        longitude=24.9,
        latitude=60.1,
    )

    assert aeroplane.to_dict() == {
        "callsign": "FIN123",
        "origin_country": "Finland",
        "velocity": 250.0,
        "altitude": 10000.0,
        "longitude": 24.9,
        "latitude": 60.1,
    }
