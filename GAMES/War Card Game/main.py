"""
The main entry point for the War Card Game.
"""

from wargame import WarGame

def main():
    print("Welcome to the War Card Game!")
    player_name = input("Enter your name, brave warrior: ").strip() or "Player"

    game = WarGame(player1_name=player_name)
    game.play_game()

if __name__ == "__main__":
    main()