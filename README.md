BURRO / OLD MAID 🃏

This is a terminal style Python card game inspired by Old Maid kinda with a twwist. Play against AI players, collect matching pairs and try noy to become the BURRO at the end of the game.

- Features
Play against 1–5 AI opponents
Choose between drawing from the deck or stealing from another player
Special one-time “Peek” ability to secretly view an opponent’s card

Prerequisites
This game requires Python 3 and uses only built-in Python modules (random and collections). No external libraries are needed.

How to Run
Download or clone the game file (cardgame.py)
Open a terminal or command prompt
Navigate to the folder containing the file
And hit the Run button
python cardgame.py

How to Play / Objective
The goal is to collect as many matching pairs as possible. The player with the fewest pairs at the end of the game becomes the BURRO.

The Queen of Spades is removed from the deck at the start, guaranteeing that one card will remain unmatched.(This is like a classic old maid rule although it doesnt do much)

Setup
Enter the number of players (2–6)
Each player is dealt 5 cards
Any starting pairs are automatically removed and added to the player's score
Turn Options

During your turn, you can:

Draw a random card from the deck
Steal a random card from another player
Use your one-time Peek ability to look at one of an opponent’s cards before making your move
Making Pairs

If the card you draw or steal matches the rank of a card already in your hand, a pair is formed. The pair is removed from your hand and your score increases by 1. Game Over
The game ends when the deck is empty and no more pairs can be made. Final scores are counted, and the player with the fewest pairs is THE BURRO.
