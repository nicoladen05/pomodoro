from time import sleep

class Pomodoro:
    def setTime(self, hours, minutes, seconds):
        self.seconds_total = seconds + minutes * 60 + hours * 3600 # calculate the total seconds in the given hours, minutes and seconds

    # Main timer function
    def timer(self):
        while self.seconds_total > 0:
            self.seconds_total -= 1
            sleep(1)

    # Return the remaining pomodoro time
    def time(self):
        try:
            # calculate seconds_total back to readable time
            hours = round((self.seconds_total - self.seconds_total % 3600) / 3600)
            self.seconds_total -= hours * 3600
            minutes = round((self.seconds_total - self.seconds_total % 60) / 60)
            self.seconds_total -= minutes * 60
            seconds = round(self.seconds_total)

            if hours <= 9:
                hours = '0' + str(hours)
            if minutes <= 9:
                minutes = '0' + str(minutes)
            if seconds <= 9:
                seconds = '0' + str(seconds)

            if hours == '0': # If the hours are 0 hide them
                result = str(minutes) + ' : ' + str(seconds)
            else:
                result = str(hours) + ' : ' + str(minutes) + ' : ' + str(seconds)

            return result

        except AttributeError: # If the time isn't set yet, return False
            return False
