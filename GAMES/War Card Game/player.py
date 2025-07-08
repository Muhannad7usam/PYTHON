"""
The Player class represents each participant in the War card game.
Players have a name and a collection of cards they're playing with.
"""

from typing import List, Union
from card import Card

class Player:
    def __init__(self, name: str):
        """Create a new player with their name and an empty hand"""
        self.name = name
        self.all_cards = []  # This holds the player's cards

    def remove_one(self) -> Card:
        """Play a card from the top of the player's stack"""
        if not self.all_cards:
            raise ValueError(f"{self.name} has no cards!")
        return self.all_cards.pop(0)

    def add_cards(self, new_cards: Union[Card, List[Card]]) -> None:
        """Add won cards to the bottom of the player's stack"""
        if isinstance(new_cards, list):
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)

    def __str__(self):
        """Give a friendly status update about the player"""
        return f"{self.name} has {len(self.all_cards)} cards"

    def __len__(self):
        """Tell us how many cards the player currently has"""
        return len(self.all_cards)