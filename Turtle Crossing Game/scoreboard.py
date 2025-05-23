from turtle import Turtle
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.LEVEL = 1
        self.penup()
        self.hideturtle()
        self.color("orange")
        self.goto(-300, 270)
        self.update()

    def update(self):
        self.write(arg=f"LEVEL={self.LEVEL}", font=FONT)

    def resetscore(self):
        self.clear()
        self.LEVEL += 1
        self.update()

    def game_over(self):
        self.color("red")
        self.goto(0, 0)
        self.write(f"GAME OVER", False, "center", ('Arial', 48, 'normal'))