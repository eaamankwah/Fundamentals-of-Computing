# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

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




# print a blank line to separate consecutive games

# print out the message for the player's choice

# convert the player's choice to player_number using the function name_to_number()

# compute random guess for comp_number using random.randrange()

# convert comp_number to comp_choice using the function number_to_name()

# print out the message for computer's choice

# compute difference of comp_number and player_number modulo five

# use if/elif/else to determine winner, print winner message


# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


