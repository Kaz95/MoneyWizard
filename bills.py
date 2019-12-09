# Handles all bill related backend


class PayDay:

    def __init__(self, amount, date):
        self.amount = amount
        self.date = date

    @staticmethod
    def add_amounts(some_list):
        total = 0

        for obj in some_list:
            total += obj.amount

        return total


class Bill(PayDay):

    def __init__(self, name, amount, date):
        PayDay.__init__(self, name, amount)
        self.date = date

    @staticmethod
    def separate_bills(list_of_bills, middle_range):
        pp1 = []
        pp2 = []
        for bill in list_of_bills:
            if bill.date in middle_range:
                pp1.append(bill)
            else:
                pp2.append(bill)

        return pp1, pp2


# Create and return a PayDay object from user string input
def create_payday(amount, date):
    payday = PayDay(int(amount), int(date))
    return payday


# Create and return a Bill object from user string input
def create_bill(name, amount, date):
    bill = Bill(name, int(amount), int(date))
    return bill


# Console prototype for main bills function
# TODO: Move this once class/static methods.
def test_run():
    # Creating paydays
    p1 = PayDay(1000, 5)
    p2 = PayDay(500, 25)

    # Creating Bills
    b1 = Bill("Insurance", 200, 2)
    b2 = Bill("Car", 500, 12)
    b3 = Bill("House", 700, 28)

    # Stuff all paydays and bills into their respective list.
    pay_days = [p1, p2]
    bills = [b1, b2, b3]

    # Find totals
    paydays_sum = PayDay.add_amounts(pay_days)
    bills_sum = Bill.add_amounts(bills)

    # Leftover will be the value passed to debt.py
    left_over = paydays_sum - bills_sum

    # Decide if there is enough money overall
    if left_over < 0:
        print("You don't have enough money!")
    else:
        print("You have enough money!")
        print(f"You have {left_over} left over")

        # Figure out which payday comes first in the month
        first_payday = min(p1.date, p2.date)
        second_payday = max(p1.date, p2.date)

        middle = range(first_payday, second_payday)
        first_pay_period, second_pay_period = Bill.separate_bills(bills, middle)

        # Total the amount of the bills for each pay period
        pp1sum = Bill.add_amounts(first_pay_period)
        pp2sum = Bill.add_amounts(second_pay_period)

        # Logic that determines which pay period has a surplus, or if both do.
        if p1.amount > pp1sum and p2.amount > pp2sum:
            print("I'm rich bitch!")

        elif p1.amount < pp1sum:
            print(f"Save {pp1sum - p1.amount} from pp2")

        else:
            print(f"Save {pp2sum - p2.amount} from pp1")

    return left_over


# Parses a dictionary and uses value retrieved for text output.
# If passed False as a param, assumes not enough money.
def dict_to_output_string(some_dict):
    if some_dict:
        text = "You have enough!\n" \
               f"You have {some_dict['leftover']} leftover\n" \
               "Save some amount from some pay period. Fix ASAP"
    else:
        text = "You don't have enough!"

    return text


# Main bills function. Returns an pre-formatted output string.
def run(payday_list, bills_list, payday1, payday2):
    # Create a dictionary to hold values used for string output
    output_dictionary = {'leftover': None}

    # Find totals of each list of objects
    paydays_sum = PayDay.add_amounts(payday_list)
    bills_sum = Bill.add_amounts(bills_list)

    # Leftover will be the value passed to debt.py
    left_over = paydays_sum - bills_sum

    # Decide if there is enough money overall

    # Changing output_dictionary to False signifies not having enough money.
    if left_over < 0:
        print("You don't have enough money!")
        output_dictionary = False

    # If leftover is greater than 0 assign it as a value of its respective key.
    else:
        output_dictionary['leftover'] = left_over
        print("You have enough money!")
        print(f"You have {left_over} left over")

        # Figure out which payday comes first in the month
        # TODO: Almost certainly a better way to go about this.
        first_payday = min(payday1.date, payday2.date)
        second_payday = max(payday1.date, payday2.date)

        # Middle range will be the days covered by the first payday
        # All other days not in this range will be covered bt the second payday
        middle_range = range(first_payday, second_payday)
        # Separate the bills into two lists, each representing a given pay period
        first_pay_period, second_pay_period = Bill.separate_bills(bills_list, middle_range)

        # Total the amount of the bills for each pay period
        pp1sum = Bill.add_amounts(first_pay_period)
        pp2sum = Bill.add_amounts(second_pay_period)

        # TODO: This logic assumes that p1 is first payday of the month.
        # TODO: Fix ASAP, starting to get annoying.
        # Logic that determines which pay period has a surplus, or if both do.
        if payday1.amount > pp1sum and payday2.amount > pp2sum:
            print("I'm rich bitch!")
        elif payday1.amount < pp1sum:
            print(f"Save {pp1sum - payday1.amount} from pp2")
        else:
            print(f"Save {pp2sum - payday2.amount} from pp1")

    # Final bills output string
    output_string = dict_to_output_string(output_dictionary)
    return output_string


if __name__ == '__main__':
    test_run()
