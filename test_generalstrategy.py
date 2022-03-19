from Card import Card
from GeneralStrategy import GeneralStrategy

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("k", "s"))
comm_cards = []
comm_cards.append(Card("q", "s"))
comm_cards.append(Card("j", "s"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "s"))

print("straight flush: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("a", "s"))
comm_cards = []
comm_cards.append(Card("a", "c"))
comm_cards.append(Card("j", "s"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("a", "d"))

print("4 kind: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("a", "s"))
comm_cards = []
comm_cards.append(Card("a", "d"))
comm_cards.append(Card("10", "c"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "s"))

print("full house: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("2", "s"))
comm_cards = []
comm_cards.append(Card("4", "s"))
comm_cards.append(Card("j", "s"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "s"))

print("flush: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("k", "s"))
comm_cards = []
comm_cards.append(Card("q", "s"))
comm_cards.append(Card("j", "d"))
comm_cards.append(Card("10", "c"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "s"))

print("straight: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("a", "s"))
comm_cards = []
comm_cards.append(Card("a", "d"))
comm_cards.append(Card("j", "s"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "d"))
comm_cards.append(Card("8", "s"))

print("3 kind: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("a", "s"))
comm_cards = []
comm_cards.append(Card("q", "s"))
comm_cards.append(Card("q", "d"))
comm_cards.append(Card("10", "s"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "c"))

print("2 pair: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("a", "s"))
comm_cards = []
comm_cards.append(Card("2", "s"))
comm_cards.append(Card("j", "c"))
comm_cards.append(Card("4", "s"))
comm_cards.append(Card("9", "d"))
comm_cards.append(Card("8", "s"))

print("pair: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))

hole_cards = []
hole_cards.append(Card("a", "h"))
hole_cards.append(Card("2", "s"))
comm_cards = []
comm_cards.append(Card("4", "s"))
comm_cards.append(Card("j", "c"))
comm_cards.append(Card("6", "d"))
comm_cards.append(Card("9", "s"))
comm_cards.append(Card("8", "s"))

print("high card: ")
print(GeneralStrategy.determine_hand(hole_cards, comm_cards))