from __future__ import annotations

from typing import Any


class Aeroplane:
    """Модель самолёта."""

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: float,
        altitude: float,
        longitude: float | None = None,
        latitude: float | None = None,
    ) -> None:
        self.callsign = self._validate_text(callsign, "Позывной")
        self.origin_country = self._validate_text(
            origin_country,
            "Страна регистрации",
        )
        self.velocity = self._validate_number(
            velocity,
            "Скорость",
        )
        self.altitude = self._validate_number(
            altitude,
            "Высота",
        )
        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def _validate_text(
        value: str,
        field_name: str,
    ) -> str:
        """Проверяет текстовое значение."""

        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой.")

        cleaned_value = value.strip()

        if not cleaned_value:
            return "Неизвестно"

        return cleaned_value

    @staticmethod
    def _validate_number(
        value: float | int | None,
        field_name: str,
    ) -> float:
        """Проверяет числовое значение."""

        if value is None:
            return 0.0

        if not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} должна быть числом.")

        return float(value)

    def __str__(self) -> str:
        return (
            f"{self.callsign} | "
            f"{self.origin_country} | "
            f"скорость: {self.velocity:.2f} м/с | "
            f"высота: {self.altitude:.2f} м"
        )

    def __repr__(self) -> str:
        return (
            "Aeroplane("
            f"callsign={self.callsign!r}, "
            f"origin_country={self.origin_country!r}, "
            f"velocity={self.velocity!r}, "
            f"altitude={self.altitude!r}"
            ")"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return (
            self.velocity,
            self.altitude,
        ) < (
            other.velocity,
            other.altitude,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return (
            self.velocity,
            self.altitude,
        ) == (
            other.velocity,
            other.altitude,
        )

    @classmethod
    def from_opensky_state(
        cls,
        state: list[Any],
    ) -> Aeroplane:
        """Создаёт самолёт из массива OpenSky."""

        if len(state) < 14:
            raise ValueError("Некорректные данные самолёта от OpenSky.")

        callsign = state[1] or "Неизвестно"
        origin_country = state[2] or "Неизвестно"
        longitude = state[5]
        latitude = state[6]
        altitude = state[7] or 0.0
        velocity = state[9] or 0.0

        return cls(
            callsign=callsign,
            origin_country=origin_country,
            velocity=velocity,
            altitude=altitude,
            longitude=longitude,
            latitude=latitude,
        )

    @classmethod
    def cast_to_object_list(
        cls,
        states: list[list[Any]],
    ) -> list[Aeroplane]:
        """Преобразует данные OpenSky в список объектов."""

        aeroplanes: list[Aeroplane] = []

        for state in states:
            try:
                aeroplane = cls.from_opensky_state(state)
            except (TypeError, ValueError):
                continue

            aeroplanes.append(aeroplane)

        return aeroplanes

    def to_dict(self) -> dict[str, str | float | None]:
        """Преобразует самолёт в словарь."""

        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
