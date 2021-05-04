import curses
import pomodoro
import config
from threading import Thread
from pyfiglet import Figlet
from os import name

if name == 'nt': # Import the right notification library depending on the os
    # Windows Notification
    from win10toast import ToastNotifier
    toast = ToastNotifier()
    def notification(text):
        toast.show_toast('Pomodoro', text, icon_path="icon.ico")
else:
    # Linux Notifications
    from gi import require_version
    require_version('Notify', '0.7')
    from gi.repository import Notify
    Notify.init('Pomodoro')
    def notification(text):
        Notify.Notification.new(text).show()

p = pomodoro.Pomodoro(config.shortBreakAmount)

# Initialize curses
s = curses.initscr()

curses.noecho()

curses.cbreak()

s.keypad(True)

s.scrollok(1)

# Set the starting time
p.setTime(config.studyTime[0], config.studyTime[1], config.studyTime[2])

# Set the starting state
p.setState('study')

def countdown():
    p.timer()

def main(s):
    countdown_thread.start() # Start the countdown thread
    while True:
        try:
            s.clear() # Clear the screen
            text = Figlet(font='big')
    
            s.addstr(text.renderText(str(p.time()))) # Print the text which is converted to ascii art by figlet
    
            s.addstr(f'\n State: {p.getState().capitalize()}') # Print the current state
    
            if p.plainTime() == 0: # Change the state after the countdown is finished
                notification(f'{p.getState().capitalize()} has finished!') # Send a notification
    
                s.addstr('\n Press any key to continue') # Wait for confirmation
                curses.flushinp()
                s.getch()
    
                p.changeState() # Change the state to the next one
    
                # Set the next timer length
                if p.getState() == 'study':
                    p.setTime(config.studyTime[0], config.studyTime[1], config.studyTime[2])
                elif p.getState() == 'break':
                    p.setTime(config.breakTime[0], config.breakTime[1], config.breakTime[2])
                elif p.getState() == 'longBreak':
                    p.setTime(config.longBreakTime[0], config.longBreakTime[1], config.longBreakTime[2])
    
                continue
    
            curses.napms(1000) # Sleep for one second
    
            s.refresh() # Refresh the screen
        except (KeyboardInterrupt, SystemExit):
            break
        except curses.error:
            print("Window too small")

    
countdown_thread = Thread(target=countdown) # Thread to countdown and show the time at the same time
countdown_thread.daemon = True

curses.wrapper(main) # Start the main curses ui
