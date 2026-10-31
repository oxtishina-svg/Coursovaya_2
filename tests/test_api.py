from unittest.mock import Mock, patch

import pytest
import requests

from src.api import AeroplanesAPI


def test_get_country_coordinates() -> None:
    api = AeroplanesAPI()

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = [
        {
            "boundingbox": [
                "59.0",
                "70.0",
                "20.0",
                "32.0",
            ]
        }
    ]

    with patch.object(
        api.session,
        "get",
        return_value=response,
    ):
        result = api.get_country_coordinates("Finland")

    assert result == [
        "59.0",
        "70.0",
        "20.0",
        "32.0",
    ]


def test_get_country_coordinates_empty_response() -> None:
    api = AeroplanesAPI()

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = []

    with patch.object(
        api.session,
        "get",
        return_value=response,
    ):
        with pytest.raises(
            ValueError,
            match="не найдена",
        ):
            api.get_country_coordinates("UnknownCountry")


def test_get_country_coordinates_invalid_box() -> None:
    api = AeroplanesAPI()

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = [
        {
            "boundingbox": [
                "59.0",
                "70.0",
            ]
        }
    ]

    with patch.object(
        api.session,
        "get",
        return_value=response,
    ):
        with pytest.raises(
            ValueError,
            match="корректные координаты",
        ):
            api.get_country_coordinates("Finland")


def test_get_country_coordinates_request_error() -> None:
    api = AeroplanesAPI()

    with patch.object(
        api.session,
        "get",
        side_effect=requests.RequestException,
    ):
        with pytest.raises(
            ConnectionError,
            match="координаты",
        ):
            api.get_country_coordinates("Finland")


def test_get_aeroplanes() -> None:
    api = AeroplanesAPI()

    coordinates = [
        "59.0",
        "70.0",
        "20.0",
        "32.0",
    ]

    states = [
        [
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
    ]

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "states": states,
    }

    with (
        patch.object(
            api,
            "get_country_coordinates",
            return_value=coordinates,
        ),
        patch.object(
            api.session,
            "get",
            return_value=response,
        ),
    ):
        result = api.get_aeroplanes("Finland")

    assert result == states


def test_get_aeroplanes_without_states() -> None:
    api = AeroplanesAPI()

    coordinates = [
        "59.0",
        "70.0",
        "20.0",
        "32.0",
    ]

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "states": None,
    }

    with (
        patch.object(
            api,
            "get_country_coordinates",
            return_value=coordinates,
        ),
        patch.object(
            api.session,
            "get",
            return_value=response,
        ),
    ):
        result = api.get_aeroplanes("Finland")

    assert result == []


def test_get_aeroplanes_request_error() -> None:
    api = AeroplanesAPI()

    coordinates = [
        "59.0",
        "70.0",
        "20.0",
        "32.0",
    ]

    with (
        patch.object(
            api,
            "get_country_coordinates",
            return_value=coordinates,
        ),
        patch.object(
            api.session,
            "get",
            side_effect=requests.RequestException,
        ),
    ):
        with pytest.raises(
            ConnectionError,
            match="самолётах",
        ):
            api.get_aeroplanes("Finland")
