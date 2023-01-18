from .unocards import UnoCard, CardColor, CardValue, card_color_str, card_value_str


def test_make_card():
    card = UnoCard(CardColor.RED, CardValue.ZERO)
    assert card.value == CardValue.ZERO
    assert card.color == CardColor.RED


def test_is_wild():
    card1 = UnoCard(CardColor.RED, CardValue.ZERO)
    card2 = UnoCard(CardColor.NONE, CardValue.WILD)
    card3 = UnoCard(CardColor.NONE, CardValue.WILD_DRAW_4)

    assert not card1.is_wild()
    assert card2.is_wild()
    assert card3.is_wild()


def test_placeable():
    card1 = UnoCard(CardColor.RED, CardValue.ZERO)
    card2 = UnoCard(CardColor.NONE, CardValue.WILD)

    assert card1.placeable(CardColor.RED, CardValue.ZERO)
    assert card1.placeable(CardColor.BLUE, CardValue.ZERO)
    assert card1.placeable(CardColor.RED, CardValue.TWO)
    assert not card1.placeable(CardColor.YELLOW, CardValue.THREE)
    assert card2.placeable(CardColor.RED, CardValue.ZERO)


def test_to_strings():
    assert card_color_str(CardColor.RED) == "Red"
    assert card_color_str(CardColor.BLUE) == "Blue"
    assert card_color_str(CardColor.GREEN) == "Green"
    assert card_color_str(CardColor.YELLOW) == "Yellow"

    assert card_value_str(CardValue.ZERO) == "0"
    assert card_value_str(CardValue.ONE) == "1"
    assert card_value_str(CardValue.TWO) == "2"
    assert card_value_str(CardValue.THREE) == "3"
    assert card_value_str(CardValue.FOUR) == "4"
    assert card_value_str(CardValue.FIVE) == "5"
    assert card_value_str(CardValue.SIX) == "6"
    assert card_value_str(CardValue.SEVEN) == "7"
    assert card_value_str(CardValue.EIGHT) == "8"
    assert card_value_str(CardValue.NINE) == "9"
    assert card_value_str(CardValue.DRAW_TWO) == "+2"
    assert card_value_str(CardValue.SKIP) == "Skip"
    assert card_value_str(CardValue.REVERSE) == "Reverse"
    assert card_value_str(CardValue.WILD) == "Wild Card"
    assert card_value_str(CardValue.WILD_DRAW_4) == "Wild Card +4"


def test_to_string():
    card = UnoCard(CardColor.RED, CardValue.ZERO)
    card2 = UnoCard(CardColor.NONE, CardValue.WILD)

    assert str(card) == "[ Red | 0 ]"
    assert str(card2) == "[ Wild Card ]"
