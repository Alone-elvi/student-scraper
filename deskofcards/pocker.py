from api.deskofcards import init_game, draw_cards
from collections import Counter

CARD_VALUE = ("2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A")
CARD_SUIT = ("S", "H", "D", "C")


def hands_ranking(cards):
    values = sorted(
        list(map(lambda x: x.replace("0", "10"), [x.get("code")[0] for x in cards]))
    )
    suites = sorted([x.get("code")[1] for x in cards])

    values = sorted(["J", "J", "Q", "Q", "Q"])
    suites = ["S", "D", "S", "S"]
    result = {}

    counter_values = Counter(values)

    straight_val = sorted(
        [CARD_VALUE.index(val) for val in values if val in CARD_VALUE]
    )

    # Flush
    flush = set(suites)

    if len(flush) == 1:
        result["FLUSH"] = True

    # straight

    straight_count = 0
    royal_flush = False
    for id, value in enumerate(straight_val):
        if id == 0 and value == 8:
            royal_flush = True
        if id != 0:
            for prev_value in straight_val[id - 1 : id]:
                diff = value - prev_value
                if diff == 1:
                    straight_count += 1

    if straight_count == 4:
        if royal_flush:
            result["ROYAL_FLUSH"] = True
            del result["FLUSH"]
        else:
            result["STRAIGHT"] = True

    # Royal Flush

    for i in enumerate(counter_values):
        if counter_values[i[1]] == 2:
            if "PAIR" not in result:
                result["PAIR"] = []
            result["PAIR"].append(i[1])  # Pair
        if counter_values[i[1]] == 3:
            if "THREE" not in result:
                result["THREE"] = []
            result["THREE"].append(i[1])  # Three
        if counter_values[i[1]] == 4:
            result["FOUR"].append(i[1])  # Four

    if result:
        if "PAIR" in result:
            if len(result["PAIR"]) == 2:
                del result["PAIR"]
                result["TWO_PAIR"] = True  # Straight Flush
        if "PAIR" in result and "THREE" in result:
            del result["PAIR"]
            del result["THREE"]
            result["FULL_HOUSE"] = True  # Flush
        if "STRAIGHT" in result and "FLUSH" in result:
            del result["STRAIGHT"]
            del result["FLUSH"]
            result["STRAIGHT_FLUSH"] = True  # Straight Flush
        result["CARDS"] = [[key, val] for key, val in zip(values, suites)]
        return result
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

    hands_rank = hands_ranking(one_hand["cards"])
    if hands_rank:
        print(hands_rank)
    # print(one_hand, second_hand)
