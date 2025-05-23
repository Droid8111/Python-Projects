from turtle import Turtle, Screen
import random

turtle = Turtle()
direction = ["right", "left"]
turtle.pensize(5)
screen = Screen()
screen.colormode(255)
turtle.speed(0)
screen.listen()

def color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    c = (r, g, b)
    return c

def up():
    turtle.fd(10)
# def down():
#     turtle.fd(50)
def right():
    turtle.right(5)
def left():
    turtle.left(5)
screen.onkeypress(up, "w")
screen.onkeypress(right, "d")
screen.onkeypress(left, "a")
turtle.fillcolor('red')
screen.exitonclick()
