from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
scoreboard = Scoreboard()
screen.setup(800, 600)
screen.bgcolor("black")
screen.tracer(0)
screen.listen()
r_paddle = Paddle(350, 0)
l_paddle = Paddle(-350, 0)
ball = Ball()
screen.onkeypress(l_paddle.up, "w")
screen.onkeypress(l_paddle.down, "s")
screen.onkeypress(r_paddle.up, "Up")
screen.onkeypress(r_paddle.down, "Down")
game_on = True
while game_on:
    time.sleep(ball.time)
    screen.update()
    ball.bounce()
    if ball.distance(r_paddle) < 50 and 320 < ball.xcor() < 350 or ball.distance(l_paddle) < 50 and -350 < ball.xcor() < -320:
        ball.paddle_bounce()
    if ball.xcor() > 370:
        ball.out()
        scoreboard.lpoint()
    elif ball.xcor() < -370:
        ball.out()
        scoreboard.rpoint()
    ball.move()


screen.exitonclick()
