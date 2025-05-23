from tkinter import *
import pandas as pd
import random
import time

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- CREATE WINDOW ------------------------------- #
window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ---------------------------- SAVE WORDS ------------------------------- #
def save_words():
    global words, word
    words.remove(word)
    data = pd.DataFrame(words)
    data.to_csv("data/words_to_learn.csv", index=False)
    flip_card()

# ---------------------------- FLIP CARD ------------------------------- #
wait = None
def show_translation(word):
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=word["English"], fill="white")
    canvas.itemconfig(card_front, image=card_front)
    canvas.itemconfig(canvas_image, image=card_back)

def flip_card():
    global words , wait, word
    try:
        window.after_cancel(wait)
    except:
        pass
    if len(words) == 0:
        canvas.itemconfig(title_text, text="You've learned all the words", fill="black")
        canvas.itemconfig(word_text, text="")
    word = random.choice(words)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=word["French"], fill="black")
    canvas.itemconfig(card_front, image=card_front)
    canvas.itemconfig(canvas_image, image=card_front)
    
    wait = window.after(3000, show_translation, word)
    
# ---------------------------- CREATE CARDS ------------------------------- #
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

# Text
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Click to Begin", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# ---------------------------- BUTTONS ------------------------------- #
window.after(3000, flip_card)
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, bd=0, command=save_words)
right_button.grid(row=1, column=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0,bd=0, command=flip_card)
wrong_button.grid(row=1, column=0)

# ---------------------------- READ WORDS ------------------------------- #

try:
    data = pd.read_csv("data/words_to_learn.csv")
    words = data.to_dict(orient="records")
    if len(words) == 0:
        data = pd.read_csv("data/french_words.csv")
        words = data.to_dict(orient="records")
except:
    data = pd.read_csv("data/french_words.csv")
    words = data.to_dict(orient="records")
    




window.mainloop()
