from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(-220, 250)
        self.update_scoreboard()

    def update_scoreboard(self):
        """Display current level"""
        self.clear()
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        """Increase level and update display"""
        self.level += 1
        self.update_scoreboard()

    def game_over(self):
        """Display game over message"""
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)
        self.goto(0, -30)
        self.write(f"Final Level: {self.level}", align=ALIGNMENT, font=FONT)