import csv
from datetime import datetime
#atttempting to load file given into list of dictionaries to facilitate the future use of CRUD
def load_transactions(filename):
    transactions = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try: 
                    date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    transaction_id = int(row['transaction_id'])
                    # checking for error in document it was a mistake looking at line number instead of transaction number
                    # if (transaction_id -1) != last_transaction_id:
                    #     with open('errors.txt', 'a', newline='') as errors:
                    #         writer = csv.DictWriter(errors, fieldnames=row.keys())
                    #         writer.writerow(row)
                    # last_transaction_id = transaction_id
                    customer_id = int(row['customer_id'])
                    amount = float(row['amount'])
                    transaction_type = row['type']
                    if transaction_type == 'debit':
                        amount = -amount
                    description = row['description']
                    transactions.append({
                        'transaction_id': transaction_id, 
                        # 'date': date.strftime('%Y-%m-%d'),
                        'date': date,
                        'customer_id': customer_id,
                        'amount': amount,
                        'transaction_type': transaction_type,
                        'description': description
                    })
                except(ValueError, KeyError) as e:
                    with open('errors.txt', 'a', newline='') as errors:
                        writer = csv.DictWriter(errors, fieldnames=row.keys())
                        writer.writerow(row)
                    print(f"{e} when converting from line in document")
                    continue
        return transactions
    except FileNotFoundError:
        print("File Not Found.")


# if __name__ == '__main__':
#     transactions = load_transactions('test.csv')
#     print(transactions[0])
#     # print(transactions[5])


def get_valid_input(prompt, cast_func):
    while True:
        try:
            value = cast_func(prompt)
            return value
        except Exception as e:
            print(f"Invalid input: {e}. Please try again.")


def add_transaction(transactions):
    transaction_id = max(int(t['transaction_id']) for t in transactions) + 1
    print(transaction_id)
    date = get_valid_input('Date: YYYY-MM-DD ', lambda x: datetime.strptime(x, '%Y-%m-%d')).date()
    customer_id = get_valid_input('Customer ID: ', int)
    amount = get_valid_input('Amount: ', float)
    while True:
        transaction_type = get_valid_input('Type of transaction: (credit, debit, transfer) ', str).strip().lower()
        if transaction_type not in {"credit", "debit", 'transfer'}:
            print('improper input Try again')
            continue
        break
    description = get_valid_input("Transaction Description: ", str)
    new_transaction = {
                        'transaction_id': transaction_id, 
                        'date': date,
                        'customer_id': customer_id,
                        'amount': amount,
                        'transaction_type': transaction_type,
                        'description': description
    }
    transactions.append(new_transaction)
    fieldnames =['transaction_id', 'date', 'customer_id', 'amount', 'transaction_type', 'description']
    with open('financial_transactions.csv', 'a', newline= '\n') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_transaction)
        print("transaction added!")


        
# if __name__ == '__main__':
#     add_transaction(transactions)


def filter_by_date(transactions: list[dict]):
    while True:
        try:
            filterDate = input("Input Date or date range (YYYY-MM-DD:(YYYY-MM-DD): ").strip()
            if ':' in filterDate:
                filterDate = filterDate.split(':')
                dateOne = datetime.strptime(filterDate[0], "%Y-%m-%d").date()
                # print(type(dateOne))
                # print(dateOne)
                dateTwo = datetime.strptime(filterDate[1], "%Y-%m-%d").date()
                # print(type(dateTwo))
                # print(dateTwo)
                filtered_list = []
                counter = 0
                for t in transactions:
                    t_date = t['date']
                    if counter < 1:
                        print(t_date)
                        print(type(t_date))
                        counter = 1
                    if dateOne < t_date < dateTwo:
                        filtered_list.append(t)
                return filtered_list
            else:
                filter_date = datetime.strptime(filterDate, "%Y-%m-%d").date()
                filtered = [t for t in transactions if t['date'] == filter_date]
                return filtered
        except Exception as e:
            print(f'Error {e}')


def filter_by_id(transactions: list[dict]):
    while True:
        try:
            filterId = input("Please type in Id number or Id number range (123-456): ").strip()
            if '-' in filterId:
                start, end = map(int, filterId.split('-'))
                filtered = [t for t in transactions if start <= int(t['transaction_id']) <= end]
            else:
                id_num = int(filterId)
                filtered = [t for t in transactions if int(t['transaction_id']) == id_num]
            transactions = filtered
            return transactions
        except Exception as e:
            print(f"error {e}")


def filter_by_customerid(transactions: list[dict]):
    while True:
        try:
            filterCustomerId = input("Input Customer ID or range of ID's seperate ranges with a semicolon : ")
            if ":" in filterCustomerId:
                start, end = map(int, filterCustomerId.split(':'))
                filtered = [t for t in transactions if start <= int(t['customer_id']) <= end]
            else:
                id_num = int(filterCustomerId)
                filtered = [t for t in transactions if t['customer_id'] == id_num]
            transactions = filtered
            return transactions
        except Exception as e:
            print(f'Error {e}')


def filter_by_type(transactions: list[dict]):
    while True:
        try:
            filterType = input("Please enter transaction Type to filter by: (credit, debit, transfer) ")
            filtered = [t for t in transactions if t['transaction_type'] == filterType.lower().strip()]
            if filterType not in {'credit', 'debit', 'transfer'}:
                print('Invalid Type')
                continue
            return filtered
        except Exception as e:
            print(f"Error {e}")


def filter_by_amount(transactions: list[dict]):
    while True:
        try:
            filterAmount = input("Please enter amount or amount range to filter by seperated by '-' :")
            if "-" in filterAmount:
                start, end = map(float, filterAmount.split('-'))
                filtered = [t for t in transactions if start <= t['amount'] <= end]
            else:
                amount_float = float(filterAmount)
                filtered = [t for t in transactions if t['amount'] == amount_float]
                transactions = filtered
            return filtered
        except Exception as e:
            print(f'error {e}')


def filter_list(transactions: list[dict]):
    while True:
         try:
            filterType = input("Filter option (ID, Date, CustomerId, Amount, Type, Description) or type exit to return full list ").strip().lower()
            match filterType:
                    case "id":
                        filtered_list = filter_by_id(transactions)
                        return filtered_list
                    case "date":
                        filtered_list = filter_by_date(transactions)
                        return filtered_list
                    case "customerid":
                        filtered_list = filter_by_customerid(transactions)
                        return filtered_list
                    case "amount":
                        filtered_list = filter_by_amount(transactions)
                        return filtered_list
                    case "type":
                        filtered_list = filter_by_type(transactions)
                        return filtered_list
                    case "exit":
                        return transactions
         except Exception as e:
             print(f'Error {e}')


def view_transactions(transactions: list[dict], check_filter: bool):
        if check_filter:
            while True:
                try:
                    choice = input("Would you like to filter list: (yes/no) ")
                    if choice.strip().lower().startswith('y'):
                        filtered = filter_list(transactions)
                        if filtered is not None:
                            transactions = filtered
                            break
                    else:
                        print("No filter applied or filter returned no results. Showing all transactions.")
                        break
                except Exception as e:
                    print(f'error {e}')
        try:
            columns = ['Trans #', 'Date', 'ID', 'Customer', 'Amount', 'Type', 'Description']

            data_rows = []
            # convert data to string to calculate length for formatting tables
            for idx, t in enumerate(transactions):
                data_rows.append([
                    str(idx +1),
                    t['date'].strftime('%Y-%m-%d'),
                    str(t['transaction_id']),
                    str(t['customer_id']),
                    str(t['amount']),
                    str(t.get('transaction_type', t.get('type', ''))),
                    str(t['description'])
                ])

            # Calculate column widths
            col_widths = [
                max(len(str(col)), *(len(row[i]) for row in data_rows))
                for i, col in enumerate(columns)
            ]

            fmt = " | ".join("{:<" + str(width) + "}" for width in col_widths)

            print(fmt.format(*columns))
            print("-" * (sum(col_widths) + 2 * (len(columns) - 1)))

            for row in data_rows:
                print(fmt.format(*row))
            answer = input("")
        except Exception as e:
            print(f'error {e}')



# if __name__ == '__main__':
#     view_transactions(transactions, True)


def display_options_and_get_choice(transactions):
    print("\nSmart Personal Finance Analyzer")
    print("1. Load Transactions")
    print("2. Add Transaction")
    print("3. View Transactions")
    print("4. Update Transaction")
    print("5. Delete Transaction")
    print("6. Analyze Finances")
    print("7. Save Transactions")
    print("8. Generate Report")
    print("9. Exit")
    choice = input("Select an option: ")
    return choice.strip().lower()


def check_choice(choice: str, transactions):
    try:
        match choice:
            case "1":
                transactions = load_transactions('test.csv')
            case "2":
                add_transaction(transactions)
            case "3":
                view_transactions(transactions, True)
            case "4":
                update_transaction(transactions)
            case "5":
                delete_transaction(transactions)
            case "6":
                analyze_finances(transactions)
            case "7":
                print("Under Construction")
            case "8":
                print("Under Construction")
            case "9":
                print("Exitting Program")
                return
    except Exception as e:
        print(f"Error {e}")


def main_menu(transactions):
    choice = ""
    while True:
        try:
            choice = display_options_and_get_choice(transactions)
            check_choice(choice, transactions)
            return choice
        except Exception as e:
            print(f"Error {e}")


def find_transaction(transactions: list[dict]):
    view_transactions(transactions, False)
    while True:
        try:
            transaction_num = int(input("Transaction Number to be updated or removed: ")) -1
            view_transactions([transactions[transaction_num]], False)
            return transaction_num
        except Exception as e:
            print(f"Error {e}")

# if __name__ == '__main__':
#     find_transaction(transactions)


def doublecheck(current_data):
    while True:
        change_answer = input(f'Would You like to change {current_data}: (yes/no) ')
        if change_answer.startswith('n'):
            return False
        if change_answer.startswith('y'):
            return True
        

def confirm_changes(current_data, new_data):
    while True:
        change_answer = input(f'Would You like to change {current_data} to {new_data}: (yes/no) ')
        if change_answer.startswith('n'):
            return False
        if change_answer.startswith('y'):
            return True
        

def update_transaction(transactions: list[dict]):
    transaction_num = find_transaction(transactions)
    while True:
        try:
            field_to_be_updated = input('Field to be updated: ')
            match field_to_be_updated:
                case "id":
                    print(transactions[transaction_num]['transaction_id'])
                    current_data = transactions[transaction_num]['transaction_id']
                    if doublecheck(current_data):
                        new_data = get_valid_input(input("new transaction id: "), int)
                        if confirm_changes(current_data, new_data):
                            transactions[transaction_num]['transaction_id'] = new_data
                    print(transactions[transaction_num]['transaction_id'])
                    break
                case "date":
                    print(transactions[transaction_num]['date'])
                    current_data = transactions[transaction_num]['date']
                    if doublecheck(current_data):
                        new_data = get_valid_input(input("new date: "), lambda x: datetime.strptime(x, '%Y-%m-%d')).date()
                        if confirm_changes(current_data, new_data):
                            transactions[transaction_num]['date'] = new_data
                    print(transactions[transaction_num]['date'])
                    break
                case "customer":
                    print(transactions[transaction_num]['customer_id'])
                    current_data = transactions[transaction_num]['customer_id']
                    if doublecheck(current_data):
                        new_data = get_valid_input(input("new customer id: "), int)
                        if confirm_changes(current_data, new_data):
                            transactions[transaction_num]['customer_id'] = new_data
                    print(transactions[transaction_num]['customer_id'])
                    break
                case "amount":
                    print(transactions[transaction_num]['amount'])
                    current_data = transactions[transaction_num]['amount']
                    if doublecheck(current_data):
                        new_data = get_valid_input(input("new amount: "), float)
                        if confirm_changes(current_data, new_data):
                            transactions[transaction_num]['amount'] = new_data
                    print(transactions[transaction_num]['amount'])
                    break
                case "type":
                    ## probably should have amount changed through transaction change
                    print(transactions[transaction_num]['transaction_type'])
                    current_data = transactions[transaction_num]['transaction_type']
                    if doublecheck(current_data):
                        while True:
                            new_data = input('new transaction type: (credit, debit, transfer) ')
                            if new_data not in ["credit", "debit", 'transfer']:
                                print('improper input Try again')
                                continue
                            break
                        if confirm_changes(current_data, new_data):
                            if new_data == 'debit':
                                transactions[transaction_num]['amount'] = abs(transactions[transaction_num]['amount'])
                            elif new_data == 'credit':
                                transactions[transaction_num]['amount'] = -abs(transactions[transaction_num]['amount'])
                            elif new_data == 'transfer':
                                transactions[transaction_num]['amount'] = abs(transactions[transaction_num]['amount'])
                            transactions[transaction_num]['transaction_type'] = new_data
                    print(transactions[transaction_num]['transaction_type'])
                    break
                case "description":
                    print(transactions[transaction_num]['description'])
                    current_data = transactions[transaction_num]['description']
                    if doublecheck(current_data):
                        new_data = get_valid_input(input("new description: "), str)
                        if confirm_changes(current_data, new_data):
                            transactions[transaction_num]['description'] = new_data
                    print(transactions[transaction_num]['description'])
                    break
                case default:
                    print("invalid input")
                    continue
        except Exception as e:
            print(f"error {e}")
            continue
# if __name__ == '__main__':
#     update_transaction(transactions)


def delete_transaction(transactions):
    while True:
        transaction_index = int(find_transaction(transactions))
        # view_transactions(transactions[transaction_index], False)
        answer = input("Are you sure you want to delete this transaction? ").lower().strip()
        if answer.startswith('y'):
            del transactions[transaction_index]
            load_transactions(transactions)
            print('transaction deleted.')
            break
        elif answer.startswith('n'):
            print('Returning to Main Menu... ')
            break

# if __name__ == '__main__':
#     delete_transaction(transactions)


def analyze_finances(transactions: list[dict]):
    try:
        ask = input("would you like to analyze a filtered list?").strip().lower()
        if ask.startswith('y'):
            transactions = filter_list(transactions)
        total_credits = sum(t['amount'] for t in transactions if t['transaction_type'] == 'credit')
        total_debits = sum(t['amount'] for t in transactions if t['transaction_type'] == 'debit')
        total_transfers = sum(t['amount'] for t in transactions if t['transaction_type'] == 'transfer')
        net_balance = sum(t['amount'] for t in transactions )
        print("Financial Summary: ")
        print(f"Total Credits: {total_credits:.2f}")
        print(f"Totla Debits: {total_debits:.2f}")
        print(f"Total Transfers: {total_transfers:.2f}")
        print(f"Net Balance: {net_balance:.2f}")
        print("By Type: ")
        print(f"\tCredit: {total_credits:.2f}")
        print(f"Debit: {total_debits:.2f}")
    except Exception as e:
        print(f"Error {e}")