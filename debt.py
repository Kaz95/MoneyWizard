class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.income = 0
        self.minimums = 0
        self.leftover = 0
        self.spillover = 0
        self.months_to_payoff = 0

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

    def print_list(self):
        temp = self.head
        while temp:
            print(temp.data.name)
            temp = temp.next

    def pay_shit(self):
        while self.head:
            cur = self.head
            prev = None
            while cur:
                # TODO: This is now ript
                if cur.data.principal <= 0:
                    if prev is None:
                        self.head = self.head.next
                        cur = self.head
                    else:
                        prev.next = cur.next
                        cur = cur.next
                else:
                    if cur == self.head:
                        cur.data.principal -= (cur.data.minimum + self.leftover + self.spillover)
                        self.spillover = 0
                        if cur.data.principal <= 0:
                            # TODO: This is the spillover area
                            p = 0 - cur.data.principal
                            self.spillover += p
                            self.leftover += cur.data.minimum
                            # TODO: Delete around here...ish
                    else:
                        cur.data.principal -= cur.data.minimum
                        if cur.data.principal <= 0:
                            # TODO: This is the spillover area
                            p = 0 - cur.data.principal
                            self.spillover += p
                            self.leftover += cur.data.minimum
                            # TODO: Delete around here...ish

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


# def count_minimums(some_list):
#     total = 0
#     for _ in some_list:
#         total += _.minimum
#     return total


def create_debt():
    name = input("Name:")
    principal = int(input("Principal:"))
    interest = int(input("Interest:"))
    minimum = int(input("Minimum:"))

    dboi = Debt(name, principal, interest, minimum)
    return dboi


# def fill_list(some_debt, some_list):
#     node = Node(some_debt)
#     if some_list.head is None:
#         some_list.head = node
#     else:
#         cur = some_list.head
#         prev = None
#
#         while cur is not None:
#             if node.data.interest < cur.data.interest:
#                 prev = cur
#                 cur = cur.next
#             elif prev is None:
#                 temp = some_list.head
#                 some_list.head = node
#                 some_list.head.next = temp
#                 break
#             else:
#                 prev.next = node
#                 prev.next.next = cur
#                 break
#
#         if cur is None:
#             if node.data.interest < prev.data.interest:
#                 prev.next = node
#             else:
#                 temp = some_list.head
#                 some_list.head = node
#                 some_list.head.next = temp


if __name__ == '__main__':

    d1 = Debt("credit card", 8, 4, 1)
    d2 = Debt("loan", 15, 3, 1)
    d3 = Debt("car", 7, 2, 1)
    d4 = Debt("Something", 3, 1, 1)

    # d1 = create_debt()
    # d2 = create_debt()
    # d3 = create_debt()

    linked_list = LinkedList()
    linked_list.income = 6
    linked_list.fill_list(d1)
    linked_list.fill_list(d2)
    linked_list.fill_list(d3)
    linked_list.fill_list(d4)

    linked_list.print_list()
    # print(linked_list.minimums)

    if linked_list.income > linked_list.minimums:
        linked_list.leftover = this_many = linked_list.income - linked_list.minimums
        print(f"You have {this_many} extra!")
    elif linked_list.income == linked_list.minimums:
        print("Just pay your minimums in order!")
    else:
        print("With ya broke ass.")

    print(f"{linked_list.pay_shit() - 1} month(s) till payoff")
