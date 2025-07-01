from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_X_POSITION = 350
BALL_X_THRESHOLD = 380
PADDLE_COLLISION_X = 320

def setup_screen():
    screen = Screen()
    screen.bgcolor("black")
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Pong")
    screen.tracer(0)
    return screen

def bind_keys(screen, left_paddle, right_paddle):
    screen.listen()
    # Right paddle controls
    screen.onkeypress(right_paddle.start_up, "Up")
    screen.onkeyrelease(right_paddle.stop, "Up")
    screen.onkeypress(right_paddle.start_down, "Down")
    screen.onkeyrelease(right_paddle.stop, "Down")
    # Left paddle controls
    screen.onkeypress(left_paddle.start_up, "w")
    screen.onkeyrelease(left_paddle.stop, "w")
    screen.onkeypress(left_paddle.start_down, "s")
    screen.onkeyrelease(left_paddle.stop, "s")

def main():
    screen = setup_screen()
    r_paddle = Paddle((PADDLE_X_POSITION, 0))
    l_paddle = Paddle((-PADDLE_X_POSITION, 0))
    ball = Ball()
    scoreboard = Scoreboard()

    bind_keys(screen, l_paddle, r_paddle)

    game_is_on = True
    while game_is_on:
        time.sleep(0.008)  # Reduced further to compensate for faster ball
        screen.update()

        # Paddle movement
        l_paddle.move()
        r_paddle.move()

        # Ball movement
        ball.move()

        # Wall collision
        if ball.ycor() > 280 or ball.ycor() < -280:
            ball.bounce_y()

        # Paddle collision
        if ((ball.distance(r_paddle) < 50 and ball.xcor() > PADDLE_COLLISION_X) or 
            (ball.distance(l_paddle) < 50 and ball.xcor() < -PADDLE_COLLISION_X)):
            ball.increase_speed()
            ball.bounce_x()

        # Scoring
        if ball.xcor() > BALL_X_THRESHOLD:
            scoreboard.l_point()
            ball.reset_position()
        elif ball.xcor() < -BALL_X_THRESHOLD:
            scoreboard.r_point()
            ball.reset_position()

    screen.exitonclick()

if __name__ == "__main__":
    main()