from Deck import Deck
from Player import Player
from GeneralStrategy import GeneralStrategy

class Game:

    def __init__(self, num_players=8, bb=2, sb=1, ante=0):
        self.deck = Deck()
        self.community_cards = []
        self.players = []
        self.players_in_order = []
        self.first_round_order = []
        self.bb = bb
        self.sb = sb
        self.ante = ante
        self.pot = 0
        self.num_players = num_players
        self.largest_bet = 0
        self.active_players_after_deal = []
        self.active_players_after_flop = []
        self.active_players_after_turn = []
        self.active_players_after_river = []
        self.current_call = 0

        for i in range(0, num_players):
            self.players.append(Player())

    def deal_flop(self):
        for i in range(3):
            self.community_cards.append(self.deck.pop_top_card())

    def deal_turn(self):
        self.community_cards.append(self.deck.pop_top_card())

    def deal_river(self):
        self.community_cards.append(self.deck.pop_top_card())

    def set_initial_positions(self):
        for i in range(self.num_players):
            self.players[i].set_position(i)

    def increment_positions(self):
        for player in self.players:
            player.increment_position(self.num_players)

    def add_chips_pot(self, player, num_chips):
        self.pot += player.put_chips_pot(num_chips)

    def add_chips_pot(self, num_chips):
        self.pot += num_chips

    """
    Order of players: sb = 0, bb = 1, etc. button = num_players-1
    """
    # FIXME: faster way to do this?
    def get_players_in_order(self):
        self.players_in_order.clear()
        for i in range(self.num_players):
            for player in self.players:
                if player.get_position() == i:
                    self.players_in_order.append(player)

    def set_first_round_order(self):
        self.first_round_order.clear()
        for i in range(2, self.num_players):
            for player in self.players:
                if player.get_position() == i:
                    self.first_round_order.append(player)

        self.first_round_order.append(self.players_in_order[0])
        self.first_round_order.append(self.players_in_order[1])

    # call only after getting players in order
    def blinds_in_pot(self):
        self.players_in_order[0].put_chips_pot(self.sb)
        self.players_in_order[1].put_chips_pot(self.bb)

    # call only after getting players in order
    def deal_hole_cards(self):
        for player in self.players_in_order:
            player.get_dealt_card(self.deck.pop_top_card())

    # clear active player lists
    def clear_active_players(self):
        self.active_players_after_deal.clear()
        self.active_players_after_flop.clear()
        self.active_players_after_turn.clear()
        self.active_players_after_river.clear()

    # first round of betting
    def execute_deal_betting_round(self):
        for player in self.first_round_order:
            bet = player.execute_strategy(self.pot, self.current_call)
            if bet > 0:
                self.add_chips_pot(bet)
                self.active_players_after_deal.append(player)
                if bet > self.current_call:
                    self.current_call = bet

    # second round of betting
    def execute_flop_betting_round(self):
        for player in self.active_players_after_deal:
            bet = player.execute_strategy(self.pot, self.current_call)
            if bet > 0:
                self.add_chips_pot(bet)
                self.active_players_after_flop.append(player)
                if bet > self.current_call:
                    self.current_call = bet

    # third round of betting
    def execute_turn_betting_round(self):
        for player in self.active_players_after_flop:
            bet = player.execute_strategy(self.pot, self.current_call)
            if bet > 0:
                self.add_chips_pot(bet)
                self.active_players_after_turn.append(player)
                if bet > self.current_call:
                    self.current_call = bet

    # fourth round of betting
    def execute_river_betting_round(self):
        for player in self.active_players_after_turn:
            bet = player.execute_strategy(self.pot, self.current_call)
            if bet > 0:
                self.add_chips_pot(bet)
                self.active_players_after_river.append(player)
                if bet > self.current_call:
                    self.current_call = bet

    # one round of betting
    def execute__betting_round(self, players_this_round, players_next_round):
        for player in players_this_round:
            bet = player.execute_strategy(self.pot, self.current_call)
            if bet > 0:
                self.add_chips_pot(bet)
                players_next_round.append(player)
                if bet > self.current_call:
                    self.current_call = bet

    # finish round if only 1 active player remaining
    def one_player_remaining(self, active_players):
        if len(active_players) == 0:
            raise ValueError("Should always have at least 1 active player at end of round!")

        if len(active_players) == 1:
            active_players[0].add_chips(self.pot)
            self.pot = 0
            return True

        return False

    # determine who has best hand
    def showdown(self, active_players):
        if len(active_players) < 2:
            raise ValueError("Need at least 2 players for a showdown!")

        best_hands = []

        # get players with best hand rankings
        for player in active_players:
            hand = GeneralStrategy.determine_hand(player.get_hole_cards(), self.community_cards)
            if len(best_hands) == 0:
                best_hands.append((player, hand))
            elif hand[0] > best_hands[0][1][0]:
                best_hands.clear()
                best_hands.append((player, hand))
            elif hand[0] == best_hands[0][1][0]:
                best_hands.append((player, hand))

        winning_players = []
        if len(best_hands) == 1:
            winning_players.append(best_hands[0])
        # adjust for hands of same rank but different kickers
        else:
            # straight flush
            if best_hands[0][1][0] == 9:
                best_hands.sort(key=lambda k: (k[1][1][0]), reverse=True)
                winning_players.append(best_hands[0][0])
                first_card = best_hands[1][1][0]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_card:
                        winning_players.append(hand[0])

            # 4 kind
            elif best_hands[0][1][0] == 8:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][4]),reverse=True)
                winning_players.append(best_hands[0][0])
                first_card = best_hands[1][1][0]
                fifth_card = best_hands[1][1][4]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_card and hand[1][1][4] == fifth_card:
                        winning_players.append(hand[0])

            # full house
            elif best_hands[0][1][0] == 7:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][3]), reverse=True)
                winning_players.append(best_hands[0][0])
                best_triplet = best_hands[1][1][0]
                best_pair = best_hands[1][1][3]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == best_triplet and hand[1][1][3] == best_pair:
                        winning_players.append(hand[0])

            # flush or high card (algorithm is same for determining winners in each)
            elif best_hands[0][1][0] == 6 or best_hands[0][1][0] == 1:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][1], k[1][1][2], k[1][1][3], k[1][1][4]), reverse=True)
                winning_players.append(best_hands[0][0])
                first_card = best_hands[1][1][0]
                second_card = best_hands[1][1][1]
                third_card = best_hands[1][1][2]
                fourth_card = best_hands[1][1][3]
                fifth_card = best_hands[1][1][4]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_card and hand[1][1][1] == second_card and hand[1][1][2] == third_card and hand[1][1][3] == fourth_card and hand[1][1][4] == fifth_card:
                        winning_players.append(hand[0])


            # straight
            elif best_hands[0][1][0] == 5:
                best_hands.sort(key=lambda k: (k[1][1][0]), reverse=True)
                winning_players.append(best_hands[0][0])
                first_card = best_hands[1][1][0]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_card:
                        winning_players.append(hand[0])

            # 3 kind
            elif best_hands[0][1][0] == 4:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][3], k[1][1][4]), reverse=True)
                winning_players.append(best_hands[0][0])
                first_card = best_hands[1][1][0]
                first_kicker = best_hands[1][1][3]
                second_kicker = best_hands[1][1][4]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_card and hand[1][1][3] == first_kicker and hand[1][1][4] == second_kicker:
                        winning_players.append(hand[0])

            # 2 pair
            elif best_hands[0][1][0] == 3:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][2], k[1][1][4]), reverse=True)
                winning_players.append(best_hands[0][0])
                first_pair = best_hands[1][1][0]
                second_pair = best_hands[1][1][2]
                kicker = best_hands[1][1][4]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == first_pair and hand[1][1][2] == second_pair and hand[1][1][4] == kicker:
                        winning_players.append(hand[0])

            # pair
            elif best_hands[0][1][0] == 2:
                best_hands.sort(key=lambda k: (k[1][1][0], k[1][1][2], k[1][1][3], k[1][1][4]), reverse=True)
                winning_players.append(best_hands[0][0])
                pair = best_hands[1][1][0]
                first_kicker = best_hands[1][1][2]
                second_kicker = best_hands[1][1][2]
                third_kicker = best_hands[1][1][4]
                for hand in best_hands[1:]:
                    if hand[1][1][0] == pair and hand[1][1][2] == first_kicker and hand[1][1][3] == second_kicker and hand[1][1][4] == third_kicker:
                        winning_players.append(hand[0])

        # distribute pot among winning players
        for player in winning_players:
            player.add_chips(self.pot/len(winning_players))

        self.pot = 0





    def cards_to_deck(self):
        for card in self.community_cards:
            self.deck.receive_card(card)

        self.community_cards.clear()

        for player in self.players:
            for card in player.hole_cards:
                self.deck.receive_card(card)
            player.hole_cards.clear()

    # execute round of poker
    def execute_round(self):

        # shuffle cards
        self.deck.shuffle()

        # clear active player list
        self.clear_active_players()

        # get players in order
        self.get_players_in_order()

        # take blinds from bb, sb into pot
        self.blinds_in_pot()

        # deal cards to players
        self.deal_hole_cards()

        # betting rounds
        for i in range(4):
            if i == 0:
                self.execute__betting_round(self.first_round_order, self.active_players_after_deal)
                if self.one_player_remaining(self.active_players_after_deal):
                    break

                self.deal_flop()
            elif i == 1:
                self.execute__betting_round(self.active_players_after_deal, self.active_players_after_flop)
                if self.one_player_remaining(self.active_players_after_flop):
                    break

                self.deal_turn()
            elif i == 2:
                self.execute__betting_round(self.active_players_after_flop, self.active_players_after_turn)
                if self.one_player_remaining(self.active_players_after_turn):
                    break

                self.deal_river()
            elif i == 3:
                self.execute__betting_round(self.active_players_after_turn, self.active_players_after_river)
                if self.one_player_remaining(self.active_players_after_river):
                    break

                # showdown
                self.showdown()

        # add cards back to deck
        self.cards_to_deck()