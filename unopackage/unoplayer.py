# should the hand be ordered? or keep it unordered?
class UnoPlayer:
    def __init__(self, name):
        self.__name__ = name
        self.__hand__ = []

    def get_name(self):
        return self.__name__

    def count_cards(self):
        return len(self.__hand__)

    def get_all_cards(self):
        return self.__hand__.copy()

    def get_placeable_card_indexes(self, top_color, top_value):
        idxs = []
        for i in range(self.count_cards()):
            card = self.__hand__[i]
            if card.placeable(top_color, top_value):
                idxs.append(i)
        return idxs

    def add_card(self, card):
        self.__hand__.append(card)

    def get_card(self, idx):
        if idx < 0 or idx >= self.count_cards():
            return None
        return self.__hand__[idx]

    def pop_card(self, idx):
        if idx < 0 or idx >= self.count_cards():
            return None
        return self.__hand__.pop(idx)
