import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем самолётов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в хранилище."""

    @abstractmethod
    def get_aeroplanes(
        self,
        criteria: dict[str, Any] | None = None,
    ) -> list[Aeroplane]:
        """Возвращает самолёты по указанным критериям."""

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из хранилища."""


class JSONSaver(BaseStorage):
    """Класс для хранения информации о самолётах в JSON-файле."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.filename = Path(filename)
        self.filename.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.filename.exists():
            self._write_data([])

    def _read_data(self) -> list[dict[str, Any]]:
        """Читает данные из JSON-файла."""

        try:
            with self.filename.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

        if not isinstance(data, list):
            return []

        return data

    def _write_data(
        self,
        data: list[dict[str, Any]],
    ) -> None:
        """Записывает данные в JSON-файл."""

        with self.filename.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолёт в JSON-файл."""

        data = self._read_data()

        aeroplane_data = aeroplane.to_dict()

        if aeroplane_data not in data:
            data.append(aeroplane_data)

        self._write_data(data)

    def get_aeroplanes(
        self,
        criteria: dict[str, Any] | None = None,
    ) -> list[Aeroplane]:
        """Возвращает самолёты из JSON-файла."""

        data = self._read_data()

        if criteria:
            filtered_data = []

            for item in data:
                if all(item.get(key) == value for key, value in criteria.items()):
                    filtered_data.append(item)

            data = filtered_data

        aeroplanes: list[Aeroplane] = []

        for item in data:
            try:
                aeroplane = Aeroplane(
                    callsign=str(
                        item.get(
                            "callsign",
                            "Неизвестно",
                        )
                    ),
                    origin_country=str(
                        item.get(
                            "origin_country",
                            "Неизвестно",
                        )
                    ),
                    velocity=float(
                        item.get(
                            "velocity",
                            0.0,
                        )
                    ),
                    altitude=float(
                        item.get(
                            "altitude",
                            0.0,
                        )
                    ),
                    longitude=self._to_optional_float(item.get("longitude")),
                    latitude=self._to_optional_float(item.get("latitude")),
                )

            except (TypeError, ValueError):
                continue

            aeroplanes.append(aeroplane)

        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Удаляет самолёт из JSON-файла."""

        data = self._read_data()
        aeroplane_data = aeroplane.to_dict()

        updated_data = [item for item in data if item != aeroplane_data]

        self._write_data(updated_data)

    @staticmethod
    def _to_optional_float(
        value: Any,
    ) -> float | None:
        """Преобразует значение в float или None."""

        if value is None:
            return None

        return float(value)
