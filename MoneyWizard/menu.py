from MoneyWizard import bills
from MoneyWizard import debt


def show_menu_options():
    print("1.) Bills")
    print("2.) Debt")
    print("3.) Both")


def main():
    show_menu_options()
    answer = input("What do: ")
    if answer == "1":
        bills.run()
    elif answer == "2":
        debt.run()
    elif answer == "3":
        print("This shites under constructions")
        answer = input("Proceed anyway? ")
        if answer.upper() == "Y":
            left_over = bills.run()
            debt.run(left_over)
        else:
            pass
    else:
        print("Your answer is shite")
        main()


if __name__ == '__main__':
    main()
