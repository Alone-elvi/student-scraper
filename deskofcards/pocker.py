from api.deskofcards import init_game, draw_cards
from collections import Counter

CARD_VALUE = ("2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A")
CARD_SUIT = ("S", "H", "D", "C")


def print_cards(cards: list) -> None:
    for id, card in enumerate(cards):
        print(id, card["code"])

    return None


def card_values(cards: list) -> list:
    values = sorted(
        list(map(lambda x: x.replace("0", "10"), [x.get("code")[0] for x in cards]))
    )
    return values


def card_suites(cards: list) -> list:
    suites = sorted([x.get("code")[1] for x in cards])
    return suites


def counting_same_cards(cards: list) -> Counter:
    return Counter(cards)


def counting_cards(counter_values: list, result: dict) -> dict:
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

    return result


def counting_result(result: dict, values: list, suites: list) -> dict:
    if result:
        if "PAIR" in result:
            if len(result["PAIR"]) == 2:
                result["TWO_PAIR"] = result["PAIR"]
                del result["PAIR"]
                result["TWO_PAIR"].append(True)  # Straight Flush
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


def is_flush_royal(values: list, result: dict) -> dict:
    straight_val = sorted(
        [CARD_VALUE.index(val) for val in values if val in CARD_VALUE]
    )
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


def hands_ranking(cards):
    values = card_values(cards)
    suites = card_suites(cards)

    # values = sorted(["J", "J", "Q", "Q", "Q"])
    # suites = ["S", "D", "S", "S"]
    result = {}

    counter_values = counting_same_cards(values)

    # Flush
    flush = set(suites)

    if len(flush) == 1 and len(suites) == 3:
        result["FLUSH"] = True

    # straight
    tmp_result = is_flush_royal(values, result)
    if tmp_result is not None:
        if "ROYAL_FLUSH" in tmp_result:
            result["ROYAL_FLUSH"] = True
        elif "STRAIGHT" in tmp_result:
            result["STRAIGHT"] = True

    # straight_val = sorted(
    #     [CARD_VALUE.index(val) for val in values if val in CARD_VALUE]
    # )

    # straight_count = 0
    # royal_flush = False

    # for id, value in enumerate(straight_val):
    #     if id == 0 and value == 8:
    #         royal_flush = True
    #     if id != 0:
    #         for prev_value in straight_val[id - 1 : id]:
    #             diff = value - prev_value
    #             if diff == 1:
    #                 straight_count += 1

    # if straight_count == 4:
    #     if royal_flush:
    #         result["ROYAL_FLUSH"] = True
    #         del result["FLUSH"]
    #     else:
    #         result["STRAIGHT"] = True

    # Royal Flush

    cards_count = counting_cards(counter_values, result)
    result_count = counting_result(cards_count, values, suites)

    print_cards(cards)
    return result_count


if __name__ == "__main__":
    desk_id = init_game()

    one_hand = draw_cards(desk_id)
    second_hand = draw_cards(desk_id)

    remaining = second_hand["remaining"]

    while remaining:
        hands_rank = hands_ranking(second_hand["cards"])
        if hands_rank:
            print(hands_rank)

        player_hand = second_hand

        want_change = input("How many cards do you want to change? ")

        second_hand = draw_cards(desk_id, want_change)

        [
            print((id + 1, card["code"]), sep="\n")
            for id, card in enumerate(player_hand["cards"])
        ]

        changeing_card = []
        for card in range(int(want_change)):
            changeing_card.append(
                player_hand["cards"][
                    int(input("Which card do you want to change? ")) - 1
                ]
            )

        for card in player_hand["cards"]:
            if card["code"] in [cange_card["code"] for cange_card in changeing_card]:
                player_hand["cards"].remove(card)

        player_hand["cards"] += second_hand["cards"]
        second_hand["cards"] = player_hand["cards"]

        remaining = second_hand["remaining"]
    # print(one_hand, second_hand)
# @TODO Сделать, чтобы после смены карт, менялся участник
