import sqlite3


CREATE_TABLE = """CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"""
CLEAR_TABLE = "DELETE FROM card;"
DROP_TABLE = "DROP TABLE card;"
INSERT_VALUES = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)"
GET_ALL_ACCOUNTS = "SELECT * FROM card;"
GET_NEEDED_ACCOUNT_WITH_PIN = "SELECT * FROM card WHERE number = ? AND pin = ?;"
GET_ACCOUNT_BY_NUMBER = "SELECT * FROM card WHERE number = ?"
GET_CANS = "SELECT"
CHANGE_BALANCE = "UPDATE card SET balance = ? WHERE number = ?"
DELETE_ACCOUNT = "DELETE FROM card WHERE number = ?"
DO_TRANSFER = """
UPDATE card SET balance = CASE number
                            WHEN ? THEN ?
                            WHEN ? THEN ?
                            END
WHERE number IN (?, ?)
"""


def connect():
    return sqlite3.connect("card.s3db")


def create_table(connection):
    with connection:
        connection.execute(CREATE_TABLE)


def insert_values(connection, number, pin, balance=0):
    with connection:
        connection.execute(INSERT_VALUES, (number, pin, balance))


def clear_table(connection):
    with connection:
        connection.execute(CLEAR_TABLE)


def drop_table(connection):
    with connection:
        connection.execute(DROP_TABLE)


def get_all_accounts(connection):
    with connection:
        return connection.execute(GET_ALL_ACCOUNTS).fetchall()


def get_needed_account_with_pin(connection, number, pin):
    with connection:
        return connection.execute(GET_NEEDED_ACCOUNT_WITH_PIN, (number, pin)).fetchone()


def get_account_by_number(connection, number):
    with connection:
        return connection.execute(GET_ACCOUNT_BY_NUMBER, (number,)).fetchone()


def change_balance(connection, balance, number):
    with connection:
        connection.execute(CHANGE_BALANCE, (balance, number))


def delete_account(connection, number):
    with connection:
        connection.execute(DELETE_ACCOUNT, (number,))


def do_transfer(connection, number_from, updated_balance_from, number_to, updated_balance_to):
    with connection:
        connection.execute(DO_TRANSFER, (number_from, updated_balance_from, number_to, updated_balance_to, number_from,
                                         number_to))
