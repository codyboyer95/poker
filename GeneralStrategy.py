import Card

class GeneralStrategy:
    @staticmethod
    def get_dict_by_value(hole_cards, comm_cards):
        temp_list = hole_cards + comm_cards

        # dict contains number of each card by value
        cards_dict = {}
        for i in range(2,15):
            # spades, hearts, clubs, diamonds
            cards_dict[i] = 0

        for card in temp_list:
            cards_dict[card.numeric_val] += 1

        return cards_dict

    @staticmethod
    def get_lists_by_suit(hole_cards, comm_cards):
        # spades, hearts, clubs, diamonds
        suit_lists = [[], [], [], []]
        temp_list = hole_cards + comm_cards
        for card in temp_list:
            if card.suit == "s":
                suit_lists[0].append(card.numeric_val)
            elif card.suit == "h":
                suit_lists[1].append(card.numeric_val)
            elif card.suit == "c":
                suit_lists[2].append(card.numeric_val)
            elif card.suit == "d":
                suit_lists[3].append(card.numeric_val)

        for i in range(0,4):
            suit_lists[i] = sorted(suit_lists[i], reverse=True)
        return suit_lists

    @staticmethod
    def determine_straight(cards_dict):
        if cards_dict[5] == 0 and cards_dict[10] == 0:
            return -1

        for i in range(14,5,-1):
            if cards_dict[i] > 0:
                for j in range(i-1,i-5,-1):
                    if cards_dict[j] > 0 and j == (i-4):
                        return i
                    elif cards_dict[j] == 0:
                        i = j
                        break

        return -1

    # return list of 5 highest cards in suit
    @staticmethod
    def determine_flush(suit_lists):
        for i in range(4):
            if len(suit_lists[i]) > 4:
                temp = []
                for j in range(5):
                    temp.append(suit_lists[i][j])
                return temp, i

        return [-1], -1

    @staticmethod
    def determine_straight_flush(suit_lists):
        (flush_val, flush_suit) = GeneralStrategy.determine_flush(suit_lists)
        if flush_val[0] != -1:
            temp_dict = {}
            for card_val in suit_lists[flush_suit]:
                temp_dict[card_val] = 1

            for i in range(14, 5, -1):
                if i in temp_dict:
                    for j in range(i - 1, i - 5, -1):
                        if j in temp_dict and j == (i - 4):
                            return i
                        elif j not in temp_dict:
                            i = j
                            break

            return -1

        return -1

    @staticmethod
    def determine_four_kind(cards_dict):
        for i in range(14,1,-1):
            if cards_dict[i] == 4:
                return i

        return -1

    @staticmethod
    def determine_three_kinds(cards_dict):
        three_kinds = []
        for i in range(14, 1, -1):
            if cards_dict[i] == 3:
                three_kinds.append(i)

        return three_kinds

    @staticmethod
    def determine_pairs(cards_dict):
        pair_vals = []
        for i in range(14, 1, -1):
            if cards_dict[i] == 2:
                pair_vals.append(i)

        # already sorted
        return pair_vals

    @staticmethod
    def determine_full_house(cards_dict):
        three_kinds = GeneralStrategy.determine_three_kinds(cards_dict)
        pair_vals = GeneralStrategy.determine_pairs(cards_dict)
        if len(three_kinds) == 0:
            return -1, -1
        elif len(three_kinds) > 1:
            return three_kinds[0], three_kinds[1]
        else:
            if len(pair_vals) == 0:
                return -1, -1

            return three_kinds[0], pair_vals[0]


    @staticmethod
    def determine_two_pair(cards_dict):
        pairs = GeneralStrategy.determine_pairs(cards_dict)
        if len(pairs) > 1:
            return pairs[0], pairs[1]

        return -1, -1

    @staticmethod
    def get_high_card_values(cards_dict):
        highest = []
        for i in range(14,1,-1):
            if cards_dict[i] > 0:
                for j in range(cards_dict[i]):
                    highest.append(i)

            if len(highest) == 5:
                return highest

        if len(highest) > 5:
            raise ValueError("Get high card values should only return 5 values!")

        return highest

    # returns tuple of: hand ranking and list of card values in best 5 card hand
    # 9 - straight flush
    # 8 - 4 of a kind
    # 7 - full house
    # 6 - flush
    # 5 - straight
    # 4 - 3 of a kind
    # 3 - 2 pair
    # 2 - pair
    # 1 - high card
    @staticmethod
    def determine_hand(hole_cards, comm_cards):

        cards_dict = GeneralStrategy.get_dict_by_value(hole_cards, comm_cards)
        suit_lists = GeneralStrategy.get_lists_by_suit(hole_cards, comm_cards)

        temp_val = GeneralStrategy.determine_straight_flush(suit_lists)
        if temp_val != -1:
            five_cards = []
            counter = 0
            for i in range(5):
                five_cards.append(temp_val - counter)
                counter -= 1
            return 9, five_cards

        temp_val = GeneralStrategy.determine_four_kind(cards_dict)
        if temp_val != -1:
            five_cards = []
            for i in range(4):
                five_cards.append(temp_val)
            for i in range(14, 1, -1):
                if i != temp_val and cards_dict[i] > 0:
                    five_cards.append(i)
                    break

            return 8, five_cards

        temp_tuple = GeneralStrategy.determine_full_house(cards_dict)
        if temp_tuple != (-1, -1):
            five_cards = []
            for i in range(3):
                five_cards.append(temp_tuple[0])
            for i in range(2):
                five_cards.append(temp_tuple[1])
            return 7, five_cards

        temp_list = GeneralStrategy.determine_flush(suit_lists)[0]
        if temp_list[0] != -1:
            return 6, temp_list

        temp_val = GeneralStrategy.determine_straight(cards_dict)
        if temp_val != -1:
            five_cards = []
            counter = 0
            for i in range(5):
                five_cards.append(temp_val - counter)
                counter -= 1
            return 5, five_cards

        temp_list = GeneralStrategy.determine_three_kinds(cards_dict)
        temp_val = temp_list[0]
        if len(temp_list) > 0:
            five_cards = []
            for i in range(3):
                five_cards.append(temp_val)
            for i in range(14, 1, -1):
                if i != temp_val and cards_dict[i] > 0:
                    five_cards.append(i)
                    if len(five_cards) == 5:
                        break

            return 4, five_cards

        temp_tuple = GeneralStrategy.determine_two_pair(cards_dict)
        if temp_tuple != (-1, -1):
            five_cards = []
            for i in range(2):
                five_cards.append(temp_tuple[0])
            for i in range(2):
                five_cards.append(temp_tuple[1])
            for i in range(14, 1, -1):
                if i != temp_tuple[0] and i != temp_tuple[1] and cards_dict[i] > 0:
                    five_cards.append(i)
                    break

            return 3, five_cards

        temp_list = GeneralStrategy.determine_pairs(cards_dict)
        if len(temp_list) > 0:
            five_cards = []
            for i in range(2):
                five_cards.append(temp_list[0])
            for i in range(14, 1, -1):
                if i != temp_list[0] and cards_dict[i] > 0:
                    five_cards.append(i)
                    if len(five_cards) == 5:
                        break

            return 2, five_cards

        return 1, GeneralStrategy.get_high_card_values(cards_dict)





