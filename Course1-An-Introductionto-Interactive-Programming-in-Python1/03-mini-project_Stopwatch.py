# template for "Stopwatch: The Game"
# implement simplegui
import simplegui

# define global variables
current = 0 # time
count = 0
wins = 0
stop = False
message = ''

# define event handlers for buttoms; "Start", "Stop" and "Reset".
def start_button_handler():
    global stop
    stop = True
    timer.start()

def reset_button_handler():
    global current, count, wins, stop
    current = 0
    count = 0
    wins = 0
    stop = False
    timer.stop()

def stop_button_handler():
    global count, wins, stop
    if stop:
        stop = False
        count = count + 1
        if current % 10 == 0:
            wins = wins +1
        timer.stop()

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global message
    a = int(t // 600) # the amount of minutes in that number
    b = int(t - a*600)//100   # the amount of tens of seconds
    c = int(t - a*600 - b*100)//10   # the amount of seconds in excess of tens of seconds
    d = t % 10           # the amount of the remaining tenths of seconds
    message = str(a) + ":" + str(b) + str(c) + "." + str(d)
    return message

pass

# define event handler for timer
def tick():
    global current
    current += 1

# define draw handler
def draw(c):
    global message
    c.draw_text(format(current), (100, 125), 48, "White")
    score = str(wins)+"/"+str(count)
    c.draw_text(score, (135,30), 30, "Red")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 250, 250)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.add_button("Start", start_button_handler, 100)
frame.add_button("Stop", stop_button_handler, 100)
frame.add_button("Reset", reset_button_handler, 100)
frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric
