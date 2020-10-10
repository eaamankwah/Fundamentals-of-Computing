# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:13:11 2017

@author: EAmankwah
"""

# implementation of card game - Memory

import simplegui
import random
index1 = 0
index2 = 0
number = []
exposed = []

# helper function to initialize globals
def new_game():
    global turns, number, exposed, state
    turns = 0
    state = 0
    number=[i for i in range(8)]+[i for i in range(8)]
    random.shuffle(number)
    exposed = [False for i in range(16)]

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turns, index1, index2
    openedCard = int(pos[0] //50)
    if state == 0:
        state = 1
        index1 = openedCard
        exposed[index1] = True
    elif state == 1:
        if not exposed[openedCard]:
            state = 2
            index2 = openedCard
            exposed[index2] = True
            turns = turns + 1
    elif state == 2:
        if not exposed[openedCard]:
            if number[index1] == number[index2]:
                pass
            else:
                exposed[index1] = False
                exposed[index2] = False
            index1 = openedCard
            exposed[index1] = True
            state = 1
            pass

# cards are logically 50x100 pixels in size
def draw(canvas):
    label.set_text("Turns = " + str(turns))
    for i in range(0, len(number)):
        if exposed[i] == True:
            canvas.draw_text(str(number[i]), [i * 50 + 10, 75], 60, "White")
        else:
            canvas.draw_polygon([(50 * i, 0), (50 * (i + 1), 0), (50 * (i + 1), 100), (50 * i, 100)], 2, 'Red', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
