from math import floor, e, log
from time import sleep, strftime


class Date(object):
    months = {"January": 0, "February": 31, "March": 59,
              "April": 90, "May": 120, "June": 151,
              "July": 181, "August": 212, "September": 243,
              "October": 273, "November": 304, "December": 334}

    def __init__(self):
        # Start date
        day_of_year = int(strftime("%j"))
        year = int(strftime("%Y"))
        total_current_days = Date.number_of_days(year)
        self.current_date = year + day_of_year / total_current_days

        # Stop date
        year_stop = Date.stop_date_input("year", int)
        month_stop = Date.stop_date_input("month", str)
        day_stop = Date.stop_date_input("day", int)
        total_stop_days = Date.number_of_days(year_stop)
        if Date.months[month_stop] >= 59 and total_stop_days == 366:
            day_stop += 1
        self.stop_date = (year_stop +
                          (Date.months[month_stop]+day_stop) / total_stop_days)

        # Length of task
        hours = Date.get_number_of_seconds("hours", 2)
        minutes = Date.get_number_of_seconds("minutes", 1)
        seconds = Date.get_number_of_seconds("seconds", 0)
        self.length = hours + minutes + seconds

    def progress(self):
        self.exponent = log(self.current_date-self.stop_date+e**3) - 3
        for i in range(0, self.length+1):
            self.percentage = i / self.length
            self.get_date()
            print(str(self.convert_to_readable()) +
                  " (" + str(self.percentage*100) + "%)")
            sleep(1)

    @staticmethod
    def number_of_days(year):
        if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
            return 366
        else:
            return 365

    @staticmethod
    def stop_date_input(datetype, datatype):
        while True:
            try:
                value = (datatype(input("Enter the " + datetype +
                         " you wish to stop in: ")))
                if datetype == "month":
                    assert value in Date.months
            except (ValueError, AssertionError):
                pass
            else:
                return value

    @staticmethod
    def get_number_of_seconds(tUnit, exponent):
        while True:
            try:
                seconds = (int(input("Enter length of the task in " +
                           tUnit + ": ")))
                assert seconds % 1 == 0
            except (ValueError, AssertionError):
                print("Not a valid input.")
            else:
                return seconds * 60**exponent

    def get_date(self):
        self.dateInProgress = (self.current_date -
                               (e**(self.exponent*self.percentage**3+3)-e**3))

    def convert_to_readable(self):
        year = floor(self.dateInProgress)
        total_days = self.number_of_days(year)
        day = round((self.dateInProgress-year) * total_days)
        if day == 0:
            day = 31
            month = "December"
            year -= 1
            return month + " " + str(day) + ", " + str(year)

        # Finds name of month
        for i in sorted(list(Date.months.values()))[::-1]:
            if total_days == 366 and i >= 59:
                i += 1
            if i >= day:
                continue
            else:
                for j in Date.months:
                    # Second condition avoids '(month) 0' outputs
                    if Date.months[j] == i or Date.months[j] == i-1:
                        month = j
                        break
                break
        day -= Date.months[month]

        # Fix for leap years
        if total_days == 366 and Date.months[month] >= 59:
            day -= 1

        return month + " " + str(day) + ", " + str(year)


if __name__ == "__main__":
    userDate = Date()
    userDate.progress()
