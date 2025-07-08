"""
The WarGame class manages the entire game of War between two players.
It handles dealing cards, playing rounds, and determining the winner.
"""

import time
from typing import List, Tuple
from deck import Deck
from player import Player
from card import Card

class WarGame:
    def __init__(self, player1_name="Player", player2_name="Computer"):
        """Set up a new game with two players and a fresh deck"""
        self.player = Player(player1_name)
        self.computer = Player(player2_name)
        self.deck = Deck()
        self.round_num = 0
        self.game_over = False

    def _deal_cards(self):
        """Evenly distribute all cards between both players"""
        while len(self.deck) > 0:
            self.player.add_cards(self.deck.deal_one())
            self.computer.add_cards(self.deck.deal_one())

    def _compare_cards(self, player_card: Card, computer_card: Card) -> int:
        """See which card wins (1=player, -1=computer, 0=war)"""
        if player_card > computer_card:
            return 1
        elif player_card < computer_card:
            return -1
        return 0

    def _handle_war(self, war_chest: List[Card]) -> Tuple[List[Card], bool]:
        """Handle the special war scenario when cards are equal"""
        print("\n⚔️  WAR! The cards are equally powerful! ⚔️")

        for _ in range(3):
            if len(self.player) == 0 or len(self.computer) == 0:
                return war_chest, True
            war_chest.append(self.player.remove_one())
            war_chest.append(self.computer.remove_one())
            print("Cards placed face down...")
            time.sleep(0.5)

        return war_chest, False

    def play_round(self) -> Tuple[bool, str]:
        """Play one complete round of the game"""
        self.round_num += 1
        print(f"\n🌟 Round {self.round_num} 🌟")
        print(f"{self.player.name}: {len(self.player)} cards")
        print(f"{self.computer.name}: {len(self.computer)} cards")
        time.sleep(1)

        if len(self.player) == 0:
            return True, f"{self.computer.name} wins! {self.player.name} has no cards left."
        if len(self.computer) == 0:
            return True, f"{self.player.name} wins! {self.computer.name} has no cards left."

        player_card = self.player.remove_one()
        computer_card = self.computer.remove_one()

        print(f"\n{self.player.name} plays: {player_card}")
        time.sleep(0.7)
        print(f"{self.computer.name} plays: {computer_card}")
        time.sleep(0.7)

        war_chest = [player_card, computer_card]
        result = self._compare_cards(player_card, computer_card)

        while result == 0:
            war_chest, game_ended = self._handle_war(war_chest)
            if game_ended:
                return True, "Game ended during war!"

            player_card = self.player.remove_one()
            computer_card = self.computer.remove_one()

            print(f"\nNew cards drawn for war:")
            print(f"{self.player.name}: {player_card}")
            print(f"{self.computer.name}: {computer_card}")
            time.sleep(1)

            war_chest.extend([player_card, computer_card])
            result = self._compare_cards(player_card, computer_card)

        if result == 1:
            self.player.add_cards(war_chest)
            print(f"\n🎉 {self.player.name} wins this round and gets {len(war_chest)} cards!")
        else:
            self.computer.add_cards(war_chest)
            print(f"\n💻 {self.computer.name} wins this round and gets {len(war_chest)} cards!")

        time.sleep(1.5)
        return False, "Round completed"

    def play_game(self):
        """Run the entire game from start to finish"""
        print("\n" + "="*50)
        print("🚀 Welcome to the Ultimate War Card Game! 🚀".center(50))
        print("="*50)

        self.deck.shuffle()
        self._deal_cards()

        print("\nCards have been shuffled and dealt. Let the battle begin!")
        print(f"{self.player.name} vs {self.computer.name}")
        print("="*50)

        while not self.game_over:
            input("\nPress Enter to play the next round...")
            self.game_over, message = self.play_round()
            if self.game_over:
                print("\n" + "="*50)
                print("🏆 Game Over! 🏆".center(50))
                print(message.center(50))
                print("="*50)

                print(f"\nFinal Score:")
                print(f"{self.player.name}: {len(self.player)} cards")
                print(f"{self.computer.name}: {len(self.computer)} cards")

                if len(self.player) > len(self.computer):
                    print(f"\n✨ {self.player.name} is the ultimate champion! ✨")
                elif len(self.player) < len(self.computer):
                    print(f"\n🤖 {self.computer.name} dominates the battlefield! 🤖")
                else:
                    print("\n⚖️  The battle ends in a draw! ⚖️")