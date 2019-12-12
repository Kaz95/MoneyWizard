import unittest
import bills


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


class TestBills(unittest.TestCase):
    def setUp(self):
        self.b1 = bills.Bill("Insurance", 200, 2)
        self.b2 = bills.Bill("Car", 500, 12)
        self.b3 = bills.Bill("House", 700, 28)

        self.p1 = bills.PayDay(1000, 5)
        self.p2 = bills.PayDay(500, 25)

        self.bills = [self.b1, self.b2, self.b3]
        self.paydays = [self.p1, self.p2]

    def test_add_amounts(self):
        answer1 = bills.Bill.add_amounts(self.bills)
        answer2 = bills.Bill.add_amounts(self.paydays)
        self.assertEqual(answer1, 1400)
        self.assertEqual(answer2, 1500)

    def test_seperate_bills(self):
        a, b = bills.Bill.separate_bills(self.bills, range(5, 20))
        self.assertEqual(a, [self.b2])
        self.assertEqual(b, [self.b1, self.b3])


if __name__ == '__main__':
    unittest.main()
