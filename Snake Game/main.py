from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)
snake = Snake()
food = Food()
scoreboard = Scoreboard()
screen.listen()
screen.onkeypress(snake.up, "w")
screen.onkeypress(snake.down, "s")
screen.onkeypress(snake.left, "a")
screen.onkeypress(snake.right, "d")

game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()
    if snake.segments[0].distance(food) < 15:
        food.refresh()
        scoreboard.increase_score()
        snake.extend()

    if snake.segments[0].xcor() < -280 or snake.segments[0].xcor() > 280 or snake.segments[0].ycor() < -290 or snake.segments[0].ycor() > 280:
        snake.reset()
        scoreboard.reset()
    for segments in snake.segments[3:]:
        if snake.segments[0].distance(segments) < 10:
            snake.reset()
            scoreboard.reset()
screen.exitonclick()
