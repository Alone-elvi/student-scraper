import unittest
from io import StringIO
from unittest.mock import patch
from api.deskofcards import print_cards

class PrintCardsTestCase(unittest.TestCase):
    def test_print_cards(self):
        cards = [
            {"code": "2S"},
            {"code": "3H"},
            {"code": "4D"},
            {"code": "5C"}
        ]
        combination = "PAIR"
        hand = 1

        expected_output = "1 2S\n2 3H\n3 4D\n4 5C\nPlayer:  1\nCombinations:  PAIR\n"

        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            print_cards(cards, combination, hand)
            self.assertEqual(fake_stdout.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
