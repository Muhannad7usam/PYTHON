from turtle import Turtle

class Road(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("gray")
        self.penup()
        self.draw_road()
        self.draw_lane_markers()

    def draw_road(self):
        """Draw the main road area"""
        self.goto(-400, -300)
        self.begin_fill()
        for _ in range(2):
            self.forward(800)
            self.left(90)
            self.forward(600)
            self.left(90)
        self.end_fill()

    def draw_lane_markers(self):
        """Draw lane markings on the road"""
        self.color("yellow")
        self.width(4)
        for y in range(-240, 300, 60):
            self.goto(-400, y)
            self.pendown()
            for _ in range(20):
                self.forward(20)
                self.penup()
                self.forward(20)
                self.pendown()
            self.penup()