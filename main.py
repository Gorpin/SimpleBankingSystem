import random


class BankAccount:

    all_accounts = []
    all_cans = []

    def __init__(self):
        self.issuer_identification_number = "400000"
        self.customer_account_number = None
        self.checksum = None
        self.card_number = None
        self.pin = None
        self.balance = 0
        BankAccount.all_accounts.append(self)

    def card_details_generator(self):
        self.customer_account_number = "{:09d}".format(random.randint(0, 999999999))
        if self.customer_account_number not in BankAccount.all_cans:
            BankAccount.all_cans.append(self.customer_account_number)
            self.card_number = self.issuer_identification_number + self.customer_account_number + self.calculate_checksum()
            self.pin = "{:04d}".format(random.randint(0, 9999))
        else:
            self.card_details_generator()

    def calculate_checksum(self):
        arr = list(self.issuer_identification_number + self.customer_account_number)
        digit_list = [int(i) for i in arr]
        helper = 0
        for i, num in enumerate(digit_list):
            if i % 2 == 0:
                if num * 2 > 9:
                    helper += num * 2 - 9
                else:
                    helper += num * 2
            else:
                helper += num
        return "0" if helper % 10 == 0 else str((helper // 10 + 1) * 10 - helper)


def main_menu():
    user_input = input("1. Create an account\n2. Log into account\n0. Exit\n")
    if user_input == "1":
        create_account()
    elif user_input == "2":
        try_log_into_account()
    elif user_input == "0":
        exit_bye()


def exit_bye():
    print("\nBye!")
    return


def create_account():
    new_account = BankAccount()
    new_account.card_details_generator()
    print("Your card has been created")
    print("Your card number:\n{}".format(new_account.card_number))
    print("Your card PIN:\n{}\n".format(new_account.pin))
    main_menu()


def try_log_into_account():
    card_number = input("\nEnter your card number:\n")
    card_pin = input("Enter your PIN:\n")
    for account in BankAccount.all_accounts:
        if account.card_number == card_number and account.pin == card_pin:
            print("You have successfully logged in!\n")
            in_account(BankAccount.all_accounts.index(account))
            return
    print("Wrong card number or PIN!\n")
    main_menu()


def in_account(account_index):
    user_input = input("1. Balance\n2. Log out\n0. Exit\n")
    if user_input == "1":
        print("\nBalance: {}\n".format(BankAccount.all_accounts[account_index].balance))
        in_account(account_index)
    elif user_input == "2":
        main_menu()
    elif user_input == "0":
        exit_bye()
    else:
        in_account(account_index)


main_menu()
