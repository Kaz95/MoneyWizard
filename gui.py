# Frontend using PyQt5 GUI library
# Uses MVC architecture pattern

import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUi
import bills
import debt
# Required for GUI to appear correctly on high DPI displays.
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# Each window will inherit from the QtWidgets.Dialog Class, except the main menu which inherits from QMainWindow
# Each window will call QWidget.__init__(self) during initialization
# Each window will use loadUi() on its respective .ui file to load the UI.
# TODO: !!! ALWAYS UPDATE A GIVEN WINDOWS __init__ WHEN ADDING, REMOVING, OR UPDATING WIDGETS !!!


# TODO: Figure out how to reuse regular expressions/validators.
class SharedWindowMethods:
    def __init__(self):
        is_digit_regex = QtCore.QRegExp("[0-9]+")
        self.is_digit_validator = QtGui.QRegExpValidator(is_digit_regex)

        is_alnum_regex = QtCore.QRegExp("[a-zA-Z0-9]+")
        self.is_alnum_validator = QtGui.QRegExpValidator(is_alnum_regex)

    # These methods will sling errors due to the way im using multiple inheritance
    def not_numeric_messagebox(self):
        QtWidgets.QMessageBox.critical(self, "Isn't Numeric", "Isn't Numeric")

    def not_alnum_messagebox(self):
        QtWidgets.QMessageBox.critical(self, "Isn't Alnum", "Isn't Alphanumeric")


class MenuWindow(QtWidgets.QMainWindow):
    payday_window_signal = QtCore.pyqtSignal()
    income_window_signal = QtCore.pyqtSignal()
    both_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.bills_btn = None
        self.debt_btn = None
        self.both_btn = None

        loadUi("menu.ui", self)

        # self.bills_btn = self.findChild(QtWidgets.QPushButton, "bills_btn")
        self.bills_btn.clicked.connect(self.switch_payday_window)
        self.debt_btn.clicked.connect(self.switch_income_window)
        self.both_btn.clicked.connect(self.emit_both_signal)

    def switch_payday_window(self):
        self.payday_window_signal.emit()

    def switch_income_window(self):
        self.income_window_signal.emit()

    def emit_both_signal(self):
        self.both_signal.emit()


class PayDayWindow(QtWidgets.QDialog, SharedWindowMethods):
    bills_window_signal = QtCore.pyqtSignal(object, object)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.add_btn = None
        self.done_btn = None
        self.date_line_edit = None
        self.amt_line_edit = None

        # TODO: p1 and p2 should be in bills.py and imported if/when needed.
        self.p1 = None
        self.p2 = None

        loadUi("payday.ui", self)

        self.done_btn.clicked.connect(self.switch_bills_window)
        self.add_btn.clicked.connect(self.add_payday)

        self.amt_line_edit.setValidator(self.is_digit_validator)
        self.amt_line_edit.inputRejected.connect(self.not_numeric_messagebox)

        self.date_line_edit.setValidator(self.is_digit_validator)
        self.date_line_edit.inputRejected.connect(self.not_numeric_messagebox)

    # def not_numeric_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Numeric", "Isn't Numeric")

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


class BillsWindow(QtWidgets.QDialog, SharedWindowMethods):
    bills_output_signal = QtCore.pyqtSignal(str)
    debt_window_signal = QtCore.pyqtSignal(str)

    pay_day_list = []
    bills_list = []

    def __init__(self, p1, p2, run_both=False):
        QtWidgets.QWidget.__init__(self)
        self.p1 = p1
        self.p2 = p2
        self.run_both = run_both

        self.output_text = None

        self.done_btn = None
        self.add_btn = None

        BillsWindow.pay_day_list.append(p1)
        BillsWindow.pay_day_list.append(p2)

        self.amt_line_edit = None
        self.date_line_edit = None
        self.name_line_edit = None

        loadUi("bills.ui", self)

        self.done_btn.clicked.connect(self.run_bills)
        self.done_btn.clicked.connect(self.switch_bills_output_window)

        self.add_btn.clicked.connect(self.add_bill)

        self.amt_line_edit.setValidator(self.is_digit_validator)
        self.amt_line_edit.inputRejected.connect(self.not_numeric_messagebox)

        self.date_line_edit.setValidator(self.is_digit_validator)
        self.date_line_edit.inputRejected.connect(self.not_numeric_messagebox)

        self.name_line_edit.setValidator(self.is_alnum_validator)
        self.name_line_edit.inputRejected.connect(self.not_alnum_messagebox)

    # def not_numeric_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Numeric", "Isn't Numeric")
    #
    # def not_alnum_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Alnum", "Isn't Alphanumeric")

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

    def switch_bills_output_window(self):
        self.bills_output_signal.emit(self.output_text)

    def run_bills(self):
        if self.run_both is False:
            self.output_text = bills.run(BillsWindow.pay_day_list, BillsWindow.bills_list, self.p1, self.p2)
            self.close()
        else:
            print("It wasn't false")
            self.switch_debt_window()


class BillsOutputWindow(QtWidgets.QDialog):

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.plainTextEdit = None
        loadUi("bills_output.ui", self)
        self.plainTextEdit.insertPlainText(text + "\n")


class IncomeWindow(QtWidgets.QDialog, SharedWindowMethods):
    debt_window_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.amt_line_edit = None
        self.done_btn = None
        loadUi("income.ui", self)

        self.done_btn.clicked.connect(self.switch_debt_window)

        self.amt_line_edit.setValidator(self.is_digit_validator)
        self.amt_line_edit.inputRejected.connect(self.not_numeric_messagebox)

    # def not_numeric_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Numeric", "Isn't Numeric")

    def switch_debt_window(self):
        self.debt_window_signal.emit(self.amt_line_edit.text())


class DebtWindow(QtWidgets.QDialog, SharedWindowMethods):
    debt_output_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, income):
        QtWidgets.QWidget.__init__(self)
        self.name_line_edit = None
        self.principal_line_edit = None
        self.interest_line_edit = None
        self.minimum_line_edit = None
        self.add_btn = None
        self.done_btn = None
        self.text1 = None
        self.text2 = None

        loadUi("debt.ui", self)
        print(f"Income: {income}")

        self.linked_list = debt.LinkedList()
        self.linked_list.income = int(income)

        self.add_btn.clicked.connect(self.add_debt)

        self.done_btn.clicked.connect(self.run)

        self.name_line_edit.setValidator(self.is_alnum_validator)
        self.name_line_edit.inputRejected.connect(self.not_alnum_messagebox)

        self.principal_line_edit.setValidator(self.is_digit_validator)
        self.principal_line_edit.inputRejected.connect(self.not_numeric_messagebox)

        # self.interest_line_edit.setValidator(is_digit_validator)
        # self.interest_line_edit.inputRejected.connect(self.not_numeric_messagebox)

        self.minimum_line_edit.setValidator(self.is_digit_validator)
        self.minimum_line_edit.inputRejected.connect(self.not_numeric_messagebox)

    # def not_numeric_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Numeric", "Isn't Numeric")
    #
    # def not_alnum_messagebox(self):
    #     QtWidgets.QMessageBox.critical(self, "Isn't Alnum", "Isn't Alphanumeric")

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
        self.linked_list.preserve_payoff_priority()
        self.text1 = self.linked_list.construct_debt_output()
        print(f"{self.linked_list.pay_shit()} month(s) till payoff")
        self.text2 = self.linked_list.construct_debt_output2()
        self.switch_debt_output_window()

    def switch_debt_output_window(self):
        self.debt_output_signal.emit(self.text1, self.text2)


class DebtOutputWindow(QtWidgets.QDialog):

    def __init__(self, text1, text2):
        QtWidgets.QWidget.__init__(self)
        loadUi("debt_output.ui", self)
        # Leaving this widget unnamed and undiscovered to show it still works
        self.plainTextEdit.insertPlainText(text1 + "\n")
        self.plainTextEdit.insertPlainText(text2 + "\n")


class Controller:
    def __init__(self):
        self.run_both = False
        self.menu = None
        self.payday = None
        self.bills = None
        self.income = None
        self.debt = None
        self.bills_output = None
        self.debt_output = None

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
        self.payday.bills_window_signal.connect(self.show_bills)
        self.payday.exec_()

    def show_bills(self, p1, p2):
        self.bills = BillsWindow(p1, p2, self.run_both)
        self.payday.close()
        self.bills.debt_window_signal.connect(self.show_debt)
        self.bills.bills_output_signal.connect(self.show_bills_output)
        self.bills.exec_()

    def show_bills_output(self, text):
        self.bills_output = BillsOutputWindow(text)
        self.bills.close()
        self.bills_output.exec_()

    def show_income(self):
        self.income = IncomeWindow()
        self.income.debt_window_signal.connect(self.show_debt)
        self.income.exec_()

    def show_debt(self, income):
        self.debt = DebtWindow(income)
        self.debt.debt_output_signal.connect(self.show_debt_output)
        if self.income is not None:
            self.income.close()
        else:
            self.bills.close()

        self.debt.exec_()

    def show_debt_output(self, text1, text2):
        self.debt_output = DebtOutputWindow(text1, text2)
        self.debt.close()
        self.debt_output.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
