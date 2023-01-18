from enum import Enum

# the value of a card
CardValue = Enum("CardValue", ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX",
                 "SEVEN", "EIGHT", "NINE", "DRAW_TWO", "SKIP", "REVERSE", "WILD", "WILD_DRAW_4", "NONE"])


def card_value_str(cv):
    if cv == CardValue.ZERO:
        return "0"
    elif cv == CardValue.ONE:
        return "1"
    elif cv == CardValue.TWO:
        return "2"
    elif cv == CardValue.THREE:
        return "3"
    elif cv == CardValue.FOUR:
        return "4"
    elif cv == CardValue.FIVE:
        return "5"
    elif cv == CardValue.SIX:
        return "6"
    elif cv == CardValue.SEVEN:
        return "7"
    elif cv == CardValue.EIGHT:
        return "8"
    elif cv == CardValue.NINE:
        return "9"
    elif cv == CardValue.DRAW_TWO:
        return "+2"
    elif cv == CardValue.SKIP:
        return "Skip"
    elif cv == CardValue.REVERSE:
        return "Reverse"
    elif cv == CardValue.WILD:
        return "Wild Card"
    elif cv == CardValue.WILD_DRAW_4:
        return "Wild Card +4"
    return ""


# the color of a card
CardColor = Enum("CardColor", ["RED", "BLUE", "GREEN", "YELLOW", "NONE"])


def card_color_str(cc):
    if cc == CardColor.RED:
        return "Red"
    elif cc == CardColor.BLUE:
        return "Blue"
    elif cc == CardColor.GREEN:
        return "Green"
    elif cc == CardColor.YELLOW:
        return "Yellow"
    return ""


# a card in the game of Uno
class UnoCard():
    def __init__(self, color, val):
        self.color = color
        self.value = val

    # returns True if the card is a Wild card
    def is_wild(self):
        return self.value == CardValue.WILD or self.value == CardValue.WILD_DRAW_4

    # returns True if the card can be placed on top of the given card values
    def placeable(self, top_of_pile_color, top_of_pile_value):
        return self.color == top_of_pile_color or self.value == top_of_pile_value or self.is_wild()

    # ToString method
    def __str__(self):
        color = card_color_str(self.color)
        val = card_value_str(self.value)

        if not color and "Wild" in val:
            return f"[ {val} ]"

        return f"[ {color} | {val} ]"
