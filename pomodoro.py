from time import sleep

class Pomodoro:
    def __init__(self, breakCount):
        self.breakCount = breakCount

    def setTime(self, hours, minutes, seconds):
        self.seconds_total = seconds + minutes * 60 + hours * 3600 # calculate the total seconds in the given hours, minutes and seconds

    # Main timer function
    def timer(self):
        while True:
            while self.seconds_total > 0:
                self.seconds_total -= 1
                sleep(1)

    # Return the remaining pomodoro time
    def time(self):
        try:
            # changing the variable seconds_total won't change self.seconds_total
            seconds_total = self.seconds_total
            # calculate seconds_total back to readable time
            hours = round((seconds_total - seconds_total % 3600) / 3600)
            seconds_total -= hours * 3600
            minutes = round((seconds_total - seconds_total % 60) / 60)
            seconds_total -= minutes * 60
            seconds = round(seconds_total)

            if hours <= 9:
                hours = '0' + str(hours)
            if minutes <= 9:
                minutes = '0' + str(minutes)
            if seconds <= 9:
                seconds = '0' + str(seconds)

            if hours == '00': # If the hours are 0 hide them
                result = str(minutes) + ' : ' + str(seconds)
            else:
                result = str(hours) + ' : ' + str(minutes) + ' : ' + str(seconds)

            return result

        except AttributeError: # If the time isn't set yet, return False
            return False

    def plainTime(self): # Return the total remaining seconds
        return self.seconds_total

    def changeState(self): # Change the state depending on the previous state
        if self.state == 'study' and self.breakCount < 4:
            self.state = 'break'
            self.breakCount += 1
        elif self.state == 'study' and self.breakCount >= 4:
            self.state = 'longBreak'
            self.breakCount = 0
        else:
            self.state = 'study'

    def getState(self): # Get the current state
        return self.state

    def setState(self, state): # Set the state manually
        self.state = state

class Tasks:
    def addTask(self, task):
        with open(tasks, a) as tasks:
            tasks.write(task)
            tasks.close()

    def getTasks(self):
        with open(tasks, r) as tasks:
            return [task.rstrip() for task in tasks]
            tasks.close()
