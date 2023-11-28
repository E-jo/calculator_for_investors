import os.path
import sqlite3
import csv


def main_menu():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    while True:
        print(
            """MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria"""
        )
        try:
            menu_choice = int(input("Enter an option: "))
            if menu_choice == 0:
                print("Have a nice day!")
                cursor.close()
                conn.commit()
                conn.close()
                exit()
            elif menu_choice == 1:
                crud_menu()
            elif menu_choice == 2:
                top_ten_menu()
            else:
                print("Invalid option!")
        except ValueError:
            print("Invalid option!")


def crud_menu():
    print(
        """CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies"""
        )
    try:
        menu_choice = int(input("Enter an option: "))
        match menu_choice:
            case 0:
                main_menu()
            case 1:
                create_company()
            case 2:
                read_company()
            case 3:
                update_company()
            case 4:
                delete_company()
            case 5:
                list_all_companies()
            case _:
                print("Invalid option!")
    except ValueError:
        print("Invalid option!")


def top_ten_menu():
    print(
        """TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA"""
    )
    try:
        menu_choice = int(input("Enter an option: "))
        match menu_choice:
            case 0:
                main_menu()
            case 1:
                top_ten_nd_ebitda()
            case 2:
                top_ten_roe()
            case 3:
                top_ten_roa()
            case _:
                print("Invalid option!")
    except ValueError:
        print("Invalid option!")


def top_ten_nd_ebitda():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    select_statement = ("SELECT ticker, net_debt / ebitda "
                        "AS nd_ebitda FROM financial ORDER BY nd_ebitda DESC LIMIT 10")
    results = cursor.execute(select_statement)

    print("TICKER ND/EBITDA")
    for row in results:
        print(str(row[0]) + " " + str(round((row[1]), 2)))

    cursor.close()
    conn.close()


def top_ten_roe():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    select_statement = ("SELECT ticker, net_profit / equity "
                        "AS roe FROM financial ORDER BY roe DESC LIMIT 10")
    results = cursor.execute(select_statement)

    print("TICKER ROE")
    for row in results:
        print(str(row[0]) + " " + str(round((row[1]), 2)))

    cursor.close()
    conn.close()


def top_ten_roa():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    select_statement = ("SELECT ticker, net_profit / assets "
                        "AS roa FROM financial ORDER BY roa DESC LIMIT 10")
    results = cursor.execute(select_statement)

    print("TICKER ROA")
    for row in results:
        print(str(row[0]) + " " + str(round((row[1]), 2)))

    cursor.close()
    conn.close()


def create_db():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()
    create_table_companies = """
                            CREATE TABLE IF NOT EXISTS companies(
                                ticker TEXT PRIMARY KEY,
                                name TEXT,
                                sector TEXT
                            );
                            """

    create_table_financial = """
                            CREATE TABLE IF NOT EXISTS financial(
                                ticker TEXT PRIMARY KEY,
                                ebitda FLOAT,
                                sales FLOAT,
                                net_profit FLOAT,
                                market_price FLOAT,
                                net_debt FLOAT,
                                assets FLOAT,
                                equity FLOAT,
                                cash_equivalents FLOAT,
                                liabilities FLOAT
                            );
                            """

    cursor.execute(create_table_companies)
    cursor.execute(create_table_financial)

    conn.commit()
    cursor.close()
    conn.close()


def populate_companies():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    with open("companies.csv", newline='') as companies:
        file_reader = csv.reader(companies, delimiter=",")
        first_line = True
        for line in file_reader:
            if first_line:
                first_line = False
                continue
            for i in range(0, len(line)):
                if line[i] == "":
                    line[i] = None
            insert_statement = "INSERT INTO companies VALUES (?,?,?)"
            cursor.execute(insert_statement, (line[0], line[1], line[2],))

    conn.commit()
    cursor.close()
    conn.close()


def populate_financial():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    with open("financial.csv", newline='') as financial:
        file_reader = csv.reader(financial, delimiter=",")
        first_line = True
        for line in file_reader:
            if first_line:
                first_line = False
                continue
            for i in range(0, len(line)):
                if line[i] == "":
                    line[i] = None
            insert_statement = "INSERT INTO financial VALUES (?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(insert_statement, (line[0], line[1], line[2],line[3],
                                              line[4], line[5],line[6], line[7], line[8], line[9]))

    conn.commit()
    cursor.close()
    conn.close()


def create_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    data = []
    data.append(input("Enter ticker (in the format 'MOON'): "))
    data.append(input("Enter company (in the format 'Moon Corp'): "))
    data.append(input("Enter industries (in the format 'Technology'): "))
    data.append(input("Enter ebitda (in the format '987654321'): "))
    data.append(input("Enter sales (in the format '987654321'): "))
    data.append(input("Enter net profit (in the format '987654321'): "))
    data.append(input("Enter market price (in the format '987654321'): "))
    data.append(input("Enter net debt (in the format '987654321'): "))
    data.append(input("Enter assets (in the format '987654321'): "))
    data.append(input("Enter equity (in the format '987654321'): "))
    data.append(input("Enter cash equivalents (in the format '987654321'): "))
    data.append(input("Enter liabilities (in the format '987654321'): "))

    insert_companies = "INSERT INTO companies VALUES (?,?,?)"
    cursor.execute(insert_companies, (data[0], data[1], data[2],))
    insert_financial = "INSERT INTO financial VALUES (?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(insert_financial, (data[0], data[3], data[4], data[5],
                                      data[6], data[7], data[8], data[9], data[10], data[11],))
    conn.commit()
    cursor.close()
    conn.close()
    print("Company created successfully!")


def read_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    company_name = input("Enter company name: ")
    company_name = "%" + company_name + "%"
    company_query = "SELECT ticker, name FROM companies WHERE name LIKE (?)"
    results = cursor.execute(company_query, (company_name,))

    index = 0
    tickers = []
    names = []
    for row in results:
        tickers.append(row[0])
        names.append(row[1])
        print(str(index) + " " + row[1])
        index += 1

    if len(names) == 0:
        print("Company not found!")
        return

    try:
        company_choice = int(input("Enter company number: "))
        if company_choice not in range(0, len(names)):
            print("Invalid selection")
            return
    except ValueError:
        print("Invalid selection")
        return

    financial_query = "SELECT * FROM financial WHERE ticker LIKE (?)"
    results = cursor.execute(financial_query, (tickers[company_choice],))
    for row in results:
        print(tickers[company_choice] + " " + names[company_choice])
        try:
            p_e = row[4] / row[3]
            print("P/E = " + str(round(p_e, 2)))
        except TypeError:
            print("P/E = None")
        try:
            p_s = row[4] / row[2]
            print("P/S = " + str(round(p_s, 2)))
        except TypeError:
            print("P/S = None")
        try:
            p_b = row[4] / row[6]
            print("P/B = " + str(round(p_b, 2)))
        except TypeError:
            print("P/B = None")
        try:
            nd_ebitda = row[5] / row[1]
            print("ND/EBITDA = " + str(round(nd_ebitda, 2)))
        except TypeError:
            print("ND/EBITDA = None")
        try:
            roe = row[3] / row[7]
            print("ROE = " + str(round(roe, 2)))
        except TypeError:
            print("ROE = None")
        try:
            roa = row[3] / row[6]
            print("ROA = " + str(round(roa, 2)))
        except TypeError:
            print("ROA = None")
        try:
            l_a = row[9] / row[6]
            print("L/A = " + str(round(l_a, 2)))
        except TypeError:
            print("L/A = None")
    print()
    cursor.close()
    conn.close()


def update_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    company_name = input("Enter company name: ")
    company_name = "%" + company_name + "%"
    company_query = "SELECT ticker, name FROM companies WHERE name LIKE (?)"
    results = cursor.execute(company_query, (company_name,))

    index = 0
    tickers = []
    names = []
    for row in results:
        tickers.append(row[0])
        names.append(row[1])
        print(str(index) + " " + row[1])
        index += 1

    if len(names) == 0:
        print("Company not found!")
        return

    try:
        company_choice = int(input("Enter company number: "))
        if company_choice not in range(0, len(names)):
            print("Invalid selection")
            return
    except ValueError:
        print("Invalid selection")
        return

    data = []
    data.append(input("Enter ebitda (in the format '987654321'): "))
    data.append(input("Enter sales (in the format '987654321'): "))
    data.append(input("Enter net profit (in the format '987654321'): "))
    data.append(input("Enter market price (in the format '987654321'): "))
    data.append(input("Enter net debt (in the format '987654321'): "))
    data.append(input("Enter assets (in the format '987654321'): "))
    data.append(input("Enter equity (in the format '987654321'): "))
    data.append(input("Enter cash equivalents (in the format '987654321'): "))
    data.append(input("Enter liabilities (in the format '987654321'): "))

    financial_update = """
                            UPDATE financial
                            SET 
                                ebitda = (?),
                                sales = (?),
                                net_profit = (?),
                                market_price = (?),
                                net_debt = (?),
                                assets = (?),
                                equity = (?),
                                cash_equivalents = (?),
                                liabilities = (?)

                            WHERE ticker LIKE (?);
                            """
    cursor.execute(financial_update, (data[0], data[1], data[2],
                                                data[3], data[4], data[5], data[6], data[7],
                                                data[8], tickers[company_choice],))
    conn.commit()
    print("Company updated successfully!")


def delete_company():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    company_name = input("Enter company name: ")
    company_name = "%" + company_name + "%"
    company_query = "SELECT ticker, name FROM companies WHERE name LIKE (?)"
    results = cursor.execute(company_query, (company_name,))

    index = 0
    tickers = []
    names = []
    for row in results:
        tickers.append(row[0])
        names.append(row[1])
        print(str(index) + " " + row[1])
        index += 1

    if len(names) == 0:
        print("Company not found!")
        return

    try:
        company_choice = int(input("Enter company number: "))
        if company_choice not in range(0, len(names)):
            print("Invalid selection")
            return
    except ValueError:
        print("Invalid selection")
        return

    delete_company_statement = "DELETE FROM companies WHERE ticker LIKE (?)"
    cursor.execute(delete_company_statement, (tickers[company_choice],))
    delete_financial_statement = "DELETE FROM financial WHERE ticker LIKE (?)"
    cursor.execute(delete_financial_statement, (tickers[company_choice],))
    conn.commit()
    print("Company deleted successfully!")
    cursor.close()
    conn.commit()
    conn.close()


def list_all_companies():
    conn = sqlite3.connect("investor.db")
    cursor = conn.cursor()

    print("COMPANY LIST")
    select_all_companies = "SELECT * FROM companies ORDER BY ticker"
    results = cursor.execute(select_all_companies)
    for row in results:
        print(row[0] + " " + row[1] + " " + row[2])
    cursor.close()
    conn.commit()
    conn.close()


if not os.path.exists("investor.db"):
    create_db()
    populate_companies()
    populate_financial()

print("Welcome to the Investor Program!")

main_menu()



