class Player:
    def __init__(self):
        self.hole_cards = []
        self.chips = 0
        self.position = 0
        self.last_bet = 0

    def get_dealt_card(self, card):
        self.hole_cards.append(card)

    def get_hole_cards(self):
        return self.hole_cards

    def clear_hole_cards(self):
        self.hole_cards.clear()

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def increment_position(self, num_players):
        self.position += 1
        self.position = self.position % num_players

    def get_chips(self):
        return self.chips

    def get_last_bet(self):
        return self.last_bet

    def add_chips(self, num_chips):
        self.chips += num_chips

    def put_chips_pot(self, num_chips):
        self.chips -= num_chips
        self.last_bet = num_chips
        return num_chips


    # FIXME: dummy function right now
    # >0: remain playing
    # 0: fold
    def execute_strategy(self, current_pot, current_call):
        return self.put_chips_pot(current_call)

