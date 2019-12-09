# Console prototype for main bills function
# def test_run():
# #     # Creating paydays
# #     p1 = PayDay(1000, 5)
# #     p2 = PayDay(500, 25)
# #
# #     # Creating Bills
# #     b1 = Bill("Insurance", 200, 2)
# #     b2 = Bill("Car", 500, 12)
# #     b3 = Bill("House", 700, 28)
# #
# #     # Stuff all paydays and bills into their respective list.
# #     pay_days = [p1, p2]
# #     bills = [b1, b2, b3]
# #
# #     # Find totals
# #     paydays_sum = PayDay.add_amounts(pay_days)
# #     bills_sum = Bill.add_amounts(bills)
# #
# #     # Leftover will be the value passed to debt.py
# #     left_over = paydays_sum - bills_sum
# #
# #     # Decide if there is enough money overall
# #     if left_over < 0:
# #         print("You don't have enough money!")
# #     else:
# #         print("You have enough money!")
# #         print(f"You have {left_over} left over")
# #
# #         # Figure out which payday comes first in the month
# #         first_payday = min(p1.date, p2.date)
# #         second_payday = max(p1.date, p2.date)
# #
# #         middle = range(first_payday, second_payday)
# #         first_pay_period, second_pay_period = Bill.separate_bills(bills, middle)
# #
# #         # Total the amount of the bills for each pay period
# #         pp1sum = Bill.add_amounts(first_pay_period)
# #         pp2sum = Bill.add_amounts(second_pay_period)
# #
# #         # Logic that determines which pay period has a surplus, or if both do.
# #         if p1.amount > pp1sum and p2.amount > pp2sum:
# #             print("I'm rich bitch!")
# #
# #         elif p1.amount < pp1sum:
# #             print(f"Save {pp1sum - p1.amount} from pp2")
# #
# #         else:
# #             print(f"Save {pp2sum - p2.amount} from pp1")
# #
# #     return left_over
