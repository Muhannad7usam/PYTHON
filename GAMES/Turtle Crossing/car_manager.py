from turtle import Turtle
import random

COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 2
CAR_FREQUENCY = 6  # Higher number means fewer cars

class CarManager:
    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE
        self.car_shapes = ["square", "circle", "triangle"]

    def create_car(self):
        """Create a new car with random chance"""
        if random.randint(1, CAR_FREQUENCY) == 1:
            new_car = Turtle()
            new_car.shape(random.choice(self.car_shapes))
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.color(random.choice(COLORS))
            new_car.penup()
            new_car.goto(400, random.randint(-250, 250))
            self.all_cars.append(new_car)

    def move_cars(self):
        """Move all cars forward"""
        for car in self.all_cars:
            car.backward(self.car_speed)
            # Remove cars that are off-screen
            if car.xcor() < -420:
                car.hideturtle()
                self.all_cars.remove(car)

    def increase_speed(self):
        """Increase car speed when level up"""
        self.car_speed += MOVE_INCREMENT