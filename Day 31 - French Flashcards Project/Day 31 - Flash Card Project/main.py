import tkinter
from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = {}
# ---------------------------- French Dictionary ---------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")
# ---------------------------- Card Functionality ---------------------------- #
def next_card():
    global current_card, flipping_once
    window.after_cancel(flipping_once)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_card)
    flipping_again = window.after(5000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card)

def is_known():
    words_to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50,bg=BACKGROUND_COLOR)

flipping_once = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text="Title", font=("Times New Roman", 45, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_answer = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_answer, highlightthickness=0,command=flip_card)
unknown_button.grid(row=1, column=0)

right_answer = PhotoImage(file="images/right.png")
known_button = Button(image=right_answer, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)


next_card()

window.mainloop()


