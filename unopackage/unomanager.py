from .unocards import CardColor, CardValue, UnoCard
from .unodeck import build_deck, UnoPile
from .unoplayer import UnoPlayer
import random

MIN_UNO_PLAYERS = 2
MAX_UNO_PLAYERS = 6

__RANDOM_CPU_NAMES__ = ["CPU Marge", "CPU Bart", "CPU Homer", "CPU Lisa", "CPU Maggie", "CPU Ned", "CPU Nelson",
                        "CPU Skinner", "CPU Moe", "CPU Lenny", "CPU Carl", "CPU Barney", "CPU Milhouse", "CPU Ralph", "CPU Stacey"]


# manages a game of Uno
class UnoManager:
    def __init__(self):
        # player hands
        self.__players__ = []
        # uno deck
        self.__deck__ = build_deck()
        # uno pile
        self.__pile__ = UnoPile()
        # turn order - % by num players
        self.__curr__ = 0
        # turn order increment - either 1 or -1 (reversed)
        self.__next__ = 1

    # adds a player to the game
    def add_player(self, name: str) -> None:
        self.__players__.append(UnoPlayer(name))

    # adds a computer player to the game
    def add_cpu(self) -> None:
        self.__players__.append(
            UnoPlayer(random.choice(__RANDOM_CPU_NAMES__), True))

    # returns the number of players
    def num_players(self) -> int:
        return len(self.__players__)

    # finishes setting up the game to be played
    def start_game(self) -> None:
        # shuffle the deck
        self.__deck__.shuffle()

        # give each player 7 cards
        self.__curr__, n = 0, len(self.__players__)
        while self.__curr__ < n:
            self.draw_card(7)
            self.__curr__ += 1
        self.__curr__ = 0

        # place first card on pile
        while self.__pile__.get_top_color() == CardColor.NONE:
            card = self.__deck__.draw_card()
            self.__pile__.place_card(card, card.color, card.value)

        # shuffle player order
        random.shuffle(self.__players__)

    # gets all the player's names and number of cards left
    def get_player_scores(self) -> list[tuple[str, int]]:
        ret = []
        for p in self.__players__:
            ret.append((p.get_name(), p.count_cards()))
        return ret

    # gets the current player's name
    def get_current_name(self) -> str:
        return self.__players__[self.__curr__].get_name()

    # gets the top card's color and value from the pile
    def get_top_card(self) -> tuple[CardColor, CardValue]:
        return self.__pile__.get_top_color(), self.__pile__.get_top_value()

    # places a card from the current player's hand
    def place_card(self, idx: int, uno: bool = False, color: CardColor = None) -> bool:
        # check if placeable
        if not self.is_card_placeable(idx):
            return False    # could not be placed

        # get card, remove from hand, place on pile
        card = self.__players__[self.__curr__].pop_card(idx)
        self.__pile__.place_card(
            card, color if card.is_wild() else card.color, card.value)

        # check for uno
        if self.__players__[self.__curr__].count_cards() == 1 and not uno:
            self.draw_card(4)

        # special effect depending on card
        if card.value == CardValue.SKIP:
            self.next_turn()
        elif card.value == CardValue.REVERSE:
            self.__next__ *= -1
        elif card.value == CardValue.DRAW_TWO:
            self.next_turn()
            self.draw_card(2)
        elif card.value == CardValue.WILD_DRAW_4:
            self.next_turn()
            self.draw_card(4)

        return True    # successfully placed

    # checks if the deck is empty
    def is_deck_empty(self) -> bool:
        return self.__deck__.is_empty()

    # draws a card for the current player
    def draw_card(self, n: int = 1) -> None:
        for _ in range(n):
            if self.__deck__.is_empty():
                self.__deck__.refill(self.__pile__.get_discards())

            if not self.__deck__.is_empty():
                card = self.__deck__.draw_card()
                self.__players__[self.__curr__].add_card(card)

        if self.__deck__.is_empty():
            self.__deck__.refill(self.__pile__.get_discards())

    # increments turn order
    def next_turn(self) -> None:
        self.__curr__ = (self.__curr__ + self.__next__) % self.num_players()

    # gets all of the current player's cards, and if they are placeable or not
    def get_curr_player_cards(self) -> list[tuple[UnoCard, bool]]:
        hand = self.__players__[self.__curr__].get_all_cards()
        ret = []
        for card in hand:
            ret.append((card, self.__pile__.placeable(card)))
        return ret

    # gets the current player's card at the given index
    def get_curr_player_card(self, idx: int) -> UnoCard:
        return self.__players__[self.__curr__].get_card(idx)

    # checks if the card at the given index for the current player can be placed on the pile
    def is_card_placeable(self, idx: int) -> bool:
        return self.__pile__.placeable(self.__players__[self.__curr__].get_card(idx))

    # checks if the current player a compuiter player
    def is_player_cpu(self) -> bool:
        return self.__players__[self.__curr__].is_cpu()

    # gets a computer player's card choice
    def cpu_get_card_choice(self) -> int:
        return self.__players__[self.__curr__].cpu_choose_card(self.__pile__.get_top_color(), self.__pile__.get_top_value())

    # checks if there is a winner, and returns the winner if exists
    def winner(self) -> str:
        for player in self.__players__:
            if player.count_cards() == 0:
                return player.get_name()
        return None
