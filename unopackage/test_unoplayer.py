from .unoplayer import UnoPlayer
from .unocards import UnoCard, CardColor, CardValue


def test_empty():
    p = UnoPlayer("Bob")

    assert p.count_cards() == 0
    assert p.get_all_cards() == []
    assert p.get_card(0) is None
    assert p.pop_card(0) is None


def test_player_name():
    p1 = UnoPlayer("Alex")
    p2 = UnoPlayer("Barker")
    p3 = UnoPlayer("Caddy")

    assert p1.get_name() == "Alex"
    assert p2.get_name() == "Barker"
    assert p3.get_name() == "Caddy"


def test_add_card():
    p = UnoPlayer("Jacob")
    c = UnoCard(CardColor.RED, CardValue.ZERO)
    d = UnoCard(CardColor.RED, CardValue.ONE)

    assert p.count_cards() == 0
    p.add_card(c)

    assert p.count_cards() == 1
    assert p.get_all_cards() == [c]

    p.add_card(d)
    assert p.count_cards() == 2
    assert p.get_all_cards() == [c, d]


def test_get_card():
    p = UnoPlayer("Jacob")
    c = UnoCard(CardColor.RED, CardValue.ZERO)
    d = UnoCard(CardColor.RED, CardValue.ZERO)

    p.add_card(c)
    p.add_card(d)

    assert p.count_cards() == 2
    assert p.get_card(0) == c
    assert p.get_card(1) == d
    assert p.get_card(3) is None


def test_pop_card():
    p = UnoPlayer("Jacob")
    c = UnoCard(CardColor.RED, CardValue.ZERO)
    d = UnoCard(CardColor.RED, CardValue.ZERO)

    p.add_card(c)
    p.add_card(d)

    assert p.count_cards() == 2
    assert p.pop_card(0) == c
    assert p.pop_card(1) is None
    assert p.pop_card(0) == d


def test_get_replaceable_indexes():
    p = UnoPlayer("Bob")
    p.add_card(UnoCard(CardColor.RED, CardValue.ZERO))
    p.add_card(UnoCard(CardColor.RED, CardValue.ONE))
    p.add_card(UnoCard(CardColor.BLUE, CardValue.ZERO))
    p.add_card(UnoCard(CardColor.BLUE, CardValue.ONE))
    p.add_card(UnoCard(CardColor.NONE, CardValue.WILD))

    assert p.get_placeable_card_indexes(
        CardColor.RED, CardValue.ZERO) == [0, 1, 2, 4]
    assert p.get_placeable_card_indexes(
        CardColor.RED, CardValue.ONE) == [0, 1, 3, 4]
    assert p.get_placeable_card_indexes(
        CardColor.BLUE, CardValue.TWO) == [2, 3, 4]
    assert p.get_placeable_card_indexes(
        CardColor.GREEN, CardValue.SEVEN) == [4]
