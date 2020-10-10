# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(120,240), random.randrange(60,180)]
    if (direction == LEFT):
        ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
    else:
        ball_vel[1] = -ball_vel[1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
    paddle2_pos = [WIDTH - PAD_WIDTH / 2, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    if (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        if (paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            spawn_ball(RIGHT)
            score2 = score2 + 1
    
    if (ball_pos[0] >= WIDTH - BALL_RADIUS -PAD_WIDTH):
        if (paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = ball_vel[0]*1.1
            ball_vel[1] = ball_vel[1]*1.1
        else:
            spawn_ball(LEFT)
            score1 = score1 + 1
ball_pos[0] += ball_vel[0]/60
ball_pos[1] += ball_vel[1]/60

# draw ball
c.draw_circle(ball_pos, BALL_RADIUS, 3, "White","White")
    
    # update paddle's vertical position, keep paddle on the screen
    if HALF_PAD_HEIGHT <= paddle1_pos[1] + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
if HALF_PAD_HEIGHT <= paddle2_pos[1] + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
    paddle2_pos[1] += paddle2_vel
    
    # draw paddles
    # paddle 1
    pad1_top = [paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT]
    pad1_bot = [paddle1_pos[0],paddle1_pos[1] + HALF_PAD_HEIGHT]
    c.draw_line(pad1_top, pad1_bot, PAD_WIDTH, "White")
    # paddle 2
    pad2_top = [paddle2_pos[0],paddle2_pos[1] - HALF_PAD_HEIGHT]
    pad2_bot = [paddle2_pos[0],paddle2_pos[1] + HALF_PAD_HEIGHT]
    c.draw_line(pad2_top, pad2_bot, PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide
    
    # draw scores
    c.draw_text(str(score1), [150, 40], 48, 'White')
    c.draw_text(str(score2), [450, 40], 48, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -acc
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = acc
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -acc
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    acce = 4
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background('Blue') # set background of canvas to blue
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
