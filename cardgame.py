import random
from collections import Counter

BURRO_WORD = "BURRO"
OLD_MAID = "QS"


def create_deck():
    suits = ["H", "D", "C", "S"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [rank + suit for rank in ranks for suit in suits]
    deck.remove(OLD_MAID)
    return deck


def shuffle(deck):
    """Fisher-Yates shuffle: every ordering is equally likely."""
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]


def create_player(num_player, deck):
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
    Draws a random card from the deck and removes it.
    Returns None if deck is empty.
    """
    if len(deck) == 0:
        return None
    index = random.randint(0, len(deck) - 1)
    card = deck[index]
    deck.pop(index)
    return card


def determine_loser(players):
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
    Handles one player's turn: draws a card, checks for a pair, removes it if found.
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
  
    if deck:
        return False

    all_cards = [card for p in players for card in p["hand"]]
    rank_counts = Counter(card[:-1] for card in all_cards)
    if any(count >= 2 for count in rank_counts.values()):
        return False
    
    return True


def display_hand(player):
    print(f"  Your hand: {player['hand']}")
    print(f"  Pairs collected: {player['pairs']}")


def display_scores(players):
    print("\nFinal scores:")
    for player in players:
        print(f"  {player['name']}: {player['pairs']} pair(s)")


def announce_loser(loser):
    if isinstance(loser, list):
        print(f"\nIt's a tie! {', '.join(loser)} are all the {BURRO_WORD}!")
    else:
        print(f"\n{loser} is the {BURRO_WORD}! (fewest pairs)")


def get_num_players():
    while True:
        try:
            num = int(input("How many players total? (2-6): "))
            if 2 <= num <= 6:
                return num
            print("Please enter a number between 2 and 6.")
        except ValueError:
            print("Please enter a valid number.")


def try_pair(player, drawn):
    """Check if drawn card pairs with anything in hand. Remove pair if so."""
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
    """Let the human choose which opponent to steal from."""
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
    """Show the target's hand as hidden slots and let the human pick one."""
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
