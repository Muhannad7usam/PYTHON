from turtle import Turtle
import time

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 20
FINISH_LINE_Y = 280

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("dark green")
        self.shapesize(stretch_wid=1.5, stretch_len=1.5)
        self.penup()
        self.go_to_start()
        self.setheading(90)
        self.animation_state = 0

    def move_up(self):
        """Move the turtle forward with animation"""
        self.forward(MOVE_DISTANCE)
        self.animate_walk()

    def move_down(self):
        """Move the turtle backward with animation"""
        if self.ycor() > -280:  # Prevent going off screen
            self.backward(MOVE_DISTANCE)
            self.animate_walk()

    def animate_walk(self):
        """Simple walking animation"""
        self.animation_state = (self.animation_state + 1) % 2
        if self.animation_state == 0:
            self.shapesize(stretch_wid=1.5, stretch_len=1.3)
        else:
            self.shapesize(stretch_wid=1.3, stretch_len=1.5)

    def go_to_start(self):
        """Reset turtle to starting position"""
        self.goto(STARTING_POSITION)
        self.setheading(90)

    def is_at_finish_line(self):
        """Check if turtle reached the finish line"""
        return self.ycor() > FINISH_LINE_Y

    def celebrate(self):
        """Celebration animation for crossing"""
        for _ in range(3):
            self.color("gold")
            time.sleep(0.1)
            self.color("dark green")
            time.sleep(0.1)

    def explode(self):
        """Explosion animation when hit"""
        self.color("red")
        self.shapesize(stretch_wid=2, stretch_len=2)
        time.sleep(0.5)
        self.hideturtle()