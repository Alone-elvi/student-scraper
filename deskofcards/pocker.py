from api.deskofcards import init_game, draw_cards

CARD_VALUE = ("2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A")
CARD_SUIT = ("S", "H", "D", "C")


def is_pared(cards):
    values = [x.get("code")[0] for x in cards]
    suites = [x.get("code")[1] for x in cards]

    print([suites.count(suit) for suit in CARD_SUIT])
    print([values.count(value) for value in CARD_VALUE])

    if 2 in [suites.count(suit) for suit in CARD_SUIT] or 2 in [
        values.count(value) for value in CARD_VALUE
    ]:
        return True
    return False

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
        print("PARED")
    print(one_hand, second_hand)
