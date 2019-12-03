import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
import bills
import debt
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class MenuWindow(QtWidgets.QMainWindow):
    payday_window_signal = QtCore.pyqtSignal()
    income_window_signal = QtCore.pyqtSignal()
    both_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("menu.ui", self)
        self.bills_btn = self.findChild(QtWidgets.QPushButton, "bills_btn")
        self.bills_btn.clicked.connect(self.switch_payday_window)

        self.debt_btn = self.findChild(QtWidgets.QPushButton, "debt_btn")
        self.debt_btn.clicked.connect(self.switch_income_window)

        self.both_btn = self.findChild(QtWidgets.QPushButton, "both_btn")
        self.both_btn.clicked.connect(self.emit_both_signal)

    def switch_payday_window(self):
        self.payday_window_signal.emit()

    def switch_income_window(self):
        self.income_window_signal.emit()

    def emit_both_signal(self):
        self.both_signal.emit()


# TODO: Re-write with signals emitting object variables.
class PayDayWindow(QtWidgets.QDialog):
    bills_window_signal = QtCore.pyqtSignal(object, object)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.date_line_edit = None
        self.amt_line_edit = None
        self.p1 = None
        self.p2 = None
        loadUi("payday.ui", self)
        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.switch_bills_window)

        self.add_btn = self.findChild(QtWidgets.QPushButton, "add_btn")
        self.add_btn.clicked.connect(self.add_payday)

    def switch_bills_window(self):
        self.bills_window_signal.emit(self.p1, self.p2)

    def add_payday(self):
        amount = self.amt_line_edit.text()
        date = self.date_line_edit.text()
        payday = bills.get_pay_day(amount, date)
        if self.p1 is None:
            self.p1 = payday
        else:
            self.p2 = payday
            self.switch_bills_window()

        self.amt_line_edit.clear()
        self.date_line_edit.clear()


# TODO: Re-write as slots for object signals
class BillsWindow(QtWidgets.QDialog):

    debt_window_signal = QtCore.pyqtSignal(str)

    pay_day_list = []
    bills_list = []

    def __init__(self, p1, p2, run_both=False):
        QtWidgets.QWidget.__init__(self)
        self.p1 = p1
        self.p2 = p2
        self.run_both = run_both

        BillsWindow.pay_day_list.append(p1)
        BillsWindow.pay_day_list.append(p2)

        self.amt_line_edit = None
        self.date_line_edit = None
        self.name_line_edit = None
        loadUi("bills.ui", self)

        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.run_bills)

        self.add_btn = self.findChild(QtWidgets.QPushButton, "add_btn")
        self.add_btn.clicked.connect(self.add_bill)

    def add_bill(self):
        name = self.name_line_edit.text()
        amount = self.amt_line_edit.text()
        date = self.date_line_edit.text()

        bill = bills.get_bill(name, amount, date)
        BillsWindow.bills_list.append(bill)

        self.name_line_edit.clear()
        self.amt_line_edit.clear()
        self.date_line_edit.clear()

    def switch_debt_window(self):
        left_over = bills.run(BillsWindow.pay_day_list, BillsWindow.bills_list, self.p1, self.p2)
        left_over = str(left_over)
        self.debt_window_signal.emit(left_over)

    def run_bills(self):
        if self.run_both is False:
            bills.run(BillsWindow.pay_day_list, BillsWindow.bills_list, self.p1, self.p2)
            self.close()
        else:
            print("It wasn't false")
            self.switch_debt_window()


class IncomeWindow(QtWidgets.QDialog):
    debt_window_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.amt_line_edit = None
        loadUi("income.ui", self)
        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.switch_debt_window)

    def switch_debt_window(self):
        self.debt_window_signal.emit(self.amt_line_edit.text())


class DebtWindow(QtWidgets.QDialog):

    def __init__(self, income):
        QtWidgets.QWidget.__init__(self)
        self.name_line_edit = None
        self.principal_line_edit = None
        self.interest_line_edit = None
        self.minimum_line_edit = None
        loadUi("debt.ui", self)
        print(f"Income: {income}")
        self.linked_list = debt.LinkedList()
        self.linked_list.income = int(income)

        self.add_btn = self.findChild(QtWidgets.QPushButton, "add_btn")
        self.add_btn.clicked.connect(self.add_debt)

        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.run)

    def add_debt(self):
        name = self.name_line_edit.text()
        principal = int(self.principal_line_edit.text())
        interest = float(self.interest_line_edit.text())
        minimum = int(self.minimum_line_edit.text())

        some_debt = debt.Debt(name, principal, interest, minimum)
        self.linked_list.fill_list(some_debt)

        self.name_line_edit.clear()
        self.principal_line_edit.clear()
        self.interest_line_edit.clear()
        self.minimum_line_edit.clear()

    def run(self):
        self.linked_list.prepare_pay_shit()
        print(f"{self.linked_list.pay_shit()} month(s) till payoff")
        self.close()


class Controller:
    def __init__(self):
        self.run_both = False
        self.menu = None
        self.payday = None
        self.bills = None
        self.income = None
        self.debt = None

    def change_run_both(self):
        self.run_both = True
        print(self.run_both)

    def show_menu(self):
        self.menu = MenuWindow()
        self.menu.both_signal.connect(self.change_run_both)
        self.menu.both_signal.connect(self.show_payday)
        self.menu.payday_window_signal.connect(self.show_payday)
        self.menu.income_window_signal.connect(self.show_income)
        self.menu.show()

    def show_payday(self):
        self.payday = PayDayWindow()
        self.menu.close()
        self.payday.bills_window_signal.connect(self.show_bills)
        self.payday.show()

    def show_bills(self, p1, p2):
        self.bills = BillsWindow(p1, p2, self.run_both)
        self.payday.close()
        self.bills.debt_window_signal.connect(self.show_debt)
        self.bills.show()

    def show_income(self):
        self.income = IncomeWindow()
        self.menu.close()
        self.income.debt_window_signal.connect(self.show_debt)
        self.income.show()

    def show_debt(self, income):
        self.debt = DebtWindow(income)
        if self.income is not None:
            self.income.close()
        else:
            self.bills.close()
        self.debt.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
