class PayDay:

    def __init__(self, amount, date):
        self.amount = amount
        self.date = date


class Bill:

    def __init__(self, name, amount, date):
        self.name = name
        self.amount = amount
        self.date = date


p1 = PayDay(1000, 5)
p2 = PayDay(500, 25)

b1 = Bill("Insurance", 200, 2)
b2 = Bill("Car", 500, 12)
b3 = Bill("House", 700, 28)

pay_days = [p1, p2]
bills = [b1, b2, b3]


def count_cash(some_list):
    total = 0

    for i in some_list:
        total += i.amount

    return total


pay_days_total = count_cash(pay_days)
bills_total = count_cash(bills)

left_over = pay_days_total - bills_total

if left_over > 0:
    print("You have enough money!")
    print(f"You have {left_over} left over")

pd1 = min(p1.date, p2.date)
pd2 = max(p1.date, p2.date)

middle = range(pd1, pd2)

pp1 = []
pp2 = []


def separate_bills():
    for b in bills:
        if b.date in middle:
            pp1.append(b)
        else:
            pp2.append(b)


separate_bills()


def print_bills(some_list):
    for i in some_list:
        print(i.name)


pp1sum = count_cash(pp1)
pp2sum = count_cash(pp2)

if p1.amount > pp1sum and p2.amount > pp2sum:
    print("I'm rich bitch!")

elif p1.amount < pp1sum:
    print(f"Save {pp1sum - p1.amount} from pp2")

else:
    print(f"Save {pp2sum - p2.amount} from pp1")





