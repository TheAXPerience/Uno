import random

# should the hand be ordered? or keep it unordered?


class UnoPlayer:
    def __init__(self, name, cpu=False):
        self.__name__ = name
        self.__hand__ = []
        self.__is_cpu__ = cpu

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

    def set_as_cpu(self):
        self.__is_cpu__ = True

    def is_cpu(self):
        return self.__is_cpu__

    def cpu_choose_card(self, top_color, top_value):
        ret = "draw"
        indices = self.get_placeable_card_indexes(top_color, top_value)
        if len(indices) > 0:
            ret = random.choice(indices)
        return ret
