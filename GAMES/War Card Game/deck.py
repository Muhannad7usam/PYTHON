"""
The Deck class represents a complete deck of 52 playing cards.
It can shuffle the deck and deal cards to players.
"""

import random
from card import Card

class Deck:
    def __init__(self):
        """Create a fresh deck with all 52 cards in order"""
        self.all_cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]

    def shuffle(self):
        """Mix up all the cards in the deck for a random order"""
        random.shuffle(self.all_cards)

    def deal_one(self):
        """Take the top card from the deck and give it to a player"""
        if not self.all_cards:
            raise ValueError("Deck is empty!")
        return self.all_cards.pop()

    def __len__(self):
        """Tell us how many cards are still in the deck"""
        return len(self.all_cards)
