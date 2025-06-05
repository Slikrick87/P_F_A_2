from PFA_Module import *
file = "test.csv"
print("If you'd like to just use the test file please select No below.")
answer = input("Would you like to enter a csv file to use in program? (Yes/No)").strip().lower()
if answer.startswith("y"):
    file = input("name of csv file containing financial transactions: ")
transactions = load_transactions(file)
# print(transactions)
while True:
    try:
        choice = main_menu(transactions)
    except Exception as e:
        print(f"Error {e}")