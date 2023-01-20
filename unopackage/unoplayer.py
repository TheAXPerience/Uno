from .unocards import UnoCard, CardColor, CardValue
import random


# represents a player in the game of Uno
class UnoPlayer:
    def __init__(self, name: str, cpu: bool = False):
        self.__name__ = name
        self.__hand__ = []
        self.__is_cpu__ = cpu

    # returns the player's name
    def get_name(self) -> str:
        return self.__name__

    # returns the number of cards in the player's hand
    def count_cards(self) -> int:
        return len(self.__hand__)

    # returns a list of cards in the player's hand
    def get_all_cards(self) -> list[UnoCard]:
        return self.__hand__.copy()

    # returns the indices of cards in the player's hand that can be placed with the given color and value
    def get_placeable_card_indexes(self, top_color: CardColor, top_value: CardValue) -> list[int]:
        idxs = []
        for i in range(self.count_cards()):
            card = self.__hand__[i]
            if card.placeable(top_color, top_value):
                idxs.append(i)
        return idxs

    # adds a card to the player's hand
    def add_card(self, card: UnoCard) -> None:
        self.__hand__.append(card)

    # gets a card from the player's hand
    def get_card(self, idx: int) -> UnoCard:
        if idx < 0 or idx >= self.count_cards():
            return None
        return self.__hand__[idx]

    # gets and removes a card from the player's hand
    def pop_card(self, idx: int) -> UnoCard:
        if idx < 0 or idx >= self.count_cards():
            return None
        return self.__hand__.pop(idx)

    # sets the player as a computer player
    def set_as_cpu(self) -> None:
        self.__is_cpu__ = True

    # checks if the player is a computer player
    def is_cpu(self) -> bool:
        return self.__is_cpu__

    # chooses a random, placeable card from the player's hand
    def cpu_choose_card(self, top_color: CardColor, top_value: CardValue) -> int:
        ret = -1
        indices = self.get_placeable_card_indexes(top_color, top_value)
        if len(indices) > 0:
            ret = random.choice(indices)
        return ret
