from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from road import Road
import time

# Screen setup
screen = Screen()
screen.setup(width=800, height=600)
screen.title("Turtle Crossing Adventure")
screen.bgcolor("lightblue")
screen.tracer(0)

# Game elements
road = Road()
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

# Controls
screen.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_down, "Down")
screen.onkeypress(screen.bye, "Escape")  # Exit game

# Game loop
game_is_on = True
while game_is_on:
    time.sleep(0.05)
    screen.update()
    
    car_manager.create_car()
    car_manager.move_cars()

    # Detect collision with car
    for car in car_manager.all_cars:
        if car.distance(player) < 25:
            game_is_on = False
            scoreboard.game_over()
            player.explode()

    # Detect successful crossing
    if player.is_at_finish_line():
        player.celebrate()
        player.go_to_start()
        car_manager.increase_speed()
        scoreboard.increase_level()

screen.exitonclick()