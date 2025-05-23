from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.fillcolor("white")
        self.penup()
        self.ymove = 1
        self.xmove = 1
        self.time = .01

    def move(self):
        newx = self.xcor() + self.xmove
        newy = self.ycor() + self.ymove
        self.goto(newx, newy)

    def bounce(self):
        if self.ycor() > 280 or self.ycor() < -280:
            self.ymove *= -1

    def paddle_bounce(self):
        self.xmove *= -1
        if self.time > .002:
            self.time -= .001
    def out(self):
        self.time = .01
        self.xmove *= -1
        self.ymove *= -1
        self.goto(0, 0)
