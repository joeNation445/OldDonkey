import random
from collections import Counter

def create_player(num_player, deck):
    players = []

    for i in range(num_player):
        # deal 5 unique cards
        hand = random.sample(deck, 5)

        
        ranks = [card[:-1] for card in hand]  # remove suit
        count = Counter(ranks)

        pairs = 0
        new_hand = []

        # remove pairs
        for card in hand:
            rank = card[:-1]
            if count[rank] >= 2:
                pairs += count[rank] // 2
                count[rank] = 0  # prevent double counting
            else:
                new_hand.append(card)

        player = {
            "Hand": new_hand,
            "Pairs": pairs,
            "Remaining": len(new_hand)
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
    lowest_pairs = players[0]["Pairs"]
    losers = [players[0]["Name"]]

    for player in players[1:]:
        if player["Pairs"] < lowest_pairs:
            lowest_pairs = player["Pairs"]
            losers = [player["Name"]]
        elif player["Pairs"] == lowest_pairs:
            losers.append(player["Name"])

    if len(losers) == 1:
        return losers[0]
    else:
        return losers



def player_turn(current_player, players, deck):
    """
Handles one players turn: draws, asks, take cards, and remove pairs.

Args:
    current_player, players, deck

Returns:
    Updated current_player, players, deck
    """

    if deck:
        drawn_card = deck.pop(0)
        current_player["hand"].append(drawn_card)

    other_player = None
    for player in players:
        if player != current_player:
            other_player = player
            break

    if current_player["hand"] and other_player is not None:
        asked_rank = current_player["hand"][0]

        taken_cards = []
        for card in other_player["hand"]:
            if card == asked_rank:
                taken_cards.append(card)

        for card in taken_cards:
            other_player["hand"].remove(card)
            current_player["hand"].append(card)

    rank_counts = {}
    for card in current_player["hand"]:
        if card in rank_counts:
            rank_counts[card] += 1
        else:
            rank_counts[card] = 1

    new_hand = []
    for card in current_player["hand"]:
        if rank_counts[card] % 2 != 0:
            new_hand.append(card)

    current_player["hand"] = new_hand

    return current_player, players, deck
