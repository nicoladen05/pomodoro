from time import sleep
import threading

class Pomodoro:
    def timer(self, hours, minutes, seconds):
        self.seconds_total = seconds + minutes * 60 + hours * 3600
        while self.seconds_total > 0:
            print(self.seconds_total)
            self.seconds_total -= 1
            sleep(1)
        print("Done")

p = Pomodoro()
p.timer(0,0,10)
