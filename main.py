from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
a = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global a, flip_timer
    window.after_cancel(flip_timer)
    a = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=a["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=answer_card)


def answer_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=a["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def known_card():
    to_learn.remove(a)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=answer_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 275, text="word", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=1)

cross_img = PhotoImage(file="images/wrong.png")
button1 = Button(image=cross_img, highlightthickness=0, command=next_card)
button1.grid(column=0, row=1)
tick_img = PhotoImage(file="images/right.png")
button2 = Button(image=tick_img, highlightthickness=0, command=known_card)
button2.grid(column=2, row=1)

next_card()
window.mainloop()