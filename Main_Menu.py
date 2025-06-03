from PFA_Module import *

transactions = load_transactions('test.csv')
print(transactions)
while True:
    try:
        choice = main_menu(transactions)
    except Exception as e:
        print(f"Error {e}")