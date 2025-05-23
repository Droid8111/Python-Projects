from turtle import Turtle,Screen
import random
import time

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:
    def __init__(self):
        self.all_cars = []
        self.carspeed = STARTING_MOVE_DISTANCE

    def create_car(self):
        num = random.randint(1, 6)
        if num == 1:
            new_car = Turtle()
            new_car.shape("square")
            new_car.shapesize(1, 2)
            new_car.penup()
            ycor = random.randint(-250, 250)
            new_car.goto(310, ycor)
            new_car.color(random.choice(COLORS))
            self.all_cars.append(new_car)

    def move(self):
        for i in self.all_cars:
            i.backward(self.carspeed)

    def level_up(self):
        self.carspeed += STARTING_MOVE_DISTANCE