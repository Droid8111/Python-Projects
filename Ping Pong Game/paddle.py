from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, positionx, positiony):
        super().__init__()
        self.shape("square")
        self.fillcolor("white")
        self.penup()
        self.turtlesize(stretch_len=1, stretch_wid=5)
        self.goto(positionx, positiony)

    def up(self):
        if self.ycor() > 240:
            pass
        else:
            new_paddle_y = self.ycor() + 20
            self.goto(self.xcor(), y=new_paddle_y)

    def down(self):
        if self.ycor() < -230:
            pass
        else:
            new_paddle_y = self.ycor() - 20
            self.goto(self.xcor(), y=new_paddle_y)
