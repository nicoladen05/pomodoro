import curses
import pomodoro
import config
from threading import Thread
from pyfiglet import Figlet
from os import name
from time import time

if name == 'nt': # Import the right notification library depending on the os
    # Windows Notification
    from win10toast import ToastNotifier
    toast = ToastNotifier()
    def notification(text):
        toast.show_toast('Pomodoro', text, icon_path="assets/icon.ico")
elif name == 'posix':
        pass
else:
    # Linux Notifications
    from gi import require_version
    require_version('Notify', '0.7')
    from gi.repository import Notify
    Notify.init('Pomodoro')
    def notification(text):
        Notify.Notification.new('Pomodoro', text).show()

p = pomodoro.Pomodoro(config.shortBreakAmount)

# Initialize curses
s = curses.initscr()

curses.noecho()

curses.cbreak()

s.keypad(True)

s.scrollok(1)

# Set the starting time
p.setTime(config.studyTime[0], config.studyTime[1], config.studyTime[2])

class Discord:
    def __init__(self):
        if config.discordPresence:
            from pypresence import Presence
            dc_client_id = '839068702581456936'
            dc = Presence(dc_client_id)
            dc.connect()
    def discord_update(self, state, time):
        if config.discordPresence:
            self.unix = time() + self.time
            dc.update(large_image="main_icon", large_text="https://github.com/nicoladen05/pomodoro", state=self.state, end=self.unix) # Update the rich presence

# Set the starting state
p.setState('study')

def countdown():
    p.timer()

def main(s):
    countdown_thread.start() # Start the countdown thread
    #dc.update(large_image="main_icon", large_text="https://github.com/nicoladen05/pomodoro", state="Focusing...", end=time() + p.plainTime()) # Update the rich presence
    dc = Discord()
    dc.discord_update("Focusing...", time() + p.plainTime())
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
                    #dc.update(large_image="main_icon", large_text="https://github.com/nicoladen05/pomodoro", state="Focusing...", end=time() + p.plainTime()) # Update the rich presence
                    dc.discord_update("Focusing...", p.plainTime())
                elif p.getState() == 'break':
                    p.setTime(config.breakTime[0], config.breakTime[1], config.breakTime[2])
                    #dc.update(large_image="main_icon", large_text="https://github.com/nicoladen05/pomodoro", state="Taking a break", end=time() + p.plainTime()) # Update the rich presence
                    dc.discord_update("Taking a break", p.plainTime())
                elif p.getState() == 'longBreak':
                    p.setTime(config.longBreakTime[0], config.longBreakTime[1], config.longBreakTime[2])
                    #dc.update(large_image="main_icon", large_text="https://github.com/nicoladen05/pomodoro", state="Taking a long break", end=time() + p.plainTime()) # Update the rich presence
                    dc.discord_update("Taking a long break", p.plainTime())

                continue

            s.refresh() # Refresh the screen

            curses.napms(1000) # Sleep for one second
        except (KeyboardInterrupt, SystemExit):
            break
        except curses.error:
            print("Window too small")


countdown_thread = Thread(target=countdown) # Thread to countdown and show the time at the same time
countdown_thread.daemon = True

curses.wrapper(main) # Start the main curses ui
