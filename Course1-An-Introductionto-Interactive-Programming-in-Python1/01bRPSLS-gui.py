## GUI-based version of RPSLS

###################################################
# Student should add code where relevant to the following.

import simplegui
import random

# Functions that compute RPSLS
# helper functions
import random
def name_to_number(name):
    # delete the following pass statement and fill in your code below
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Something was wrong with my name_to-number input."

# helper functions
def number_to_name(number):
    # delete the following pass statement and fill in your code below
    # delete the following pass statement and fill in your code below
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "Something was wrong with my number_to-name input."

# convert number to a name using if/elif/else
# don't forget to return the result!

# main functions

def rpsls(player_choice):
    # convert name to player_number using name_to_number
    player_number = name_to_number(player_choice)
    print "Player chooses", player_choice
    
    # compute random trial for computer_number using random.randrange()
    computer_number = random.randrange(0,5)
    
    # convert computer_number to name using number_to_name
    computer_name = number_to_name(computer_number)
    print"Computer chooses", computer_name
    
    # compute difference of player_number and computer_number modulo five
    
    difference = (player_number - computer_number) % 5
    
    # use if/elif/else to determine winner
    
    if (difference== 1) or (difference == 2):
        print "Player wins!"
        print " "
    elif (difference== 3) or (difference == 4):
        print "Computer wins!"
        print " "
    else:
        print "There is a tie between Player and Computer choices"
        print " "
        print " "


# Handler for input field

def get_guess(guess):
    
    # validate input
    if not (guess == "rock" or guess == "Spock" or guess == "paper" or
            guess == "lizard" or guess == "scissors"):
        print
        print 'Error: Bad input "' + guess + '" to rpsls'
        return
            else:
        rpsls(guess)



# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 200, 200)
frame.add_input("Enter guess for RPSLS", get_guess, 200)


# Start the frame animation
frame.start()




###################################################
# Test

get_guess("Spock")
get_guess("dynamite")
get_guess("paper")
get_guess("lazer")

###################################################
# Sample expected output from test
# Note that computer's choices may vary from this sample.

#Player chose Spock
#Computer chose paper
#Computer wins!
#
#Error: Bad input "dynamite" to rpsls
#
#Player chose paper
#Computer chose scissors
#Computer wins!
#
#Error: Bad input "lazer" to rpsls
