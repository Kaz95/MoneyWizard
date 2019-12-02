import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUi
import bills
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class Menu(QtWidgets.QMainWindow):
    payday_window_signal = QtCore.pyqtSignal()
    income_window_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("menu.ui", self)
        self.bills_btn = self.findChild(QtWidgets.QPushButton, "bills_btn")
        self.bills_btn.clicked.connect(self.switch_payday_window)

        self.debt_btn = self.findChild(QtWidgets.QPushButton, "debt_btn")
        self.debt_btn.clicked.connect(self.switch_income_window)

    def switch_payday_window(self):
        self.payday_window_signal.emit()

    def switch_income_window(self):
        self.income_window_signal.emit()


class PayDay(QtWidgets.QDialog):
    bills_window_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.date_line_edit = None
        self.amt_line_edit = None
        loadUi("payday.ui", self)
        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.bills_window_signal)

        self.add_btn = self.findChild(QtWidgets.QPushButton, "add_btn")
        self.add_btn.clicked.connect(self.add_payday)

    def switch_bills_window(self):
        self.bills_window_signal.emit()

    def add_payday(self):
        amount = self.amt_line_edit.text()
        date = self.date_line_edit.text()
        payday = bills.get_pay_day(amount, date)
        if bills.p1 is None:
            bills.p1 = payday
        else:
            bills.p2 = payday

        # TODO: Emit a signal to change page if both vars are filled.
        # TODO: Eliminates the user having to press "done" button.

        bills.pay_days_list.append(payday)
        self.amt_line_edit.clear()
        self.date_line_edit.clear()


class Bills(QtWidgets.QDialog):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
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
        bills.bills_list.append(bill)

        self.name_line_edit.clear()
        self.amt_line_edit.clear()
        self.date_line_edit.clear()

    def run_bills(self):
        bills.run(bills.pay_days_list, bills.bills_list, bills.p1, bills.p2)
        self.close()


class Income(QtWidgets.QDialog):
    debt_window_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("income.ui", self)
        self.done_btn = self.findChild(QtWidgets.QPushButton, "done_btn")
        self.done_btn.clicked.connect(self.switch_debt_window)

    def switch_debt_window(self):
        self.debt_window_signal.emit()


class Debt(QtWidgets.QDialog):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi("debt.ui", self)


class Controller:
    def __init__(self):
        pass

    def show_menu(self):
        self.menu = Menu()
        self.menu.payday_window_signal.connect(self.show_payday)
        self.menu.income_window_signal.connect(self.show_income)
        self.menu.show()

    def show_payday(self):
        self.payday = PayDay()
        self.menu.close()
        self.payday.bills_window_signal.connect(self.show_bills)
        self.payday.show()

    def show_bills(self):
        self.bills = Bills()
        self.payday.close()
        self.bills.show()

    def show_income(self):
        self.income = Income()
        self.menu.close()
        self.income.debt_window_signal.connect(self.show_debt)
        self.income.show()

    def show_debt(self):
        self.debt = Debt()
        self.income.close()
        self.debt.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
