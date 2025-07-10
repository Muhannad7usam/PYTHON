from turtle import Turtle

FONT = ("Courier", 24, "normal")
ALIGNMENT = "center"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.color("black")
        self.goto(-380, 260)
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
        self.color("red")
        self.write("GAME OVER", align=ALIGNMENT, font=("Courier", 36, "bold"))
        self.goto(0, -40)
        self.write(f"Final Level: {self.level}", align=ALIGNMENT, font=FONT)