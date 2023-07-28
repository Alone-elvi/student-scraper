from api.deskofcards import init_game, draw_cards
from collections import Counter

CARD_VALUE = ("2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A")
CARD_SUIT = ("S", "H", "D", "C")


def is_pared(cards):
    values = sorted(
        list(
            map(lambda x: x.replace("0", "10"), [x.get("code")[0] for x in cards])
        )
    )
    suites = sorted([x.get("code")[1] for x in cards])

    # values = ['2', '2', '2', '5', '0']

    result = {"PARED": [], "THREE": []}

    pared = []

    for i in enumerate(Counter(values)):
        if Counter(values)[i[1]] == 2:
            result["PARED"].append(i[1])
        if Counter(values)[i[1]] == 3:
            result["THREE"].append(i[1])
    if pared:
        return pared
    return None


def is_three():
    pass


def is_suter():
    pass


def is_flush():
    pass


def is_flush_royal():
    pass


if __name__ == "__main__":
    desk_id = init_game()

    one_hand = draw_cards(desk_id)
    second_hand = draw_cards(desk_id)

    remaining = second_hand["remaining"]

    if is_pared(one_hand["cards"]):
        print(is_pared(one_hand["cards"]))
    # print(one_hand, second_hand)
