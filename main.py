import curses
import pomodoro
from threading import Thread
from pyfiglet import Figlet

p = pomodoro.Pomodoro()

# Initialize curses
s = curses.initscr()

curses.noecho()

curses.cbreak()

s.keypad(True)

# Set the time for the pomodoro
p.setTime(0,0,10)

def countdown():
    p.timer()

def main(s):
    countdown_thread.start() # Start the countdown thread
    while True:
        text = Figlet(font='big')

        s.clear() # Clear the screen
        s.addstr(text.renderText(str(p.time()))) # Print the text which is converted to ascii art by figlet

        if p.time() == 0: # Stop the thread and break the while loop when the time is finished
            countdown_thread.join()
            break

        curses.napms(1000) # Sleep for one second

        s.refresh() # Refresh the screen

countdown_thread = Thread(target=countdown) # Thread to countdown and show the time at the same time

curses.wrapper(main)
