import sqlite3
from datetime import date


COUNT_NUMBERS = 5


def get_soiskatel_number():
    connection = sqlite3.connect("numbers.db")

    cursor = connection.cursor()

    cursor.execute("select max(application_id), application_date  from Soiskatel")

    last_application = cursor.fetchone()

    connection.close()

    number_ap = str(last_application[0])
    date_ap = last_application[1]

    date_ap = date_ap.split("-")

    date_ap = f'{date_ap[1]}-{date_ap[0][2]}{date_ap[0][3]}'

    count_zero = COUNT_NUMBERS - len(number_ap)

    number = f'{"0" * count_zero}{number_ap}S/{date_ap}'

    return number
    

def update_soiskatel_number(number=None):
    connection = sqlite3.connect("numbers.db")

    cursor = connection.cursor()

    if number == None:
        cursor.execute('insert into Soiskatel (application_date) values (?)', (date.today(), ))
    else:
        cursor.execute('insert into Soiskatel (application_id, application_date) values (?, ?)', (number, date.today()))

    connection.commit()

    connection.close()


def get_employer_number():
    connection = sqlite3.connect("numbers.db")

    cursor = connection.cursor()

    cursor.execute("select max(application_id), application_date  from Employer")

    last_application = cursor.fetchone()

    connection.close()

    number_ap = str(last_application[0])
    date_ap = last_application[1]

    date_ap = date_ap.split("-")

    date_ap = f'{date_ap[1]}-{date_ap[0][2]}{date_ap[0][3]}'

    count_zero = COUNT_NUMBERS - len(number_ap)

    number = f'{"0" * count_zero}{number_ap}R/{date_ap}'

    return number


def update_employer_number(number=None):
    connection = sqlite3.connect("numbers.db")

    cursor = connection.cursor()

    if number == None:
        cursor.execute('insert into Employer (application_date) values (?)', (date.today(), ))
    else:
        cursor.execute('insert into Employer (application_id, application_date) values (?, ?)', (number, date.today()))

    connection.commit()

    connection.close()


def create_db():
    connection = sqlite3.connect("numbers.db")

    cursor = connection.cursor()

    cursor.execute('''
    create table Soiskatel (
    application_id integer primary key AUTOINCREMENT,
    application_date text          
    )
    ''')

    connection.commit()

    cursor.execute('''
    create table Employer (
    application_id integer primary key AUTOINCREMENT,
    application_date text          
    )
    ''')

    connection.commit()

    connection.close()