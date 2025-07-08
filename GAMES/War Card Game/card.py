"""
The Card class represents a single playing card in our War game.
Each card knows its suit, rank, and how powerful it is compared to others.
"""

class Card:
    # All possible suits and ranks a card can have
    suits = ('♥ Hearts', '♦ Diamonds', '♠ Spades', '♣ Clubs')
    ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    # How powerful each rank is (Ace is high)
    values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, suit: str, rank: str):
        """Create a new card with a specific suit and rank."""
        self.suit = suit
        self.rank = rank
        self.value = self.values[rank]  # How powerful this card is

    def __str__(self):
        """Return a pretty description of the card, like 'A of Hearts'"""
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        """Technical representation for debugging purposes"""
        return f"Card('{self.suit}', '{self.rank}')"

    def __eq__(self, other):
        """Check if two cards have equal power"""
        return self.value == other.value

    def __lt__(self, other):
        """Check if this card is weaker than another"""
        return self.value < other.value

    def __gt__(self, other):
        """Check if this card is stronger than another"""
        return self.value > other.value
