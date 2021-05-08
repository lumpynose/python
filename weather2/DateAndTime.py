import datetime

class DateToday():
    def __init__(self):
        self.today = datetime.datetime.now()

    def month(self):
        return self.today.strftime("%b")

    def date(self):
        return self.today.strftime("%d") + " " + self.today.strftime("%b")

    def dayOfWeek(self):
        return self.today.strftime("%a")

if __name__ == '__main__':
    dateToday = DateToday()
    print(dateToday.month())
    print(dateToday.date())
    print(dateToday.dayOfWeek())
