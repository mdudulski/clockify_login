from datetime import timedelta

from polish_holiday import get_holidays


def checkifworkingday(today):
    if today.weekday() == 5 or today.weekday() == 6 or today in get_holidays(today.year):
        return False
    return True


def getlastworkingday(day):
    bool = True
    while bool is True:
        day = day - timedelta(days=1)
        if checkifworkingday(day) is True:
            bool = False
    return day.strftime('%Y-%m-%d')


