from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import time

# Screen setup
screen = Screen()
screen.setup(width=600, height=600)
screen.title("Turtle Crossing Game")
screen.tracer(0)

# Game objects
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Controls
screen.listen()
screen.onkeypress(player.move_up, "Up")

# Game loop
game_is_on = True
while game_is_on:
    time.sleep(0.05)
    screen.update()
    
    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            game_is_on = False
            scoreboard.game_over()

    # Detect successful crossing
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.increase_speed()
        scoreboard.increase_level()

screen.exitonclick()