from src.aeroplane import Aeroplane


def filter_aeroplanes_by_country(
    aeroplanes: list[Aeroplane],
    countries: list[str],
) -> list[Aeroplane]:
    """Фильтрует самолёты по стране регистрации."""

    normalized_countries = {country.strip().lower() for country in countries if country.strip()}

    if not normalized_countries:
        return aeroplanes

    return [aeroplane for aeroplane in aeroplanes if aeroplane.origin_country.lower() in normalized_countries]


def sort_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane],
) -> list[Aeroplane]:
    """Сортирует самолёты по высоте по убыванию."""

    return sorted(
        aeroplanes,
        key=lambda aeroplane: aeroplane.altitude,
        reverse=True,
    )


def get_top_aeroplanes(
    aeroplanes: list[Aeroplane],
    top_n: int,
) -> list[Aeroplane]:
    """Возвращает top N самолётов по высоте."""

    if top_n <= 0:
        raise ValueError("Количество самолётов должно быть больше нуля.")

    sorted_aeroplanes = sort_aeroplanes_by_altitude(aeroplanes)

    return sorted_aeroplanes[:top_n]


def parse_top_n(value: str) -> int:
    """Преобразует пользовательский ввод в положительное число."""

    try:
        top_n = int(value)
    except ValueError as error:
        raise ValueError("Введите целое число.") from error

    if top_n <= 0:
        raise ValueError("Количество самолётов должно быть больше нуля.")

    return top_n
