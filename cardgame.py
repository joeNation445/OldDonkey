import random
from collections import Counter

BURRO_WORD = "BURRO"
OLD_MAID = "QS"  # Queen of no pair


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
        # FIX: pop cards from the deck so players don't share cards
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
            "name": f"Player {i + 1}",  # FIX: added missing "name" key
            "hand": new_hand,           
            "pairs": pairs,            
        }
        players.append(player)
    return players


def draw_card(deck):
    """
    Draws a random card from the deck and removes it.
    Args:
        deck (list): list of remaining cards
    Returns:
        str: the card that was drawn, or None if deck is empty
    Side effects:
        removes the drawn card from the deck
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
    Args:
        current_player, players, deck
    Returns:
        Updated current_player, players, deck
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
