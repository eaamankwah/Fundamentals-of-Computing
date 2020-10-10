# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

def __str__(self):
    return self.suit + self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []   # create Hand object
    
    def __str__(self):
        # return a string representation of a hand
        printString = ''
        for i in self.cards:
            printString += str(i) + ' '
        return "Hand contains " + printString
    
    def add_card(self, card):
        self.cards.append(card)    # add a card object to a hand
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        ace_number = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace_number = ace_number + 1
        if ((value + 10 <= 21) and (ace_number > 0)):
            value = value + 10
        return value
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 90

# define deck class
class Deck:
    def __init__(self):
        self.cards = []    # create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

def shuffle(self):
    # shuffle the deck
    return random.shuffle(self.cards)    # use random.shuffle()
    
    def deal_card(self):
        return self.cards.pop()    # deal a card object from the deck
    
    def __str__(self):
        prtString = ''
        for i in self.cards:
            prtString += str(i) + ' '
        return "Deck contains " + prtString    # return a string representing the deck

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, message, result, score
    
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    # print str(deck)
    message = "Hit or stand?"
    outcome = ""
    result = ""
    
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    if(in_play):
        score = score - 1;
    in_play = True

def hit():
    global outcome, message, score, in_play
    
    # if the hand is in play, hit the player
    if in_play == True:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            # if busted, assign a message to outcome, update in_play and score
            outcome = "Player busted!"
            message = "New deal?"
            score = score - 1
            in_play = False

# handler for a "Stand" button. Remind the player if they bust.
def stand():
    global in_play, score, message, outcome
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        
        # assign a message to outcome, update in_play and score
        # dealer win!
        if dealer.get_value() <= 21 and player.get_value()<= dealer.get_value():
            outcome = "Player lose."
            message = "New deal?"
            in_play = False
            score = score - 1
        # player win!
        else:
            outcome = "Player win."
            message = "New deal?"
            in_play = False
            score = score + 1

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # global player, dealer, in_play, message
    dealerPos = [60,240]
    playerPos = [dealerPos[0],dealerPos[1]+200]
    
    dealer.draw(canvas, dealerPos)
    player.draw(canvas, playerPos)
    canvas.draw_text("Blackjack", [60, 80], 60, "Red")
    canvas.draw_text("Dealer", [60, 200], 36, "Black")
    canvas.draw_text("Player", [60, 400], 36, "Black")
    canvas.draw_text("Score: " + str(score), [360, 150], 36, "Yellow")
    
    canvas.draw_text(outcome, [250, 200], 36, "Black")
    canvas.draw_text(message, [250, 400], 36, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
