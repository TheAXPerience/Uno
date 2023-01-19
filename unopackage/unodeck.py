from .unocards import CardColor, CardValue, UnoCard
import random


# represents a deck of Uno cards
class UnoDeck:
    def __init__(self):
        self.__deck__ = []

    # checks if the deck is empty
    def is_empty(self):
        return len(self.__deck__) == 0

    # draws a card from the deck
    def draw_card(self):
        if self.is_empty():
            return None
        return self.__deck__.pop()

    # shuffles the deck
    def shuffle(self):
        random.shuffle(self.__deck__)

    # adds cards to the deck
    def refill(self, newcards):
        self.__deck__.extend(newcards)


# represents the center pile of Uno cards
class UnoPile:
    def __init__(self):
        self.__top_color__ = CardColor.NONE
        self.__top_value__ = CardValue.NONE
        self.__cards__ = []

    # returns the color of the top card
    def get_top_color(self):
        return self.__top_color__

    # returns the value of the top card
    def get_top_value(self):
        return self.__top_value__

    # checks if a card can be placed on the pile
    def placeable(self, card):
        if card is None:
            return False
        return card.placeable(self.__top_color__, self.__top_value__)

    # places a card on top of the pile
    def place_card(self, card, color, value):
        if card is not None:
            self.__top_value__ = value
            self.__top_color__ = color
            self.__cards__.append(card)

    # removes all but the top card of the pile and returns the rest
    def get_discards(self):
        if len(self.__cards__) < 2:
            return []
        ret = self.__cards__[:-1]
        self.__cards__[:-1] = []
        return ret


# builds a default Uno deck
def build_deck():
    deck = []
    # colors
    for i in range(1, 5):
        # values
        for j in range(1, 14):
            deck.append(UnoCard(CardColor(i), CardValue(j)))
            deck.append(UnoCard(CardColor(i), CardValue(j)))

        deck.append(UnoCard(CardColor.NONE, CardValue.WILD))
        deck.append(UnoCard(CardColor.NONE, CardValue.WILD_DRAW_4))

    unodeck = UnoDeck()
    unodeck.refill(deck)
    return unodeck
