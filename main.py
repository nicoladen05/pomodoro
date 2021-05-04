import curses
import pomodoro
from pyfiglet import Figlet

p = pomodoro.Pomodoro()

# Initialize curses
s = curses.initscr()

curses.noecho()

curses.cbreak()

s.keypad(True)

def main(s):
    s.clear()

    text = Figlet(font='standard')

    s.addstr(text.renderText(str(p.time())))

    s.refresh()
    s.getkey()

curses.wrapper(main)
