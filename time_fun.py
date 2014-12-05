from math import floor, e, log
from time import sleep, strftime


def number_of_days(year):
    if(year % 4 == 0 and year % 100 != 0 or year % 400 == 0):
        return 366
    else:
        return 365


def get_date(current, stop, percentage):
    return current - (e**(get_exp(current, stop)*percentage**3+3)-e**3)


def get_exp(current, stop):
    return log(current-stop+e**3) - 3


def convert_to_readable(date):
    year = floor(date)
    total_days = number_of_days(year)
    day = round((date-year) * total_days)

    for i in sorted(list(months.values()))[::-1]:
        if total_days == 366 and i >= 59:
            i += 1
        if i >= day:
            continue
        else:
            for j in months:
                # Second condition avoids '(month) 0' outputs
                if months[j] == i or months[j] == i-1:
                    month = j
                    break
            break
    day -= months[month]

    # Fix for leap years
    if total_days == 366 and months[month] >= 59:
        day -= 1

    return month + " " + str(day) + ", " + str(year)


def get_number_of_seconds(increment, exponent):
    while True:
        try:
            seconds = (int(input("Enter length of the task in " + increment +
                       ": ")))
            assert seconds % 1 == 0
        except(ValueError, AssertionError):
            print("Not a valid input.")
        else:
            return seconds*60 ** exponent

if __name__ == "__main__":
    day_of_year = int(strftime("%j"))
    year = int(strftime("%Y"))
    total_current_days = number_of_days(year)

    current_date = year + day_of_year/total_current_days

    months = {"January": 0, "February": 31, "March": 59,
              "April": 90, "May": 120, "June": 151,
              "July": 181, "August": 212, "September": 243,
              "October": 273, "November": 304, "December": 334}

    # Main user input loop; gets stop year and percentage completed
    year_stop = 0
    month_stop = ""
    day_stop = 0
    while True:
        try:
            if not bool(year_stop):
                year_stop = int(input("Enter the year you wish to stop in: "))
            while month_stop not in months:
                month_stop = input("Enter the month you wish to stop in: ")
            if not bool(day_stop):
                day_stop = int(input("Enter the day you wish to stop in: "))
        except ValueError:
            continue
        else:
            total_stop_days = number_of_days(year_stop)
            if months[month_stop] >= 59 and total_stop_days == 366:
                day_stop += 1
            stop_date = (year_stop +
                         (months[month_stop]+day_stop)/total_stop_days)
            break

    hours = get_number_of_seconds("hours", 2)
    minutes = get_number_of_seconds("minutes", 1)
    seconds = get_number_of_seconds("seconds", 0)
    length = hours + minutes + seconds

    for i in range(0, length+1):
        percentage = i / length
        date = get_date(current_date, stop_date, percentage)
        print(str(convert_to_readable(date)) +
              " (" + str(percentage*100) + "%)")
        sleep(1)
