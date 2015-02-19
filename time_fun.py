from datetime import date, timedelta
import getopt
from math import floor, e, log
from time import sleep
import sys


class Task(object):
    def __init__(self, arguments):
        try:
            self.opts, self.args = (getopt.getopt(arguments, "Y:M:D:h:m:s:v",
                                                  ["year=", "month=", "day=",
                                                   "hours=", "minutes",
                                                   "seconds=", "help",
                                                   "verbose"]))
        except getopt.GetoptError:
            Task.usage()
            sys.exit(2)

        # Makes list of all flags used
        self.flags = [self.opts[i][0] for i in range(0, len(self.opts))]
        if '--help' in self.flags:
            Task.help()

        self.get_start_date()
        self.get_stop_date()
        self.difference_in_dates = (self.start_date - self.stop_date).days

        self.get_task_length()

    @staticmethod
    def usage():
        print("usage: time_fun.py -Y <year> -M <month> -D <day> " +
              "-h <hours> -m <minutes> -s <seconds>")

    @staticmethod
    def help():
        print("Backward In Time")
        Task.usage()
        sys.exit(0)

    def get_start_date(self):
        self.start_date = date.today()
        days_in_start_year = Task.number_of_days(self.start_date.year)
        days_since_new_year = ((self.start_date -
                               date(self.start_date.year, 1, 1)).days)
        self.start_date_decimal = (self.start_date.year +
                                   (days_since_new_year/days_in_start_year))

    def get_stop_date(self):
        year = month = day = None
        for opt, arg in self.opts:
            if opt == "-Y":
                year = arg
            elif opt == "-M":
                month = arg
            elif opt == "-D":
                day = arg
        if year is None or month is None or day is None:
            Task.usage()
            sys.exit(2)
        try:
            for i in [year, month, day]:
                assert float(i) % 1 == 0 and int(i) > 0
            self.stop_date = date(int(year), int(month), int(day))
            if self.stop_date >= self.start_date:
                raise ValueError
        except AssertionError:
            print("Error: date inputs must be natural numbers.")
            sys.exit(2)
        except ValueError:
            print("Error: date out of range.")
            sys.exit(2)

    def get_task_length(self):
        hours, minutes, seconds = 0, 0, 0
        for opt, arg in self.opts:
            if opt == "-h":
                hours = arg
            elif opt == "-m":
                minutes = arg
            elif opt == "-s":
                seconds = arg
        try:
            for i in [hours, minutes, seconds]:
                assert float(i) % 1 == 0 and int(i) >= 0
            self.task_length = (int(hours) * 60**2 + int(minutes) * 60 +
                                int(seconds))
            if self.task_length == 0:
                print("Error: task length is required.")
                sys.exit(2)
        except (ValueError, AssertionError):
            print("Error: inputs must be whole numbers.")
            sys.exit(2)

    def progress(self):
        # exponent = ln(current-stop+e^3)-3
        self.exponent = log(self.difference_in_dates / 365.2425 + e**3) - 3
        for i in range(0, self.task_length+1):
            self.percentage = i / self.task_length
            self.get_in_progress_date()
            output = (str(self.get_readable_date()).ljust(10) +
                      (" (" + str(round(self.percentage*100, 2)) +
                      "%)").center(10))
            if "--verbose" in self.flags or "-v" in self.flags:
                output += (" (" + str(self.in_progress_date) + ")").rjust(20)
            print(output)
            sleep(1)

    def get_in_progress_date(self):
        # date = current - (e^(exponent*p^3+3)-e^3)
        self.in_progress_date = (self.start_date_decimal -
                                 (e**(self.exponent*self.percentage**3+3) -
                                  e**3))

    def get_readable_date(self):
        year = floor(self.in_progress_date)
        total_days = self.number_of_days(year)
        day = round((self.in_progress_date-year) * total_days)
        start_point = date(year, 1, 1)
        new_date = start_point + timedelta(days=day)
        return new_date

    @staticmethod
    def number_of_days(year):
        if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            return 366
        else:
            return 365


if __name__ == "__main__":
    user_task = Task(sys.argv[1:])
    user_task.progress()
