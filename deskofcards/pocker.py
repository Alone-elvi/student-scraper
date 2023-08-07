from api.deskofcards import init_game, draw_cards
from collections import Counter

CARD_VALUE = ("2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A")
CARD_RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

CARD_SUIT = ("S", "H", "D", "C")


def print_cards(cards: list, combination=None, hand: int = 0) -> None:
    """
    Print the cards and the hand number.

    Args:
        cards (list): A list of cards.
        hand (int): The hand number.

    Returns:
        None
    """
    for id, card in enumerate(cards):
        if card["code"][0] == "0":
            print(id + 1, "1" + card["code"])
        else:
            print(id + 1, card["code"])

    print("Player: ", hand + 1)
    print("Combinations: ", combination)
    return None


def print_hands_ranking(move_hand: dict, hand: int = 0) -> None:
    hands_rank = hands_ranking(move_hand["cards"])
    if hands_rank:
        print_cards(move_hand["cards"], hands_rank["COMBINATIONS"], hand)
    else:
        print_cards(move_hand["cards"], "NONE", hand)

    print("Player: ", hand + 1, "Score: ", counting_score(move_hand["cards"]))

    return None


def card_values(cards: list) -> list:
    """
    Returns a sorted list of card values.

    Parameters:
        cards (list): A list of dictionaries representing cards.
            Each dictionary should have a 'code' key.

    Returns:
        list: A sorted list of card values.
    """
    values = sorted(
        list(map(lambda x: x.replace("0", "10"), [x.get("code")[0] for x in cards]))
    )
    return values


def card_suites(cards: list) -> list:
    """
    Generate a list of card suites from a list of card dictionaries.

    Args:
        cards (list): A list of card dictionaries. Each dictionary represents
            a card and contains a 'code' key.
            The 'code' value is a string representing the card's code.

    Returns:
        list: A list of card suites extracted from the given list of card
            dictionaries. The suites are sorted in ascending order.
    """
    suites = sorted([x.get("code")[1] for x in cards])
    return suites


def counting_same_cards(cards: list) -> Counter:
    """
    Create a counter object that counts the occurrences of each card
      in the given list.

    Parameters:
        cards (list): A list of cards.

    Returns:
        Counter: A Counter object that contains the count of each card.
    """
    return Counter(cards)


def counting_cards(counter_values: list, result: dict) -> dict:
    """
    Counts the occurrences of values in a list and categorizes
    them into pairs, threes, and fours.

    Parameters:
        counter_values (list): A list of values to be counted.
        result (dict): A dictionary to store the categorized values.

    Returns:
        dict: A dictionary containing the categorized values.
    """
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
            if "FOUR" not in result:
                result["FOUR"] = []
            result["FOUR"].append(i[1])  #

    return result


def counting_score(cards: dict) -> int:
    """
    Calculate the score based on the given list of cards.

    Args:
        cards (dict): A dictionary representing a list of cards.
            Each card is a dictionary with a 'code' key that represents
            the card code.

    Returns:
        int: The total score calculated from the cards.
    """
    res = sum(
        [
            int(CARD_RANKS[CARD_VALUE.index(card["code"][0])])
            for card in cards
            if card["code"][0] in CARD_VALUE
        ]
    )
    return res


def counting_result(result: dict, values: list, suites: list) -> dict:
    """
    Takes a dictionary `result`, a list of `values`, and a list of `suites`
    as parameters.
    Modifies the `result` dictionary based on certain conditions.
    Returns the modified `result` dictionary if it is not empty, otherwise
    returns None.
    """
    if result:
        if "COMBINATIONS" not in result:
            result["COMBINATIONS"] = "NONE"
        if "PAIR" in result:
            if len(result["PAIR"]) == 2:
                result["TWO_PAIR"] = result["PAIR"]
                del result["PAIR"]
                result["TWO_PAIR"].append(True)  # Straight Flush
                result["COMBINATIONS"] = "2 PAIR"
            else:
                result["COMBINATIONS"] = "PAIR"

        if "THREE" in result:
            result["COMBINATIONS"] = "THREE"

        if "PAIR" in result and "THREE" in result:
            del result["PAIR"]
            del result["THREE"]
            result["FULL_HOUSE"] = True  # Flush
            result["COMBINATIONS"] = "FULL_HOUSE"

        if "STRAIGHT" in result:
            result["COMBINATIONS"] = "STRAIGHT"
        if "FLUSH" in result:
            result["COMBINATIONS"] = "FLUSH"

        if "STRAIGHT" in result and "FLUSH" in result:
            del result["STRAIGHT"]
            del result["FLUSH"]
            result["STRAIGHT_FLUSH"] = True  # Straight Flush
            result["COMBINATIONS"] = "STRAIGHT_FLUSH"
        result["CARDS"] = [[key, val] for key, val in zip(values, suites)]
        return result
    return None


def is_flush_royal(values: list, result: dict) -> dict:
    """
    Check if the given list of values represents a flush royal hand.

    Args:
        values (list): A list of card values.
        result (dict): A dictionary to store the result.

    Returns:
        dict: A dictionary with the result of the check.
    """
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
    """
    Generate the ranking of hands based on the given cards.

    Parameters:
    cards (list): A list of cards representing a hand.

    Returns:
    dict: A dictionary containing the ranking of hands based on the given cards.
          The dictionary may include the following keys:
          - 'FLUSH': True if the hand is a flush, False otherwise.
          - 'ROYAL_FLUSH': True if the hand is a royal flush, False otherwise.
          - 'STRAIGHT': True if the hand is a straight, False otherwise.
    """
    values = card_values(cards)
    suites = card_suites(cards)

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

    cards_count = counting_cards(counter_values, result)
    result_count = counting_result(cards_count, values, suites)

    return result_count


def api_get_cards(hand: int, turn: bool, desk_id: str, move_hand: dict) -> dict:
    """
    Retrieves the cards for a player in a card game.

    Args:
        hand (int): The player's hand number.
        turn (bool): Indicates if it is the player's turn.
        desk_id (str): The ID of the desk.
        move_hand (dict): The current state of the player's hand.

    Returns:
        dict: The updated state of the player's hand after making any changes.
    """
    want_change = str()
    # if not move_hand:
    #     move_hand = draw_cards(desk_id)
    if not turn:
        print_hands_ranking(move_hand, hand)
        want_change = input("How many cards do you want to change? ")
        player_hand = draw_cards(desk_id, want_change)
    elif want_change.isdigit():
        move_hand = draw_cards(desk_id, want_change)
    else:
        move_hand = draw_cards(desk_id)
        print_hands_ranking(move_hand, hand)
        want_change = input("How many cards do you want to change? ")
        player_hand = draw_cards(desk_id, want_change)

    if want_change.isdigit():
        changeing_card = []
        for card in range(int(want_change)):
            changeing_card.append(
                move_hand["cards"][int(input("Which card do you want to change? ")) - 1]
            )

        for changed_card in player_hand["cards"]:
            for id, card in enumerate(move_hand["cards"]):
                if card["code"] in [chaned["code"] for chaned in changeing_card]:
                    move_hand["cards"][id] = changed_card
                    break

    return move_hand


if __name__ == "__main__":
    desk_id = init_game()

    first_hand = {}
    second_hand = {}
    enough = "y"
    move_hand = {}

    hand = 0
    player = hand

    remaining = 52

    while remaining:
        if enough.lower() == "y":
            move_hand = api_get_cards(
                hand=hand, turn=True, desk_id=desk_id, move_hand=move_hand
            )
        else:
            move_hand = api_get_cards(
                hand=hand, turn=False, desk_id=desk_id, move_hand=move_hand
            )

        remaining = move_hand["remaining"]

        print_hands_ranking(move_hand, hand)

        move_hand["score"] = counting_score(move_hand["cards"])

        enough = input("Do you want to continue? (y/n) ")

        if hand == 0:
            first_hand = move_hand
        else:
            second_hand = move_hand

        if enough.lower() == "y":
            hand = 1 if hand == 0 else 2

        remaining = move_hand["remaining"]
