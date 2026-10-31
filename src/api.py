from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list[str]:
        """Получает bounding box страны."""

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Получает данные о самолётах в воздушном пространстве страны."""


class AeroplanesAPI(BaseAPI):
    """Класс для работы с Nominatim и OpenSky API."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "aeroplanes-api-coursework/1.0",
            }
        )

    def get_country_coordinates(self, country: str) -> list[str]:
        """Получает bounding box указанной страны."""

        params: dict[str, str | int | float] = {
            "q": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = self.session.get(
                self.NOMINATIM_URL,
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()

        except requests.RequestException as error:
            raise ConnectionError("Не удалось получить координаты страны.") from error

        if not data:
            raise ValueError(f"Страна '{country}' не найдена.")

        bounding_box = data[0].get("boundingbox")

        if not bounding_box or len(bounding_box) != 4:
            raise ValueError("API не вернул корректные координаты страны.")

        return list(bounding_box)

    def get_aeroplanes(self, country: str) -> list[list[Any]]:
        """Получает самолёты в воздушном пространстве указанной страны."""

        coordinates = self.get_country_coordinates(country)

        south = float(coordinates[0])
        north = float(coordinates[1])
        west = float(coordinates[2])
        east = float(coordinates[3])

        params: dict[str, str | int | float] = {
            "lamin": south,
            "lamax": north,
            "lomin": west,
            "lomax": east,
        }

        try:
            response = self.session.get(
                self.OPENSKY_URL,
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()

        except requests.RequestException as error:
            raise ConnectionError("Не удалось получить данные о самолётах.") from error

        states = data.get("states")

        if states is None:
            return []

        return states
