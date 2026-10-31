import json
from pathlib import Path

from src.aeroplane import Aeroplane
from src.storage import JSONSaver


def make_aeroplane() -> Aeroplane:
    return Aeroplane(
        callsign="FIN123",
        origin_country="Finland",
        velocity=250,
        altitude=10000,
        longitude=24.9,
        latitude=60.1,
    )


def test_json_saver_creates_file(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "aeroplanes.json"

    JSONSaver(str(file_path))

    assert file_path.exists()

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        assert json.load(file) == []


def test_add_aeroplane(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "aeroplanes.json"
    saver = JSONSaver(str(file_path))

    saver.add_aeroplane(make_aeroplane())

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]["callsign"] == "FIN123"


def test_add_duplicate_aeroplane(
    tmp_path: Path,
) -> None:
    saver = JSONSaver(str(tmp_path / "aeroplanes.json"))

    aeroplane = make_aeroplane()

    saver.add_aeroplane(aeroplane)
    saver.add_aeroplane(aeroplane)

    result = saver.get_aeroplanes()

    assert len(result) == 1


def test_get_aeroplanes(
    tmp_path: Path,
) -> None:
    saver = JSONSaver(str(tmp_path / "aeroplanes.json"))

    saver.add_aeroplane(make_aeroplane())

    result = saver.get_aeroplanes()

    assert len(result) == 1
    assert result[0].callsign == "FIN123"
    assert result[0].origin_country == "Finland"


def test_get_aeroplanes_by_criteria(
    tmp_path: Path,
) -> None:
    saver = JSONSaver(str(tmp_path / "aeroplanes.json"))

    first = Aeroplane(
        "FIN1",
        "Finland",
        200,
        5000,
    )
    second = Aeroplane(
        "GER1",
        "Germany",
        250,
        8000,
    )

    saver.add_aeroplane(first)
    saver.add_aeroplane(second)

    result = saver.get_aeroplanes(
        {
            "origin_country": "Finland",
        }
    )

    assert len(result) == 1
    assert result[0].callsign == "FIN1"


def test_delete_aeroplane(
    tmp_path: Path,
) -> None:
    saver = JSONSaver(str(tmp_path / "aeroplanes.json"))

    aeroplane = make_aeroplane()

    saver.add_aeroplane(aeroplane)
    saver.delete_aeroplane(aeroplane)

    assert saver.get_aeroplanes() == []


def test_invalid_json_returns_empty_list(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "aeroplanes.json"

    file_path.write_text(
        "not json",
        encoding="utf-8",
    )

    saver = JSONSaver(str(file_path))

    assert saver.get_aeroplanes() == []


def test_non_list_json_returns_empty_list(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "aeroplanes.json"

    file_path.write_text(
        '{"test": "value"}',
        encoding="utf-8",
    )

    saver = JSONSaver(str(file_path))

    assert saver.get_aeroplanes() == []


def test_invalid_item_is_skipped(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "aeroplanes.json"

    data = [
        {
            "callsign": "FIN123",
            "origin_country": "Finland",
            "velocity": "not-a-number",
            "altitude": 10000,
            "longitude": None,
            "latitude": None,
        }
    ]

    file_path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    saver = JSONSaver(str(file_path))

    assert saver.get_aeroplanes() == []
