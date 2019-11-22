# TODO: Variable names still mostly shit. Same with function names. Take another look when user input.
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


# Purpose modified linked list class definition
class LinkedList:

    def __init__(self):
        self.temp_leftover = 0  # Used to hold leftover during actual iteration. Refilled at the start of each pass.
        self.head = None
        self.income = 0     # The value that will eventually be passed from bills.py
        self.minimums = 0   # Total minimum payment of all debts. Used to calculate if enough money for mins.
        self.leftover = 0   # L = (Income - minimums)
        self.months_to_payoff = 0   # ++ once per full pass of linked list

    # Fills linked list with debt object
    # Sorts objects into the list based on interest rate
    # Keeps running tally of minimums
    def fill_list(self, some_debt):
        self.minimums += some_debt.minimum
        node = Node(some_debt)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            prev = None

            while cur is not None:
                if node.data.interest < cur.data.interest:
                    prev = cur
                    cur = cur.next
                elif prev is None:
                    temp = self.head
                    self.head = node
                    self.head.next = temp
                    break
                else:
                    prev.next = node
                    prev.next.next = cur
                    break

            if cur is None:
                if node.data.interest < prev.data.interest:
                    prev.next = node
                else:
                    temp = self.head
                    self.head = node
                    self.head.next = temp

    # Currently used to visually ensure list has been sorted correctly.
    def print_list(self):
        temp = self.head
        while temp:
            print(temp.data.name)
            temp = temp.next

    # Recursive function to handle spillover from paid off debts.
    def spill(self):
        if self.head.data.principal <= 0:
            spillover = 0 - self.head.data.principal
            self.head = self.head.next
            if self.head:
                self.head.data.principal -= spillover
                self.spill()

    # Slightly altered recursive function that handles nodes that are not currently the "head" node.
    # TODO: Seriously consider reworking these functions into a single function.....or renaming...or something.
    def spill_not_head(self, cur, prev):
        if cur.data.principal <= 0:
            spillover = 0 - cur.data.principal
            prev.next = cur.next
            if self.head:
                self.head.data.principal -= spillover
                self.spill()

    # Meat and potatoes function.
    # Iterates through linked list paying down principles and removing paid off nodes.
    # Keeps tracks of number of passes(months)
    # Leverages the spill() functions to handle spillover of paid debts.
    # Returns number of months till all debts are paid based on available information.
    def pay_shit(self):
        while self.head:
            cur = self.head
            prev = None
            self.temp_leftover += self.leftover
            while cur:
                if cur == self.head:
                    cur.data.principal -= (cur.data.minimum + self.temp_leftover)
                    self.temp_leftover = 0
                    if cur.data.principal <= 0:
                        self.leftover += cur.data.minimum
                        self.spill()
                else:
                    cur.data.principal -= cur.data.minimum
                    if cur.data.principal <= 0:
                        self.leftover += cur.data.minimum
                        self.spill_not_head(cur, prev)

                prev = cur
                cur = cur.next

            self.months_to_payoff += 1

        return self.months_to_payoff


class Debt:

    def __init__(self, name, principal, interest, minimum):
        self.name = name
        self.principal = principal
        self.interest = interest
        self.minimum = minimum


# Prototype function for accepting user input and turning it into debt objects.
def create_debt():
    name = input("Name:")
    principal = int(input("Principal:"))
    interest = int(input("Interest:"))
    minimum = int(input("Minimum:"))

    dboi = Debt(name, principal, interest, minimum)
    return dboi


if __name__ == '__main__':

    # Test debts
    d1 = Debt("credit card", 28, 4, 2)
    d2 = Debt("loan", 17, 3, 2)
    d3 = Debt("car", 12, 2, 2)
    d4 = Debt("Something", 22, 1, 2)

    linked_list = LinkedList()

    # TODO: Consider setting income somewhere else, or via user input.
    # TODO: Fix when user input
    linked_list.income = 11

    # TODO: Find a better way to link the list.
    # TODO: Fix when user input
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

    # Expecting pay_shit() to return an int value.
    print(f"{linked_list.pay_shit()} month(s) till payoff")
