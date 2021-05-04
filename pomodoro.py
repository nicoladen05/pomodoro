from time import sleep

class Pomodoro:
    def setTime(self, hours, minutes, seconds):
        self.seconds_total = seconds + minutes * 60 + hours * 3600

    # Main timer function
    def timer(self):
        while self.seconds_total > 0:
            self.seconds_total -= 1
            sleep(1)

    # Return the remaining pomodoro time
    def time(self):
        try:
            return self.seconds_total
        except AttributeError: # If the time isn't set yet
            return False

p = Pomodoro()
p.timer(0,0,3)
