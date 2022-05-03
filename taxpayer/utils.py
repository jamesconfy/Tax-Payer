from datetime import datetime, timedelta

class Tax:
    def __init__(self, annualsalary=1000000, stateTax=0, arrears=0, fines=0):
        #self.reg = registeredstate.lower()
        #self.curr = currentstate.lower()
        self.salary = annualsalary
        self.stateTax = stateTax
        self.arrears = arrears
        self.fines = fines

    def taxPayable(self):
        if self.salary < 250000:
            return 0 + self.stateTax + self.arrears + self.fines
        elif 250000 <= self.salary < 500000:
            CGST = 5 * (self.salary / 100)
            SGST = 5 * (self.salary / 100)
            totalTax = CGST + SGST + self.stateTax + self.arrears + self.fines
            return totalTax
        elif 500000 <= self.salary < 1000000:
            CGST = 20 * (self.salary / 100)
            SGST = 20 * (self.salary / 100)
            totalTax = CGST + SGST
            return totalTax + self.stateTax + self.arrears + self.fines
        elif 1000000 <= self.salary:
            CGST = 30 * (self.salary / 100)
            SGST = 30 * (self.salary / 100)
            totalTax = CGST + SGST
            return totalTax + self.stateTax + self.arrears + self.fines

def getDiff(date1, date2=datetime.utcnow()):
    delta = date2 - date1
    return delta.days

def getDate(days, date1=datetime.utcnow()):
    delta = date1 + timedelta(days)
    return delta.strftime("%d/%m/%Y")

# d1 = datetime(2021, 6, 12)
# # d2 = datetime(2022, 2, 21)
# year = getDiff(d1) // 365
# year1 = getDate(days=-60)
# print(f'Difference is {year1} year')

#james = Tax()
#print(james.taxPayable())