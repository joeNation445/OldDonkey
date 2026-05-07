import random
from collections import Counter

BURRO_WORD = "BURRO"
OLD_MAID = "QS"


def create_deck():
    """
    Creates a standard 52-card deck and removes the Old Maid (Queen of Spades).

    Arguments:
        None

    Returns:
        list: A list of strings representing the playing cards.

    Side Effects:
        None
    """
    suits = ["H", "D", "C", "S"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [rank + suit for rank in ranks for suit in suits]
    deck.remove(OLD_MAID)
    return deck


def shuffle(deck):
    """
    Randomizes the order of the cards in the deck using the Fisher-Yates shuffle algorithm.
    Every ordering is equally likely.

    Arguments:
        deck (list): The list of cards to shuffle.

    Returns:
        None

    Side Effects:
        Mutates the 'deck' list in place by changing the order of its elements.
    """
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]


def create_player(num_player, deck):
    """
    Initializes players, deals 5 cards to each, and removes any initial pairs from their hands.

    Arguments:
        num_player (int): The number of players in the game.
        deck (list): The main deck of cards.

    Returns:
        list: A list of player dictionaries containing their name, hand, pair count, and peek status.

    Side Effects:
        Mutates the 'deck' list by popping (removing) cards to deal to the players.
    """
    players = []
    for i in range(num_player):
        hand = []
        for _ in range(5):
            if deck:
                hand.append(deck.pop())

        ranks = [card[:-1] for card in hand]
        count = Counter(ranks)
        pairs = 0
        seen = set()
        new_hand = []

        for card in hand:
            rank = card[:-1]
            if rank in seen:
                continue
            seen.add(rank)
            if count[rank] >= 2:
                pairs += count[rank] // 2
                remainder = count[rank] % 2
                kept = 0
                for c in hand:
                    if c[:-1] == rank and kept < remainder:
                        new_hand.append(c)
                        kept += 1
            else:
                new_hand.append(card)

        player = {
            "name": f"Player {i + 1}",
            "hand": new_hand,
            "pairs": pairs,
            "peek_used": False,   
        }
        players.append(player)
    return players


def draw_card(deck):
    """
    Draws a random card from the available deck.

    Arguments:
        deck (list): The main deck of cards.

    Returns:
        str or None: The drawn card string, or None if the deck is empty.

    Side Effects:
        Mutates the 'deck' list by removing the drawn card.
    """
    if len(deck) == 0:
        return None
    index = random.randint(0, len(deck) - 1)
    card = deck[index]
    deck.pop(index)
    return card


def determine_loser(players):
    """
    Identifies the player(s) with the fewest pairs at the end of the game.

    Arguments:
        players (list): A list of player dictionaries.

    Returns:
        str or list: A string of the loser's name, or a list of names if there is a tie.

    Side Effects:
        None
    """
    lowest_pairs = players[0]["pairs"]
    losers = [players[0]["name"]]
    for player in players[1:]:
        if player["pairs"] < lowest_pairs:
            lowest_pairs = player["pairs"]
            losers = [player["name"]]
        elif player["pairs"] == lowest_pairs:
            losers.append(player["name"])
    if len(losers) == 1:
        return losers[0]
    else:
        return losers


def player_turn(current_player, players, deck):
    """
    Handles one standard player's turn: draws a card, checks for a pair, and removes it if found.

    Arguments:
        current_player (dict): The dictionary of the player taking the turn.
        players (list): A list of all player dictionaries.
        deck (list): The main deck of cards.

    Returns:
        tuple: A tuple containing the updated (current_player, players, deck).

    Side Effects:
        Mutates the 'deck' list by removing a card.
        Mutates the 'current_player' dictionary by updating their hand and pairs count.
    """
    drawn = draw_card(deck)
    if drawn is None:
        return current_player, players, deck

    drawn_rank = drawn[:-1]

    match = None
    for card in current_player["hand"]:
        if card[:-1] == drawn_rank:
            match = card
            break

    if match:
        current_player["hand"].remove(match)
        current_player["pairs"] += 1
    else:
        current_player["hand"].append(drawn)

    return current_player, players, deck


def is_game_over(deck, players):
    """
    Checks if the game has reached its end condition. The game is over when the deck 
    is empty AND no further pairs can be made among any players' hands.

    Arguments:
        deck (list): The main deck of cards.
        players (list): A list of all player dictionaries.

    Returns:
        bool: True if the game is over, False otherwise.

    Side Effects:
        None
    """
    if deck:
        return False

    all_cards = [card for p in players for card in p["hand"]]
    rank_counts = Counter(card[:-1] for card in all_cards)
    if any(count >= 2 for count in rank_counts.values()):
        return False
    
    return True


def display_hand(player):
    """
    Prints a player's current hand and number of pairs to the console.

    Arguments:
        player (dict): The dictionary of the player whose hand is being displayed.

    Returns:
        None

    Side Effects:
        Prints output to standard output (the console).
    """
    print(f"  Your hand: {player['hand']}")
    print(f"  Pairs collected: {player['pairs']}")


def display_scores(players):
    """
    Prints the final pair counts for all players to the console.

    Arguments:
        players (list): A list of all player dictionaries.

    Returns:
        None

    Side Effects:
        Prints output to standard output (the console).
    """
    print("\nFinal scores:")
    for player in players:
        print(f"  {player['name']}: {player['pairs']} pair(s)")


def announce_loser(loser):
    """
    Prints the name of the losing player(s) to the console.

    Arguments:
        loser (str or list): The name of the losing player, or a list of names if tied.

    Returns:
        None

    Side Effects:
        Prints output to standard output (the console).
    """
    if isinstance(loser, list):
        print(f"\nIt's a tie! {', '.join(loser)} are all the {BURRO_WORD}!")
    else:
        print(f"\n{loser} is the {BURRO_WORD}! (fewest pairs)")


def get_num_players():
    """
    Prompts the user to enter a valid number of players (between 2 and 6).

    Arguments:
        None

    Returns:
        int: The validated number of players entered by the user.

    Side Effects:
        Blocks execution waiting for user input (stdin).
        Prints prompts and error messages to standard output (stdout).
    """
    while True:
        try:
            num = int(input("How many players total? (2-6): "))
            if 2 <= num <= 6:
                return num
            print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Please enter a valid number.")


def try_pair(player, drawn):
    """
    Checks if a newly obtained card pairs with any existing card in the player's hand.
    If it does, the pair is removed; if not, the card is added to the hand.

    Arguments:
        player (dict): The dictionary of the player receiving the card.
        drawn (str): The string representing the card obtained.

    Returns:
        str or None: The matching card from the hand if a pair is made, otherwise None.

    Side Effects:
        Mutates the 'player' dictionary by updating their hand (adding or removing a card) 
        and incrementing their pairs count if a match is found.
    """
    drawn_rank = drawn[:-1]
    match = None
    for card in player["hand"]:
        if card[:-1] == drawn_rank:
            match = card
            break
    if match:
        player["hand"].remove(match)
        player["pairs"] += 1
        return match
    else:
        player["hand"].append(drawn)
        return None


def human_turn(player, players, deck):
    """
    Handles the interactive terminal menu and actions for the human player's turn.

    Arguments:
        player (dict): The dictionary of the human player.
        players (list): A list of all player dictionaries in the game.
        deck (list): The main deck of cards.

    Returns:
        None

    Side Effects:
        Blocks execution waiting for user input (stdin).
        Prints menus, choices, and outcomes to standard output (stdout).
        Mutates the 'deck' list if a card is drawn.
        Mutates the 'player' dictionary based on drawn/stolen cards and used peek ability.
        Mutates opponent player dictionaries if a card is stolen.
    """
    print(f"\n--- Your turn ---")
    display_hand(player)


    opponents = [p for p in players if p["name"] != "You" and p["hand"]]

 
    can_draw  = len(deck) > 0
    can_steal = len(opponents) > 0

    if not can_draw and not can_steal:
        print("No cards available to draw or steal!")
        return

    
    print("\nWhat do you want to do?")
    options = []
    if can_draw:
        options.append("Draw from deck")
    if can_steal:
        options.append("Steal from a player")
    if not player["peek_used"] and can_steal:
        options.append("Peek at a player's card (1 use)")

    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(options):
                break
            print(f"Enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")

    action = options[choice - 1]


    if action == "Draw from deck":
        drawn = draw_card(deck)
        match = try_pair(player, drawn)
        if match:
            print(f"You drew {drawn} and paired it with {match}! Pairs: {player['pairs']}")
        else:
            print(f"You drew {drawn} — no pair.")


    elif action == "Steal from a player":
        target = pick_opponent(opponents)
        drawn = pick_hidden_card(target, player)
        match = try_pair(player, drawn)
        if match:
            print(f"You stole {drawn} and paired it with {match}! Pairs: {player['pairs']}")
        else:
            print(f"You stole {drawn} — no pair.")


    elif action == "Peek at a player's card (1 use)":
        player["peek_used"] = True
        target = pick_opponent(opponents)
       
        peeked = random.choice(target["hand"])
        print(f"You peeked and saw: {peeked} in {target['name']}'s hand!")
        input("Press Enter to now steal or draw...")
  
        human_turn(player, players, deck)


def pick_opponent(opponents):
    """
    Prompts the human player to select an opponent from the provided list.

    Arguments:
        opponents (list): A list of opponent player dictionaries who have cards.

    Returns:
        dict: The selected opponent player dictionary.

    Side Effects:
        Blocks execution waiting for user input (stdin).
        Prints choices to standard output (stdout).
    """
    print("\nChoose a player:")
    for i, opp in enumerate(opponents, 1):
        print(f"  {i}. {opp['name']} ({len(opp['hand'])} card(s))")
    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(opponents):
                return opponents[choice - 1]
            print(f"Enter a number between 1 and {len(opponents)}.")
        except ValueError:
            print("Please enter a valid number.")


def pick_hidden_card(target, player):
    """
    Displays an opponent's hand as hidden slots and prompts the human to select one to steal.

    Arguments:
        target (dict): The dictionary of the opponent being stolen from.
        player (dict): The dictionary of the human player (unused in function body, but kept for signature).

    Returns:
        str: The card string that was selected and stolen.

    Side Effects:
        Blocks execution waiting for user input (stdin).
        Prints the hidden hand to standard output (stdout).
        Mutates the 'target' dictionary by popping (removing) the selected card from their hand.
    """
    print(f"\n{target['name']}'s cards (face down):")
    for i in range(len(target["hand"])):
        print(f"  {i + 1}. ?")
    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(target["hand"]):
                return target["hand"].pop(choice - 1)
            print(f"Enter a number between 1 and {len(target['hand'])}.")
        except ValueError:
            print("Please enter a valid number.")


def ai_turn(player, players, deck):
    """
    Executes an automated turn for a non-human player, randomly choosing to draw or steal.

    Arguments:
        player (dict): The dictionary of the AI player taking the turn.
        players (list): A list of all player dictionaries.
        deck (list): The main deck of cards.

    Returns:
        None

    Side Effects:
        Prints turn actions and outcomes to standard output (stdout).
        Mutates the 'deck' list if the AI draws.
        Mutates the 'player' dictionary by updating hand and pairs.
        Mutates a target opponent's dictionary if the AI decides to steal.
    """
    print(f"\n--- {player['name']}'s turn ---")

    
    opponents = [p for p in players if p["name"] != player["name"] and p["hand"]]
    can_draw  = len(deck) > 0
    can_steal = len(opponents) > 0

    if not can_draw and not can_steal:
        print(f"  {player['name']} has no moves.")
        return

 
    steal = can_steal and (not can_draw or random.random() < 0.5)

    if steal:
        target = random.choice(opponents)
        index  = random.randint(0, len(target["hand"]) - 1)
        drawn  = target["hand"].pop(index)
        match  = try_pair(player, drawn)
        if match:
            print(f"  {player['name']} stole from {target['name']} and made a pair! Pairs: {player['pairs']}")
        else:
            print(f"  {player['name']} stole from {target['name']} — no pair.")
    else:
        drawn = draw_card(deck)
        match = try_pair(player, drawn)
        if match:
            print(f"  {player['name']} drew from the deck and made a pair! Pairs: {player['pairs']}")
        else:
            print(f"  {player['name']} drew from the deck — no pair.")


def setup_game():
    """
    Initializes the game state by getting player counts, building the deck, and creating players.

    Arguments:
        None

    Returns:
        tuple: A tuple containing the list of player dictionaries and the deck list.

    Side Effects:
        Calls functions that block for user input (stdin).
        Prints welcome messages and setup status to standard output (stdout).
    """
    print("=" * 40)
    print("    Welcome to BURRO / OLD MAID!")
    print("=" * 40)
    num_players = get_num_players()
    deck = create_deck()
    shuffle(deck)
    players = create_player(num_players, deck)
    players[0]["name"] = "You"
    print("\nCards dealt! Starting pairs removed.")
    print(f"Cards remaining in deck: {len(deck)}\n")
    return players, deck


def play_game():
    """
    The main game loop. Runs setup, cycles through player turns, and handles the end game.

    Arguments:
        None

    Returns:
        None

    Side Effects:
        Continuously calls functions that block for user input (stdin) and print to console (stdout).
        Heavily mutates the entire game state (deck and players) until the game finishes.
    """
    players, deck = setup_game()
    round_num = 1

    while not is_game_over(deck, players):
        print(f"\n=== Round {round_num} ===")
        for player in players:
            if is_game_over(deck, players):
                break
            if player["name"] == "You":
                human_turn(player, players, deck)
            else:
                ai_turn(player, players, deck)
        round_num += 1

    display_scores(players)
    announce_loser(determine_loser(players))


if __name__ == "__main__":
    play_game()
