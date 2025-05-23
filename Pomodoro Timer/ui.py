from tkinter import *
from quiz_brain import QuizBrain
import html
THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.score = 0
        self.quiz = quiz_brain
        
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text="Score: 0", fg="white", bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(150, 125, width=280, text="Some Question Text", fill=THEME_COLOR, font=("Arial", 20, "italic"))
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        
        true_image = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_image, highlightthickness=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)

        false_image = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_image, highlightthickness=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        if self.quiz.still_has_questions():
            self.canvas.config(bg="white")
            question = html.unescape(self.quiz.next_question())
            self.canvas.itemconfig(self.question_text, text=question)
            self.canvas.itemconfig(self.question_text, fill=THEME_COLOR)
            self.true_button.config(state="normal")
            self.false_button.config(state="normal")
        else:
            self.canvas.itemconfig(self.question_text, text=f"You've reached the end of the quiz. Your final score was: {self.score}/10")
            self.canvas.config(bg="white")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        self.check_answer("True")
        

    def false_pressed(self):
        self.check_answer("False")
        

    def check_answer(self, user_answer: str):
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        correct_answer = self.quiz.check_answer(user_answer)
        if correct_answer:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)
        