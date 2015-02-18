from datetime import date, timedelta
from math import floor, e, log
from time import sleep


class Task(object):
    def __init__(self):
        self.get_start_date()
        self.get_stop_date()
        self.difference_in_dates = (self.start_date - self.stop_date).days

        self.get_task_length()

    def get_start_date(self):
        self.start_date = date.today()
        days_in_start_year = Task.number_of_days(self.start_date.year)
        days_since_new_year = ((self.start_date -
                               date(self.start_date.year, 1, 1)).days)
        self.start_date_decimal = (self.start_date.year +
                                   (days_since_new_year/days_in_start_year))

    def get_stop_date(self):
        self.stop_date = self.start_date + timedelta(days=1)
        while self.stop_date > self.start_date:
            try:
                self.stop_date = (date(self.stop_date_input("year"),
                                       self.stop_date_input("month"),
                                       self.stop_date_input("day")))
                if self.stop_date > self.start_date:
                    print("Invalid input: date is in the future.")
            except ValueError:
                print("Invalid input: one or more values out of range.")

    @staticmethod
    def stop_date_input(datetype):
        while True:
            try:
                value = (int(input("Enter the " + datetype +
                         " you wish to stop in: ")))
            except (ValueError):
                print("Invalid input: date must be a number.")
            else:
                return value

    def get_task_length(self):
        nums = []
        exponent = 2
        for t_unit in ["hours", "minutes", "seconds"]:
            while True:
                try:
                    seconds = (int(input("Enter length of the task in " +
                               t_unit + ": ")))
                    assert seconds % 1 == 0
                except (ValueError, AssertionError):
                    print("Invalid input: input must be an integer.")
                else:
                    nums.append(seconds * 60**exponent)
                    exponent -= 1
                    break
        self.task_length = sum(nums)

    def progress(self):
        # exponent = ln(current-stop+e^3)-3
        self.exponent = log(self.difference_in_dates / 365.2425 + e**3) - 3
        for i in range(0, self.task_length+1):
            self.percentage = i / self.task_length
            self.get_in_progress_date()
            print(str(self.get_readable_date()) +
                  " (" + str(self.percentage*100) + "%)")
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
    user_task = Task()
    user_task.progress()
