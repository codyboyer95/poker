
# values are strings: 2-10, j, q, k, a
# suits are strings: s, h, c, d
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.numeric_val = 0
        try:
            self.numeric_val = int(self.value)
        except ValueError:
            if self.value == "j":
                self.numeric_val = 11
            elif self.value == "q":
                self.numeric_val = 12
            elif self.value == "k":
                self.numeric_val = 13
            elif self.value == "a":
                self.numeric_val = 14

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def get_numeric_val(self):
        return self.numeric_val

    def get_card_as_string(self):
        return (self.value+self.suit)

    def get_card_tuple(self):
        return (self.numeric_val, self.suit)