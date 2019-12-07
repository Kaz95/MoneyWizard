# Static functions
def move_cursors(cur):
    prev = cur
    cur = cur.next
    return cur, prev


def insert(node, cur, prev):
    prev.next = node
    prev.next.next = cur


def find_spillover(principal):
    spillover = 0 - principal
    return spillover


# TODO: Variable names still mostly shit. Same with function names. Take another look when user input.
# TODO: Import this
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


# Purpose modified linked list class definition
# TODO: Consider importing linked list and inherit....something....look it up.
class LinkedList:

    def __init__(self):
        self.temp_leftover = 0  # Used to hold leftover during actual iteration. Refilled at the start of each pass.
        self.head = None
        self.income = 0     # The value that will eventually be passed from bills.py
        self.minimums = 0   # Total minimum payment of all debts. Used to calculate if enough money for mins.
        self.leftover = 0   # L = (Income - minimums)
        self.months_to_payoff = 0   # ++ once per full pass of linked list
        self.interest_already_paid = []
        self.pay_off_priority_list = []
        self.pay_off_month_dictionary = {}

    def prime_cursors(self):
        cur = self.head
        prev = None
        return cur, prev

    def insert_new_head(self, node):
        temp = self.head
        self.head = node
        self.head.next = temp

    def prepare_recalc(self, spillover):
        self.head.data.principal -= self.head.data.interest_incurred
        self.head.data.principal -= spillover
        print(self.head.data.name, round(self.head.data.principal, 2))

    def generate_interest(self, cur=None):
        if cur:
            cur.data.interest_incurred = cur.data.principal * cur.data.interest
            cur.data.principal += cur.data.interest_incurred
        else:
            self.head.data.interest_incurred = self.head.data.principal * self.head.data.interest
            self.head.data.principal += self.head.data.interest_incurred
            print(self.head.data.name, round(self.head.data.principal, 2))

    def add_to_leftover(self, cur):
        self.leftover += cur.data.minimum

    # Fills linked list with debt object
    # Sorts objects into the list based on interest rate
    # Keeps running tally of minimums
    # TODO: Decide what to do if == interest rate. Need uniform behavior for testing.
    def fill_list(self, some_debt):
        self.minimums += some_debt.minimum
        node = Node(some_debt)
        if self.head is None:
            self.head = node
        else:
            cur, prev = self.prime_cursors()
            while cur is not None:
                if node.data.interest < cur.data.interest:
                    cur, prev = move_cursors(cur)
                elif prev is None:
                    self.insert_new_head(node)
                    break
                else:
                    insert(node, cur, prev)
                    break

            if cur is None:
                if node.data.interest < prev.data.interest:
                    prev.next = node
                else:
                    self.insert_new_head(node)

    # Currently used to visually ensure list has been sorted correctly.
    # TODO: Unittest with setup/teardown...?
    def print_list(self):
        temp = self.head
        while temp:
            print(temp.data.name)
            temp = temp.next

    # Recursive function to handle spillover from paid off debts.
    def spill(self):
        if self.head.data.principal <= 0:
            spillover = find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                self.head.data.principal -= spillover
                print(self.head.data.name, round(self.head.data.principal, 2))
                self.spill()

    # TODO: Unittest
    def special_spill_not_head(self, cur, prev):
        if cur.data.principal <= 0:
            spillover = find_spillover(cur.data.principal)
            prev.next = cur.next
            if self.head:
                self.prepare_recalc(spillover)

                if self.head.data.principal <= 0:
                    self.special_spill()
                else:
                    self.generate_interest()

    # TODO: Unittest
    def special_spill(self):
        if self.head.data.principal <= 0:
            spillover = find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                if self.head in self.interest_already_paid:
                    self.prepare_recalc(spillover)

                    if self.head.data.principal <= 0:
                        self.special_spill()
                    else:
                        self.generate_interest()
                else:
                    self.head.data.principal -= spillover
                    # TODO: Might be able to do a normal spill here
                    self.special_spill()

    # Meat and potatoes function.
    # Iterates through linked list paying down principles and removing paid off nodes.
    # Keeps tracks of number of passes(months)
    # Leverages the spill() functions to handle spillover of paid debts.
    # Returns number of months till all debts are paid based on available information.
    def pay_shit(self):
        while self.head:
            cur, prev = self.prime_cursors()
            self.temp_leftover += self.leftover
            self.interest_already_paid = []
            while cur:
                if cur == self.head:
                    cur.data.principal -= (cur.data.minimum + self.temp_leftover)
                    self.temp_leftover = 0
                    if cur.data.principal <= 0:
                        self.add_to_leftover(cur)
                        self.spill()
                        print(cur.data.name, f"paid off in {self.months_to_payoff + 1} months(s)")
                        self.pay_off_month_dictionary[cur.data.name] = self.months_to_payoff + 1
                    else:
                        self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid.append(cur)
                else:
                    cur.data.principal -= cur.data.minimum
                    if cur.data.principal <= 0:
                        print(cur.data.name, f"paid off in {self.months_to_payoff + 1} months(s)")
                        self.pay_off_month_dictionary[cur.data.name] = self.months_to_payoff + 1
                        self.add_to_leftover(cur)
                        self.special_spill_not_head(cur, prev)
                    else:
                        self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid.append(cur)

                cur, prev = move_cursors(cur)

            self.months_to_payoff += 1

        print(self.pay_off_month_dictionary)
        return self.months_to_payoff

    def preserve_payoff_priority(self):
        cur = self.head
        while cur:
            self.pay_off_priority_list.append(cur)
            cur = cur.next

    def prepare_pay_shit(self):
        if self.income > self.minimums:
            self.leftover = this_many = self.income - self.minimums
            print(f"You have {this_many} extra!")
        elif self.income == self.minimums:
            print("Just pay your minimums in order!")
        else:
            print("With ya broke ass.")

    def construct_debt_output(self):
        text = "Priority\n"
        count = 1
        for i in self.pay_off_priority_list:
            text += (f"{count}.) " + i.data.name + "\n")
            count += 1

        return text

    def construct_debt_output2(self):

        text = "Months to Payoff\n"

        for i in self.pay_off_month_dictionary.items():
            temp = f"{i[0]} - {i[1]} months to payoff\n"
            text += temp

        return text


# TODO: Move this somewhere else....
class Debt:

    def __init__(self, name, principal, interest, minimum):
        self.name = name
        self.principal = principal
        self.interest = interest
        self.minimum = minimum
        self.interest_incurred = 0


# Prototype function for accepting user input and turning it into debt objects.
# TODO: Unittest
def create_debt(name, principal, interest, minimum):
    dboi = Debt(name, principal, interest, minimum)
    return dboi


def run(income=None):
    # Test debts
    d1 = Debt("credit card", 40, .04, 10)
    d2 = Debt("loan", 60, .03, 10)
    d3 = Debt("car", 20, .02, 10)
    d4 = Debt("Something", 100, .01, 10)

    linked_list = LinkedList()

    # TODO: Consider setting income somewhere else, or via user input.
    # TODO: Fix when user input
    if income:
        linked_list.income = income
    else:
        linked_list.income = 50

    # TODO: Find a better way to link the list.
    # TODO: Fix when user input
    # TODO: Unittest
    linked_list.fill_list(d1)
    linked_list.fill_list(d2)
    linked_list.fill_list(d3)
    linked_list.fill_list(d4)

    linked_list.print_list()
    # Logic that decides if there is enough money to cover mins.
    # TODO: You are currently finding & assigning leftover value here.
    # TODO: Fix when user input

    if linked_list.income > linked_list.minimums:
        linked_list.leftover = this_many = linked_list.income - linked_list.minimums
        print(f"You have {this_many} extra!")
    elif linked_list.income == linked_list.minimums:
        print("Just pay your minimums in order!")
    else:
        print("With ya broke ass.")

    linked_list.preserve_payoff_priority()
    print(linked_list.construct_debt_output())
    # Expecting pay_shit() to return an int value.
    print(f"{linked_list.pay_shit()} month(s) till payoff")
    print(linked_list.construct_debt_output2())


if __name__ == '__main__':
    run()
