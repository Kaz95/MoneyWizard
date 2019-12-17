# Handles all debt related backend


class Debt:
    def __init__(self, name, principal, interest, minimum):
        self.name = name
        self.principal = principal
        self.interest = interest
        self.minimum = minimum

        self.interest_incurred = 0


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Purpose modified linked list class definition
class LinkedList:

    # TODO: Try to slim this down, or at least break into logical blocks. Look up a proper init
    def __init__(self):
        self.head = None
        self.income = 0  # The value that will eventually be passed from bills.py
        self.minimums = 0  # Total minimum payment of all debts. Used to calculate if enough money for minimums.
        self.leftover = 0   # L = (Income - minimums)
        self.temp_leftover = 0  # Used to hold leftover during actual iteration. Refilled at the start of each pass.
        self.months_to_payoff = 0   # ++ once per full pass of linked list

        # Used to keep track of which debts have been paid during a given pass.
        # Needed to decide if interest needs recalculating
        self.interest_already_paid_list = []

        self.pay_off_priority_list = []  # Used to preserve payoff priority for final debt output string
        self.pay_off_month_dictionary = {}  # Used to capture pay off month of each debt for output string

        self.need_refinance = None

    # Prepare cursors for list traversal
    # Start from head
    def prime_cursors(self):
        cur = self.head
        prev = None
        return cur, prev

    @staticmethod
    def move_cursors(cur):
        prev = cur
        cur = cur.next
        return cur, prev

    # Insert new head node
    def insert_new_head(self, node):
        temp = self.head
        self.head = node
        self.head.next = temp

    @staticmethod
    def manual_insertion(node, cur, prev):
        prev.next = node
        prev.next.next = cur

    # Fills linked list with debt object
    # Sorts objects into the list based on interest rate
    # Keeps running tally of minimums
    # TODO: Decide what to do if == interest rate. Need uniform behavior for testing.
    def auto_insert(self, some_debt):
        self.minimums += some_debt.minimum
        node = Node(some_debt)

        if self.head is None:
            self.head = node
        else:
            cur, prev = self.prime_cursors()
            while cur is not None:
                if node.data.interest < cur.data.interest:
                    cur, prev = LinkedList.move_cursors(cur)
                elif prev is None:
                    self.insert_new_head(node)
                    break
                else:
                    LinkedList.manual_insertion(node, cur, prev)
                    break

            if cur is None:
                if node.data.interest < prev.data.interest:
                    prev.next = node
                else:
                    self.insert_new_head(node)

    @staticmethod
    def find_spillover(principal):
        spillover = 0 - principal
        return spillover

    # Remove previously incurred interest in preparation for interest recalculation
    # Used when payment spills over into new node
    def prepare_recalc(self, spillover):
        self.head.data.principal -= self.head.data.interest_incurred
        self.head.data.principal -= spillover
        print(self.head.data.name, round(self.head.data.principal, 2))

    # Single function that calculates and incurs interest
    # Generates interest on head node by default unless a node is passes as param
    def generate_interest(self, cur=None):
        if cur:
            cur.data.interest_incurred = cur.data.principal * cur.data.interest
            if cur.data.interest_incurred > self.income:
                return True
            cur.data.principal += cur.data.interest_incurred
        else:
            self.head.data.interest_incurred = self.head.data.principal * self.head.data.interest
            if self.head.data.interest_incurred > self.income:
                return True
            self.head.data.principal += self.head.data.interest_incurred
            print(self.head.data.name, round(self.head.data.principal, 2))

    # Used to increased leftover amount after a give cursor is paid off.
    def add_to_leftover(self, cur):
        self.leftover += cur.data.minimum

    # Currently used to visually ensure list has been sorted correctly.
    def print_list(self):
        cur = self.head
        while cur:
            print(cur.data.name)
            cur = cur.next

    # Recursive function to handle spillover from paid off head node.
    def spill(self):
        if self.head.data.principal <= 0:
            spillover = LinkedList.find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                self.head.data.principal -= spillover
                print(self.head.data.name, round(self.head.data.principal, 2))
                self.spill()

    # TODO: Unittest
    # Recursive function to handle spillover from paid off cursor node.
    def special_spill_not_head(self, cur, prev):
        if cur.data.principal <= 0:
            spillover = LinkedList.find_spillover(cur.data.principal)
            prev.next = cur.next
            if self.head:
                self.prepare_recalc(spillover)

                if self.head.data.principal <= 0:
                    self.special_spill()
                else:
                    self.generate_interest()

    # TODO: Unittest
    # Handles a cursor node being paid off, and its spill over paying off the head node.
    # Only used within special_spill_not_head()
    def special_spill(self):
        if self.head.data.principal <= 0:
            spillover = LinkedList.find_spillover(self.head.data.principal)
            self.head = self.head.next
            if self.head:
                if self.head in self.interest_already_paid_list:
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
    def run_payoff(self):
        print(f"Minimums: {self.minimums}")
        if self.minimums > self.income:
            return "You don't have enough to cover minimums, refinance."
        self.leftover = self.income - self.minimums
        while self.head:
            cur, prev = self.prime_cursors()
            self.temp_leftover += self.leftover
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
                        self.need_refinance = self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid_list.append(cur)
                else:
                    cur.data.principal -= cur.data.minimum
                    if cur.data.principal <= 0:
                        print(cur.data.name, f"paid off in {self.months_to_payoff + 1} months(s)")
                        self.pay_off_month_dictionary[cur.data.name] = self.months_to_payoff + 1
                        self.add_to_leftover(cur)
                        self.special_spill_not_head(cur, prev)
                    else:
                        self.need_refinance = self.generate_interest(cur)
                        print(cur.data.name, round(cur.data.principal, 2))
                        self.interest_already_paid_list.append(cur)
                if self.need_refinance is True:
                    self.head = None
                    break
                cur, prev = LinkedList.move_cursors(cur)

            self.months_to_payoff += 1

        if self.need_refinance is True:
            return "Refinance, a debts interest is too high."
        print(self.pay_off_month_dictionary)
        return self.construct_debt_payoff_output()

    # Traverse list and append each node to a list
    def preserve_payoff_priority(self):
        cur = self.head
        while cur:
            self.pay_off_priority_list.append(cur)
            cur = cur.next

    # TODO: I'm not even commenting this until I clean it up.
    def construct_debt_priority_output(self):
        text = "Priority\n"
        count = 1
        for debt in self.pay_off_priority_list:
            text += (f"{count}.) " + debt.data.name + "\n")
            count += 1

        return text

    # TODO: Clean it up.
    def construct_debt_payoff_output(self):

        text = "Months to Payoff\n"

        for tup in self.pay_off_month_dictionary.items():
            temp = f"{tup[0]} - {tup[1]} months to payoff\n"
            text += temp

        return text


# Only used for exploratory testing. Remove at some point.
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
    linked_list.auto_insert(d1)
    linked_list.auto_insert(d2)
    linked_list.auto_insert(d3)
    linked_list.auto_insert(d4)

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
    print(linked_list.construct_debt_priority_output())
    print(f"{linked_list.run_payoff()} month(s) till payoff")
    print(linked_list.construct_debt_payoff_output())


if __name__ == '__main__':
    run()
