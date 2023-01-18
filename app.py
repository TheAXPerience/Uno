from os import system, name as osname
from colorama import Fore
from unopackage.unomanager import UnoManager, MIN_UNO_PLAYERS, MAX_UNO_PLAYERS
from unopackage.unocards import CardColor, CardValue, card_color_str, card_value_str


# this may not be the best in terms of security but its the only way I can find to do this
# just so I can hide who has what card
def clear_terminal():
    if osname == 'nt':
        # Windows
        system('cls')
    else:
        system('clear')


# sets up UnoManager to start a game
def setup_game():
    um = UnoManager()

    # Get number of players + names
    while True:
        try:
            num_players = int(input("How many players (2-6)? "))

            if num_players < MIN_UNO_PLAYERS:
                print("Too few players.\n")
            elif num_players > MAX_UNO_PLAYERS:
                print("Too many players.\n")
            else:
                break
        except (ValueError):
            print("Invalid number of players.\n")

    for i in range(num_players):
        name = input(f"Enter name for Player #{i+1}: ")
        um.add_player(name)

    return um


# converts CardColor to Fore
def card_color_to_fore_color(cc):
    if cc == CardColor.RED:
        return Fore.RED
    elif cc == CardColor.BLUE:
        return Fore.BLUE
    elif cc == CardColor.GREEN:
        return Fore.GREEN
    elif cc == CardColor.YELLOW:
        return Fore.YELLOW
    return Fore.RESET


# main game loop
def game_loop(uno_manager):
    winner = None
    message = ""
    uno_manager.start_game()
    while winner is None:
        # clear the terminal and prints a message to the players about what happened
        clear_terminal()
        if message:
            print(message)
            message = ""

        # post initial information
        #    players and number of cards left
        #    top card on the pile
        #    who is going next
        scores = uno_manager.get_player_scores()
        curr_player = uno_manager.get_current_name()
        tc, tv = uno_manager.get_top_card()

        print("Players: ", end="|")
        for name, num in scores:
            if num == 1:
                color = Fore.LIGHTRED_EX
            elif num <= 3:
                color = Fore.LIGHTYELLOW_EX
            elif num <= 5:
                color = Fore.LIGHTGREEN_EX
            elif num <= 10:
                color = Fore.LIGHTBLUE_EX
            else:
                color = Fore.RESET
            print(
                f" {Fore.MAGENTA}{name}{Fore.RESET}: {color}{num}{Fore.RESET} ", end="|")
        print("\n" + ("There are no more cards to be drawn." if uno_manager.is_deck_empty() else ""), end="")

        print(f"\n{Fore.RESET}Top Card: " +
              f"{card_color_to_fore_color(tc)}[ {card_color_str(tc)} | {card_value_str(tv)} ]")

        print(f"{Fore.RESET}\nIt is {Fore.MAGENTA}{curr_player}{Fore.RESET}'s turn!")
        input("Press Enter to continue")

        # prints the current player's hand
        # make sure to somehow indicate something cannot be played... LIGHTBLACK_EX?
        hand = uno_manager.get_curr_player_cards()
        for i in range(len(hand)):
            card, placeable = hand[i]
            color = card_color_to_fore_color(
                card.color) if placeable else Fore.LIGHTBLACK_EX
            print(f"{Fore.RESET}{i+1}. {color}{card}{Fore.RESET}")

        uno = False
        print(
            f"\nType \"{Fore.CYAN}draw{Fore.RESET}\" to draw a card, or \"{Fore.CYAN}uno{Fore.RESET}\" to declare UNO.")
        while True:
            choice = input("Choose a card: ").strip()
            if choice.lower() == "draw":
                # draw a card
                uno_manager.draw_card()
                message += f"{Fore.MAGENTA}{curr_player}{Fore.RESET} drew a card.\n"
                break
            elif choice.lower() == "uno":
                # declare UNO
                uno = True
                continue

            # choose a card to place
            try:
                choice = int(choice) - 1
                if choice < 0 or choice >= len(hand):
                    print("Card does not exist.")
                    continue
                card, placeable = hand[choice]
            except (ValueError):
                print("Invalid command.")
                continue

            # check if placeable
            if not placeable:
                print("Card cannot be placed.")
                continue

            # if wild, player chooses color
            if card.is_wild():
                while True:
                    color_choice = input(
                        f"Choose a color ({Fore.CYAN}RGBY{Fore.RESET}): ").strip().lower()
                    if color_choice.startswith("r"):
                        color_choice = CardColor.RED
                        break
                    elif color_choice.startswith("g"):
                        color_choice = CardColor.GREEN
                        break
                    elif color_choice.startswith("b"):
                        color_choice = CardColor.BLUE
                        break
                    elif color_choice.startswith("y"):
                        color_choice = CardColor.YELLOW
                        break
            else:
                color_choice = card.color

            uno_manager.place_card(choice, uno, color_choice)

            if len(hand) == 2 and uno:
                message += "UNO!!!\n"
            elif len(hand) == 2:
                message += "PENALTY! Draw 4 cards!\n"

            message += f"{Fore.MAGENTA}{curr_player}{Fore.RESET} placed a {card_color_to_fore_color(card.color)}{card}{Fore.RESET} card.\n"

            if card.value == CardValue.SKIP:
                message += f"Skipped {Fore.MAGENTA}{uno_manager.get_current_name()}{Fore.RESET}'s turn.\n"
            if card.value == CardValue.REVERSE:
                message += f"Now going the opposite direction.\n"
            if card.value == CardValue.DRAW_TWO:
                message += f"{Fore.MAGENTA}{uno_manager.get_current_name()}{Fore.RESET} drew 2 cards.\n"
            if card.value == CardValue.WILD:
                message += f"The color was changed to {card_color_to_fore_color(color_choice)}{card_color_str(color_choice)}{Fore.RESET}.\n"
            if card.value == CardValue.WILD_DRAW_4:
                message += f"The color was changed to {card_color_to_fore_color(color_choice)}{card_color_str(color_choice)}{Fore.RESET}.\n"
                message += f"{Fore.MAGENTA}{uno_manager.get_current_name()}{Fore.RESET} drew 4 cards.\n"
            break

        winner = uno_manager.winner()
        uno_manager.next_turn()

    print(f"{Fore.MAGENTA}{winner}{Fore.RESET} has won the game!")


def main():
    print(f"""Welcome to the game of {Fore.MAGENTA}Uno{Fore.RESET}!
Place cards with either the same number or same color as the one on top of the pile.
The first player to empty their hand wins.
When you're about to place a card won that would leave you with one left in your hand,
you must type out \"{Fore.CYAN}UNO{Fore.RESET}\" then press Enter beforehand or you will be penalized with 4 cards.
""")
    while True:
        game_loop(setup_game())

        playagain = input(
            f"\nWant to play again ({Fore.CYAN}Y/N{Fore.RESET})? ")
        if playagain.strip().lower().startswith("n"):
            break

    print(f"{Fore.RED}Have {Fore.GREEN}a {Fore.BLUE}great {Fore.YELLOW}day!")


if __name__ == "__main__":
    main()
