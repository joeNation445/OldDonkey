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
