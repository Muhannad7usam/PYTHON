from turtle import Turtle

class Paddle(Turtle):
    PADDLE_SPEED = 10 
    UPPER_LIMIT = 250
    LOWER_LIMIT = -250

    def __init__(self, position):
        super().__init__()
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)
        self.y_move = 0

    def start_up(self):
        self.y_move = self.PADDLE_SPEED

    def start_down(self):
        self.y_move = -self.PADDLE_SPEED

    def stop(self):
        self.y_move = 0

    def move(self):
        new_y = self.ycor() + self.y_move
        # Constrain paddle within screen boundaries
        if new_y > self.UPPER_LIMIT:
            new_y = self.UPPER_LIMIT
        elif new_y < self.LOWER_LIMIT:
            new_y = self.LOWER_LIMIT
        self.goto(self.xcor(), new_y)