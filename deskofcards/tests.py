import unittest
from io import StringIO
from unittest.mock import patch
from pocker import print_cards, print_hands_ranking

class PrintCardsTestCase(unittest.TestCase):
    def test_print_cards(self):
        cards = [
            {"code": "2S"},
            {"code": "3H"},
            {"code": "4D"},
            {"code": "5C"}
        ]
        combination = "PAIR"
        hand = 0

        expected_output = "1 2S\n2 3H\n3 4D\n4 5C\nPlayer:  1\nCombinations:  PAIR\n"

        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            print_cards(cards, combination, hand)
            self.assertEqual(fake_stdout.getvalue(), expected_output)

class TestPrintHandsRanking(unittest.TestCase):
    def test_print_hands_ranking_with_valid_move_hand(self):
        move_hand = {"cards": ["A", "K", "Q", "J", "10"]}
        expected_output = "Player: 1 Score: 10"

        with patch("pocker.hands_ranking") as mock_hands_ranking, \
             patch("pocker.print_cards") as mock_print_cards, \
             patch("pocker.counting_score") as mock_counting_score:

            mock_hands_ranking.return_value = {"COMBINATIONS": "Royal Flush"}
            mock_counting_score.return_value = 10

            print_hands_ranking(move_hand, hand=0)

            mock_hands_ranking.assert_called_once_with(move_hand["cards"])
            mock_print_cards.assert_called_once_with(move_hand["cards"], "Royal Flush", 0)
            mock_counting_score.assert_called_once_with(move_hand["cards"])
            self.assertEqual(expected_output, self.output.getvalue().strip())

    def test_print_hands_ranking_with_invalid_move_hand(self):
        move_hand = {"cards": []}
        expected_output = "Player: 1 Score: 0"

        with patch("pocker.hands_ranking") as mock_hands_ranking, \
             patch("pocker.print_cards") as mock_print_cards, \
             patch("pocker.counting_score") as mock_counting_score:

            mock_hands_ranking.return_value = None
            mock_counting_score.return_value = 0

            print_hands_ranking(move_hand, hand=0)

            mock_hands_ranking.assert_called_once_with(move_hand["cards"])
            mock_print_cards.assert_called_once_with(move_hand["cards"], "NONE", 0)
            mock_counting_score.assert_called_once_with(move_hand["cards"])
            self.assertEqual(expected_output, self.output.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
