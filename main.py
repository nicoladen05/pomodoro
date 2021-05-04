import curses
import pomodoro
from threading import Thread
from pyfiglet import Figlet
from os import name

if name == 'nt': # Import the right notification library depending on the os
    pass
else:
    from gi.repository import Notify # Linux notifications
    Notify.init('Pomodoro')
    def notification(text):
        Notify.Notification.new(text).show()

p = pomodoro.Pomodoro()

# Initialize curses
s = curses.initscr()

curses.noecho()

curses.cbreak()

s.keypad(True)

# Set the time for the pomodoro
p.setTime(0,0,10)

# Set the starting state
p.setState('study')

def countdown():
    p.timer()

def main(s):
    countdown_thread.start() # Start the countdown thread
    while True:
        s.clear() # Clear the screen
        text = Figlet(font='big')

        s.addstr(text.renderText(str(p.time()))) # Print the text which is converted to ascii art by figlet

        s.addstr(f'\n State: {p.getState()}')

        if p.plainTime() == 0: # Change the state after the countdown is finished
            notification(f'{p.getState().capitalize()} has finished!')

            s.addstr('\n Press any key to continue')
            s.getch()

            p.changeState() # Change the state to the next one

            if p.getState() == 'study':
                p.setTime(0,0,25)
            elif p.getState() == 'break':
                p.setTime(0,0,5)
            elif p.getState() == 'longBreak':
                p.setTime(0,0,15)

            continue

        curses.napms(1000) # Sleep for one second

        s.refresh() # Refresh the screen

countdown_thread = Thread(target=countdown) # Thread to countdown and show the time at the same time

curses.wrapper(main)
