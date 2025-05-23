from turtle import Turtle

POSITIONS = [(0, 0), (-20, 0), (-40, 0)]
MOVE = 20


class Snake:
    def __init__(self):
        self.segments = []
        self.createsnake()

    def createsnake(self):
        for position in POSITIONS:
            self.add_segment(position)
    def add_segment(self,position):
        cube = Turtle(shape="square")
        cube.color("white")
        cube.penup()
        cube.goto(position)
        self.segments.append(cube)
    def extend(self):
        self.add_segment(self.segments[-1].position())
    def forward(self):
        self.forward()

    def move(self):
        for seg in range(len(self.segments) - 1, 0, -1):
            newx = self.segments[seg - 1].xcor()
            newy = self.segments[seg - 1].ycor()
            self.segments[seg].goto(newx, newy)
        self.segments[0].forward(MOVE)


    def reset(self):
        for seg in self.segments:
            seg.goto(700,700)
        self.segments.clear()
        self.createsnake()
    def up(self):
        if self.segments[0].heading() != 270:
            self.segments[0].setheading(90)

    def left(self):
        if self.segments[0].heading() != 0:
            self.segments[0].setheading(180)

    def right(self):
        if self.segments[0].heading() != 180:
            self.segments[0].setheading(0)

    def down(self):
        if self.segments[0].heading() != 90:
            self.segments[0].setheading(270)
