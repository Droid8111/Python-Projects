import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
score = Scoreboard()
screen = Screen()
screen.tracer(0)
player = Player()
screen.setup(width=600, height=600)
car = CarManager()
screen.listen()
screen.onkeypress(player.up, "w")
screen.update()
game_is_on = True
while game_is_on:
    time.sleep(0.1)
    if player.ycor() == 280:
        player.goto(0, -280)
        car.level_up()
        score.resetscore()
    car.create_car()
    car.move()
    screen.update()
    for _ in car.all_cars:
        if _.distance(player) < 25:
            game_is_on = False
            score.game_over()
            player.color("white")
            screen.bgcolor("black")



screen.exitonclick()