import random
import database
import luhn_algorithm


conn = database.connect()
database.create_table(conn)


class BankAccount:

    def __init__(self):
        self.issuer_identification_number = "400000"
        self.customer_account_number = None
        self.checksum = None
        self.card_number = None
        self.pin = None
        self.balance = 0

    def card_details_generator(self):
        self.customer_account_number = "{:09d}".format(random.randint(0, 999999999))
        self.card_number = luhn_algorithm.append(self.issuer_identification_number + self.customer_account_number)
        self.pin = "{:04d}".format(random.randint(0, 9999))


def main_menu():
    user_input = input("1. Create an account\n2. Log into account\n0. Exit\n")
    if user_input == "1":
        create_account()
    elif user_input == "2":
        try_log_into_account()
    elif user_input == "0":
        exit_bye()
    else:
        print("Wrong input!")
        main_menu()


def exit_bye():
    print("\nBye!")
    return


def create_account():
    new_account = BankAccount()
    new_account.card_details_generator()
    database.insert_values(conn, new_account.card_number, new_account.pin)
    print("Your card has been created")
    print("Your card number:\n{}".format(new_account.card_number))
    print("Your card PIN:\n{}\n".format(new_account.pin))
    main_menu()


def try_log_into_account():
    card_number = input("\nEnter your card number:\n")
    card_pin = input("Enter your PIN:\n")
    accounts = database.get_all_accounts(conn)
    for account in accounts:
        if account[1] == card_number and account[2] == card_pin:
            print("You have successfully logged in!\n")
            in_account(account)
            return
    print("Wrong card number or PIN!\n")
    main_menu()


def in_account(account):
    user_input = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
    if user_input == "1":
        print("\nBalance: {}\n".format(account[3]))
        in_account(account)
    elif user_input == "2":
        add_income(account)
    elif user_input == "3":
        do_transfer(account)
    elif user_input == "4":
        close_account(account[1])
    elif user_input == "5":
        main_menu()
    elif user_input == "0":
        exit_bye()
    else:
        in_account(account)


def add_income(account):
    income = int(input("Enter income:\n"))
    database.change_balance(conn, income + account[3], account[1])
    in_account(database.get_needed_account_with_pin(conn, account[1], account[2]))


def do_transfer(account_from):
    card_number_to = input("Transfer\nEnter card number:\n")
    if not luhn_algorithm.verify(card_number_to):
        print("Probably you made a mistake in the card number. Please try again!")
        in_account(account_from)
    elif not database.get_account_by_number(conn, card_number_to):
        print("Such a card does not exist.")
        in_account(account_from)
    elif card_number_to == account_from[1]:
        print("You can't transfer money to the same account!")
        in_account(card_number_to)
    else:
        transfer_amount = int(input("Enter how much money you want to transfer:\n"))
        if account_from[3] < transfer_amount:
            print("Not enough money!\n")
            in_account(account_from)
        else:
            account_to_balance = database.get_account_by_number(conn, card_number_to)[3]
            database.do_transfer(conn, account_from[1], (account_from[3] - transfer_amount), card_number_to,
                                 (account_to_balance + transfer_amount))
            print("Success!\n")
            in_account(database.get_account_by_number(conn, account_from[1]))


def close_account(account_number):
    database.delete_account(conn, account_number)
    print("The account has been closed!")
    main_menu()


main_menu()
