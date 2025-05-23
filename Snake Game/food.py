from turtle import Turtle
import random


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.speed(0)
        self.shape("circle")
        self.color("red")
        self.shapesize(.5, .5)
        self.refresh()

    def refresh(self):
        randomx = random.randint(-280, 280)
        randomy = random.randint(-280, 280)
        self.goto(randomx, randomy)
