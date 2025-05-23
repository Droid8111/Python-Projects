from turtle import Turtle
from typing import TextIO


class Scoreboard(Turtle):
    def __init__(self):
        self.score = 0
        with open("score.txt") as data:
            self.highscore = int(data.read())
        super().__init__()
        self.penup()
        self.color("white")
        self.goto(0, 265)
        self.score_update()
        self.hideturtle()

    def increase_score(self):
        self.score += 1
        self.score_update()

    def score_update(self):
        self.clear()
        with open("score.txt") as data:
            self.highscore = int(data.read())
        self.write(f"Score={self.score} High Score={self.highscore}", False, "center", ('Arial', 24, 'normal'))

    def reset(self):
        if self.score > self.highscore:
            with open("score.txt", mode="w") as data:
                data.write(f"{self.score}")

            self.score_update()
        self.score = 0
        self.score_update()
