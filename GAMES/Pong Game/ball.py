from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.initial_speed = 1.0  
        self.x_move = self.initial_speed
        self.y_move = self.initial_speed
        self.speed_increment = 0.15  
        self.max_speed = 2.5  
        self.reset_position()

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def increase_speed(self):
        # More aggressive speed increase
        if (abs(self.x_move) + abs(self.y_move)) / 2 < self.max_speed:
            self.x_move *= 1.15
            self.y_move *= 1.15

    def reset_speed(self):
        direction_x = 1 if self.x_move > 0 else -1
        direction_y = 1 if self.y_move > 0 else -1
        self.x_move = self.initial_speed * direction_x
        self.y_move = self.initial_speed * direction_y

    def reset_position(self):
        self.goto(0, 0)
        self.bounce_x()
        self.reset_speed()