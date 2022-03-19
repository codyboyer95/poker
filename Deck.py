import random
from Card import Card

class Deck:
    def __init__(self):
        self.cards = []
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
        suits = ["s", "h", "c", "d"]
        for v in values:
            for s in suits:
                self.cards.append(Card(self, v, s))

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_top_card(self):
        return self.cards.pop(0)

    def receive_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        value = card.numeric_val
        suit = card.suit
        for c in self.cards:
            if c.numeric_val == value and c.suit == suit:
                self.cards.remove(c)