from .unocards import UnoCard, CardColor, CardValue
from .unodeck import build_deck, UnoDeck, UnoPile


def test_build_deck():
    deck = build_deck()
    i = 0
    for color in [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]:
        for value in [CardValue.ZERO, CardValue.ONE, CardValue.TWO, CardValue.THREE, CardValue.FOUR, CardValue.FIVE, CardValue.SIX, CardValue.SEVEN, CardValue.EIGHT, CardValue.NINE, CardValue.DRAW_TWO, CardValue.SKIP, CardValue.REVERSE]:
            c, v = deck.__deck__[i].color, deck.__deck__[i].value
            assert color == c
            assert value == v
            i += 1

            c, v = deck.__deck__[i].color, deck.__deck__[i].value
            assert color == c
            assert value == v
            i += 1

        assert deck.__deck__[i].value == CardValue.WILD
        i += 1

        assert deck.__deck__[i].value == CardValue.WILD_DRAW_4
        i += 1


def test_deck_empty():
    deck = UnoDeck()
    assert deck.is_empty()


def test_deck_draw_empty():
    deck = UnoDeck()
    assert not deck.draw_card()


def test_deck_refill():
    deck = UnoDeck()
    deck.refill([UnoCard(CardColor.RED, CardValue.ZERO)])

    assert not deck.is_empty()

    card = deck.draw_card()
    assert card
    assert card.value == CardValue.ZERO
    assert card.color == CardColor.RED
    assert deck.is_empty()


def test_empty_pile():
    pile = UnoPile()
    assert pile.get_top_color() == CardColor.NONE
    assert pile.get_top_value() == CardValue.NONE
    assert len(pile.get_discards()) == 0


def test_pile_place_card():
    pile = UnoPile()
    pile.place_card(UnoCard(CardColor.RED, CardValue.ZERO),
                    CardColor.RED, CardValue.ZERO)
    assert pile.get_top_color() == CardColor.RED
    assert pile.get_top_value() == CardValue.ZERO
    assert len(pile.get_discards()) == 0


def test_pile_placeable():
    pile = UnoPile()
    pile.place_card(UnoCard(CardColor.RED, CardValue.ZERO),
                    CardColor.RED, CardValue.ZERO)

    assert pile.placeable(UnoCard(CardColor.RED, CardValue.ZERO))
    assert pile.placeable(UnoCard(CardColor.RED, CardValue.ONE))
    assert pile.placeable(UnoCard(CardColor.BLUE, CardValue.ZERO))
    assert not pile.placeable(UnoCard(CardColor.GREEN, CardValue.THREE))
    assert pile.placeable(UnoCard(CardColor.NONE, CardValue.WILD))


def test_discards():
    pile = UnoPile()
    card1 = UnoCard(CardColor.RED, CardValue.ZERO)
    card2 = UnoCard(CardColor.BLUE, CardValue.ZERO)
    card3 = UnoCard(CardColor.BLUE, CardValue.THREE)

    pile.place_card(card1, card1.color, card1.value)
    pile.place_card(card2, card2.color, card2.value)
    pile.place_card(card3, card3.color, card3.value)

    assert len(pile.__cards__) == 3
    discards = pile.get_discards()
    assert len(pile.__cards__) == 1
    assert len(discards) == 2
    assert pile.get_top_color() == CardColor.BLUE
    assert pile.get_top_value() == CardValue.THREE

    assert discards[0] is card1
    assert discards[1] is card2
    assert pile.__cards__[0] is card3
