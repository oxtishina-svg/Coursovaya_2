from src.aeroplane import Aeroplane
from src.api import AeroplanesAPI
from src.storage import JSONSaver
from src.utils import filter_aeroplanes_by_country, get_top_aeroplanes, parse_top_n


def print_aeroplanes(
    aeroplanes: list[Aeroplane],
) -> None:
    """Выводит самолёты в человекочитаемом виде."""

    if not aeroplanes:
        print("Самолёты не найдены.")
        return

    for index, aeroplane in enumerate(
        aeroplanes,
        start=1,
    ):
        print(
            f"{index}. "
            f"{aeroplane.callsign} | "
            f"{aeroplane.origin_country} | "
            f"скорость: {aeroplane.velocity:.2f} м/с | "
            f"высота: {aeroplane.altitude:.2f} м"
        )


def save_aeroplanes(
    saver: JSONSaver,
    aeroplanes: list[Aeroplane],
) -> None:
    """Сохраняет самолёты в JSON-файл."""

    for aeroplane in aeroplanes:
        saver.add_aeroplane(aeroplane)


def user_interaction() -> None:
    """Запускает взаимодействие с пользователем через консоль."""

    api = AeroplanesAPI()
    saver = JSONSaver()

    country = input("Введите название страны для поиска самолётов: ").strip()

    if not country:
        print("Название страны не может быть пустым.")
        return

    try:
        states = api.get_aeroplanes(country)
    except (ConnectionError, ValueError) as error:
        print(f"Ошибка: {error}")
        return

    aeroplanes = Aeroplane.cast_to_object_list(states)

    if not aeroplanes:
        print("В воздушном пространстве выбранной страны " "самолёты не найдены.")
        return

    save_aeroplanes(
        saver,
        aeroplanes,
    )

    print(f"\nПолучено самолётов: {len(aeroplanes)}")

    top_n_input = input("Введите количество самолётов для top N по высоте: ")

    try:
        top_n = parse_top_n(top_n_input)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    top_aeroplanes = get_top_aeroplanes(
        aeroplanes,
        top_n,
    )

    print(f"\nTop {top_n} самолётов по высоте:")
    print_aeroplanes(top_aeroplanes)

    filter_input = input(
        "\nВведите страны регистрации для фильтрации " "через запятую или оставьте строку пустой: "
    ).strip()

    if filter_input:
        countries = [country_name.strip() for country_name in filter_input.split(",") if country_name.strip()]

        filtered_aeroplanes = filter_aeroplanes_by_country(
            aeroplanes,
            countries,
        )

        print("\nСамолёты после фильтрации:")
        print_aeroplanes(filtered_aeroplanes)

    print("\nДанные сохранены в data/aeroplanes.json")


if __name__ == "__main__":
    user_interaction()
