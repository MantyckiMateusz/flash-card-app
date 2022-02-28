from tkinter import *
import pandas as pd
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
#-------------Create flash card-------------
#Try to read the list of words left to learn, if it doesn't exist read the full list
try:
    data = pd.read_csv('data/to_learn.csv').to_dict(orient='records')
except FileNotFoundError:
    data = pd.read_csv('data/french_words.csv').to_dict(orient='records')

def create_flash_card(word):
    '''A function that creates a new flashcard by changing the card background image, title and word on the card. After that the function
    starts a timer that will flip the card after 3 seconds'''
    global timer
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(title, text='French', fill='black')
    canvas.itemconfig(english_word, text=f'{word["French"]}', fill='black')
    timer = window.after(3000, flip_card)

#-------------Button functionality-------------
#load random word from data as current word
curr_word = choice(data)
def known_word():
    '''A function that will stop the timer flipping the card, remove the known word from the list, get a new random word from the list as current word
    call create_flash_card function and then call save_progress function'''
    global curr_word, timer
    window.after_cancel(timer)
    data.remove(curr_word)
    curr_word = choice(data)
    create_flash_card(curr_word)
    save_progress()

def unknown_word():
    '''A function that will stop the timer flipping the card, get a new random word from the list as current word
    call create_flash_card function and then call save_progress function'''
    global curr_word, timer
    window.after_cancel(timer)
    curr_word = choice(data)
    create_flash_card(curr_word)
    save_progress()

#-------------Card flip functionality-------------
def flip_card():
    '''A function that flips the card, changing it's background, text color, title and switching the french word to it's english translation.'''
    global curr_word
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(title, text='English', fill='white')
    canvas.itemconfig(english_word, text=f'{curr_word["English"]}', fill='white')
    window.after_cancel(timer)
#-------------Save progress-------------
def save_progress():
    '''A function saving current state of the word list to to_learn.csv file'''
    to_learn = pd.DataFrame(data)
    to_learn.to_csv('data/to_learn.csv')


#-------------UI SETUP-------------
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#Images
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
right = PhotoImage(file='images/right.png')
wrong = PhotoImage(file='images/wrong.png')

#Creating the card
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=card_front)
title = canvas.create_text(400, 150,text="Title", font=('Ariel', 40, 'italic'))
english_word = canvas.create_text(400, 263,text=f"word", font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

#Creating right and wrong buttons

right_button = Button(image=right, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, command=known_word)
wrong_button = Button(image=wrong, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0, command=unknown_word)

right_button.grid(column=1, row=1)
wrong_button.grid(column=0, row=1)

create_flash_card(curr_word)
window.mainloop()