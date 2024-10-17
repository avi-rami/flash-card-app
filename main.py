from tkinter import *
import pandas as pd
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"

def next_card():
    global timer, current_word
    window.after_cancel(timer)  #ensures the timer cancels if card is flipped faster than 3 sec
    canvas.itemconfig(language, text="French")
    canvas.itemconfig(card, image=front_card)
    if len(to_learn) > 0:
        current_word = random.choice(to_learn)
        canvas.itemconfig(word_text, text=current_word["French"], fill="black")
        canvas.itemconfig(language, text="French", fill="black")
    else:
        messagebox.showinfo(title="Great Work!", message="You've completed this set of flashcards. Exit the application to try again!")
    timer = window.after(3000, flip_card)


def flip_card():
    global current_word
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_word["English"], fill="white")
    canvas.itemconfig(card, image=back_card)


def remove_learned_word():
    to_learn.remove(current_word)
    data = pd.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv",index=False)

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

def timer_start():
    pass

# load in the data, either previously saved progress or fresh data
try:
    data = pd.read_csv("./data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except:
    data = pd.read_csv("./data/french_words.csv")
    to_learn = data.to_dict(orient="records")
current_word = random.choice(to_learn)

timer = window.after(0, timer_start)

# flash cards
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 263, image=front_card)
language = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Press 'x' to begin.", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# left/right buttons
check_mark = PhotoImage(file="./images/right.png")
right_button = Button(image=check_mark, command=lambda: [remove_learned_word(), next_card()], highlightthickness=0, highlightcolor=BACKGROUND_COLOR, borderwidth=0)
right_button.grid(row=1, column=1)

cross = PhotoImage(file="./images/wrong.png")
left_button = Button(image=cross, command=next_card, highlightthickness=0, highlightcolor=BACKGROUND_COLOR,borderwidth=0)
left_button.grid(row=1, column=0)

window.mainloop()
