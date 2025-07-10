from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.go_to_start()
        self.setheading(90)

    def move_up(self):
        """Move the turtle forward"""
        self.forward(MOVE_DISTANCE)

    def go_to_start(self):
        """Reset turtle to starting position"""
        self.goto(STARTING_POSITION)

    def is_at_finish_line(self):
        """Check if turtle reached the finish line"""
        return self.ycor() > FINISH_LINE_Y