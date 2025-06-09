# Bank Simulator
# Version 2

#NEW FUNCTIONS
#Admin Menu
#Using text file to safe the account data.
#Asking users to enter their own balance.
#EASYGUI

import easygui as eg  # Import EasyGUI for graphical user interface elements
import json           # Import json to read/write data in JSON format
import os             # Import os to check if files exist
import random         # Import random for generating random card numbers

# Load account data from JSON file if it exists
def load_accounts():
    global account_data  # Use the global variable to access account data in other functions
    if os.path.exists('account_data.json'):  # Check if the file exists
        with open('account_data.json', 'r') as file:  # Open file in read mode
            account_data = json.load(file)  # Load JSON data into Python dictionary

account_data = []  # Initialize account data list
load_accounts()    # Load data from the file into account_data list

# Save current account data to JSON file
def save_accounts():
    with open("account_data.json", "w") as file:  # Open file in write mode
        json.dump(account_data, file, indent=4)   # Dump the account_data with indentation

# Admin login system using EasyGUI
def admin_login():

    while True:
        # Show a login box for admin with fields for username and pin
        login_details = eg.multpasswordbox("Enter Admin Credentials", "Admin Login", ["Username", "PIN"])
        if login_details is None:  # If user cancels
            return
        admin_user, admin_pin = login_details  # if admin_user and admin_pin equals to login_detalis user input
        if admin_user == 'admin' and admin_pin == '4695':  # Check credentials
            eg.msgbox("Access Granted", "Success")  # Show success message
            admin_menu()  # Open admin menu
            return 
        else:
            eg.msgbox("Access Denied", "Error")  # Show error message

# Admin menu interface
def admin_menu():
    while True:
        # Present admin options in a button box
        choice = eg.buttonbox("Choose an option:", "Admin Menu", ["View Accounts", "Edit Accounts", "Remove Account", "Exit"]) # Admin Options
        if choice == "View Accounts":
            view_accounts() # View All Accounts in the json file
        elif choice == "Edit Accounts":
            edit_accounts() # Edit all Accounts that are in the json file
        elif choice == "Remove Account":
            remove_accounts() # Remove Accounts that are in the json file
        elif choice == "Exit":
            return

# Display all user accounts
def view_accounts():
    if not account_data:  # If no accounts exist
        eg.msgbox("No accounts found.", "View Accounts")
        return
    all_accounts = ""  # Initialize a string to build the display
    for account in account_data:
        # Add each account's info to the string
        all_accounts += f"""
Card Number: {account['card number']}
Name: {account['first name']} {account['last name']}
Email: {account['email']}
PIN: {account['pin number']}
Balance: ${account['balance']:.2f}

"""
    # Display all account info in a textbox
    eg.textbox("All Accounts", "Account List", text=all_accounts)

# Admin edits an account's info
def edit_accounts():
    # Check if there are any accounts first
    if not account_data:
        eg.msgbox("No accounts found.", "Edit Account") # If there is no accounts in account data
        return

    # Show all current accounts
    view_accounts()

    # Ask user which account to edit
    card_input = eg.enterbox("Enter the card number of the account to edit:", "Edit Account") # Enter the card number of the one to edit
    if card_input is None:
        return

    # Loop through all accounts to find a match
    for account in account_data:
        if account['card number'] == card_input:
            # Let user choose what to edit
            choice = eg.buttonbox(
                f"Account Found: {account['first name']} {account['last name']} ({account['card number']})\n\n"
                "What would you like to edit?",
                "Edit Options",
                choices=["First Name", "Last Name", "Email", "PIN", "Cancel"] # What would they like to change?Dd
            )

            # Edit first name
            if choice == "First Name": # if user choice is first name
                new_first = eg.enterbox("Enter New First Name:", "Edit First Name")
                if new_first and new_first.isalpha(): # Making sure the first name consists of alphabetic characters
                    account['first name'] = new_first.strip().title()
                    eg.msgbox("First name updated.")
                else:
                    eg.msgbox("Invalid first name. Only letters allowed.") # If user enters numbers

            # Edit last name
            elif choice == "Last Name": # if user choice is last name
                new_last = eg.enterbox("Enter New Last Name:", "Edit Last Name")
                if new_last and new_last.isalpha(): # Making sure the first name consists of alphabetic characters
                    account['last name'] = new_last.strip().title()
                    eg.msgbox("Last name updated.")
                else:
                    eg.msgbox("Invalid last name. Only letters allowed.") # If user enters numbers 

            # Edit email
            elif choice == "Email": # if user choice is email
                new_email = eg.enterbox("Enter New Email (must contain '@' and '.'):", "Edit Email")
                if new_email and '@' in new_email and '.' in new_email: # Making sure email has '@' and '.'
                    account['email'] = new_email.strip().lower()
                    eg.msgbox("Email updated.")
                else:
                    eg.msgbox("Invalid email format.") # if '@' OR '1' is not inputed

            # Edit PIN
            elif choice == "PIN": # If user choice is PIN
                while True:
                    new_pin = eg.enterbox("Enter New 4-digit PIN:", "Edit PIN") # Enter new PIN Number
                    if new_pin is None:
                        break
                    if new_pin.isdigit() and len(new_pin) == 4: # if the pin .isdigit and is 4 digits long
                        account['pin number'] = int(new_pin)
                        eg.msgbox("PIN updated.")
                        break
                    else: 
                        eg.msgbox("Invalid PIN. Must be 4 digits.") # Making sure the PIN is 4 digits 

            elif choice == "Cancel":
                return

            save_accounts() # saving the changes made
            eg.msgbox("Account information updated successfully.") 
            return

    eg.msgbox("Account not found.")

# Admin removes an account
def remove_accounts():
    # Check if there are any accounts first
    if not account_data:
        eg.msgbox("No accounts found.", "Remove Account") # If there is no accounts in account data
        return

    # Show all current accounts
    view_accounts() # Shows user all accounts so they can make a choice

    # Ask user which account to remove
    card_input = eg.enterbox("Enter the card number of the account to remove:", "Remove Account") # Enter the card number 
    if card_input is None:
        return

    # Search and remove the matching account
    for account in account_data: 
        if account['card number'] == card_input: # This looks for the card number in account data
            full_name = f"{account['first name']} {account['last name']}"
            confirm = eg.ynbox(f"Are you sure you want to delete the account for:\n\n"
                                f"{full_name} ({account['card number']})?", # If the user is sure to delete the account from the system
                                "Confirm Delete")
            if confirm:
                account_data.remove(account)
                save_accounts()
                eg.msgbox("Account successfully removed.", "Success")  # if yes
            else:
                eg.msgbox("Account removal canceled.", "Cancelled") # if no
            return

    eg.msgbox("Account not found.", "Error")

# Login for users using pin
def login_sys():
    while True:
        choice = eg.buttonbox("Login Options:", "Login", choices=["Pin Number", "Exit"]) # If user would like to put in pin or exit
        if choice == "Pin Number":
            pinnum_input = eg.passwordbox("Enter your 4-digit PIN:", "Pin Login") # Pin number input 
            if not (pinnum_input and pinnum_input.isdigit() and len(pinnum_input) == 4): #Making sure it's number by using .isdigit and len(4) long
                eg.msgbox("PIN must be exactly 4 digits and numbers only.")
                continue

            pinnum_input = int(pinnum_input) # Converting string into integer
            for account in account_data:
                if account['pin number'] == pinnum_input: # Finding the pin number in account data  
                    eg.msgbox(f"Login Successful. Welcome {account['first name']} {account['last name']}!") # If found 
                    main_menu(account)
                    return
            eg.msgbox("PIN Number not found or invalid.") # If it's not found
        else:
            return # If anything else is pressed like 'exit', it will take you back to inital menu

# Generates a unique 5-digit card number
def generate_card_number():
    return ''.join(str(random.randint(0, 9)) for _ in range(5))

# Create a new bank account
def account_creation():
    while True:
        # Get first name
        first_name = eg.enterbox("Enter your first name:") # Enter First Name
        if first_name is None: # If nothing is entered goes back to inital menu
            return  # Return to initial menu
        # Get last name
        last_name = eg.enterbox("Enter your last name:") # Enter Last Name
        if last_name is None:
            return
        # Get email
        email_input = eg.enterbox("Enter New Email (must contain '@' and '.'):") # Enter email
        if email_input is None:
            return
        # Get PIN
        pin_input = eg.enterbox("Enter a 4-digit PIN number:") # Enter PIN 
        if pin_input is None:
            return

        # Validate inputs
        errors = []
        #This will handle muiliple errors at once
        if not all([first_name, last_name, email_input, pin_input]):
            errors.append("All fields must be filled.") # All fields must be filled
        if not (pin_input.isdigit() and len(pin_input) == 4):
            errors.append("PIN must be 4 digits and only numbers.") # Pin Invalid case
        if not first_name.isalpha() or not last_name.isalpha():
            errors.append("Names must contain only letters.") # Name Invalid Case
        if '@' not in email_input or '.' not in email_input:
            errors.append("Invalid email format.") #Email Invalid Case

        if errors:
            eg.msgbox("\n".join(errors), "Input Errors") #joins all cases and joins in a single string
            continue  # loop again


        pin_input = int(pin_input)

        # Check for duplicate email or pin from the account_data
        for account in account_data:
            if account['email'] == email_input:
                eg.msgbox("This email is already in use.")
                break
            if account['pin number'] == pin_input:
                eg.msgbox("This PIN is already in use.") 
                break
        else:
            # Get custom starting balance
            while True:
                balance_input = eg.enterbox("Enter your starting balance ($):", "Starting Balance") # Getting user balance for their account
                if balance_input is None:
                    return
                try:
                    balance = float(balance_input) # Converts string into float
                    if balance < 0:
                        eg.msgbox("Balance must be a non-negative number.") # balance must be not negative 
                        continue
                    break
                except ValueError:
                    eg.msgbox("Please enter a valid number.") # If user enters a word or an invalid case

            # Generate and save account
            card_number = generate_card_number()
            account_info = {
                'card number': card_number,
                'first name': first_name.title(),
                'last name': last_name.title(),
                'email': email_input.lower(),
                'pin number': pin_input,
                'balance': balance,
                'transactions': [f"Account opened with ${balance:.2f}"] # In the transaction menu they will see starting balance.
            }

            account_data.append(account_info)
            save_accounts()
            eg.msgbox(f"Account created!\nCard number: {card_number}\nStarting balance: ${balance:.2f}")
            return

# Deposit money into user's account
def deposit(account_info):
    while True:
        eg.msgbox(f"Current Balance: ${account_info['balance']:.2f}")
        amount_input = eg.enterbox("Enter amount to deposit:") # Ammount
        if amount_input is None:
            return
        try:
            dpt_amount = float(amount_input)
        except ValueError:
            eg.msgbox("Invalid amount.") # if the user enters an value error like words
            continue
        if dpt_amount <= 0:
            eg.msgbox("Amount must be greater than 0.") # if the amount that is equals to 0 or below
            continue

        # Reference
        add_ref = eg.buttonbox("Add a reference?", choices=["Yes", "No"])
        if add_ref == "Yes":
            ref = eg.enterbox("Enter reference:") or ""
            account_info['transactions'].append(f"Deposited ${dpt_amount:.2f} - {ref}") # The transaction made will append the deposit to the account_info{} 
        else:
            account_info['transactions'].append(f"Deposited ${dpt_amount:.2f}") # This is if the user didn't want a reference

        account_info['balance'] += dpt_amount #Adding deposit amount to balance
        save_accounts()
        eg.msgbox(f"Deposit successful. New balance: ${account_info['balance']:.2f}")
        again = eg.buttonbox("Another deposit?", choices=["Yes", "No"])
        if again != "Yes":
            return

# Withdraw money from user's account
def withdraw(account_info):
    while True:
        eg.msgbox(f"Current Balance: ${account_info['balance']:.2f}")
        amount_input = eg.enterbox("Enter amount to withdraw:") # Enter the amount to
        if amount_input is None:
            return
        try:
            wdr_amount = float(amount_input) # Converting string to a float 
        except ValueError:
            eg.msgbox("Invalid amount.") # If user enters words
            continue
        if wdr_amount <= 0:
            eg.msgbox("Amount must be greater than 0.") #Account balance must be over 0 to withdraw
            continue
        if wdr_amount > account_info['balance']:
            eg.msgbox("Insufficient funds.") # if withdraw ammount is greater than the balance
            continue

        # Refernece
        add_ref = eg.buttonbox("Add a reference?", choices=["Yes", "No"]) # If user would like to add an reference
        if add_ref == "Yes":
            ref = eg.enterbox("Enter reference:") or ""
            account_info['transactions'].append(f"Withdrew ${wdr_amount:.2f} - {ref}")  # The transaction made will append the withdrawal to the account_info{} 
        else:
            account_info['transactions'].append(f"Withdrew ${wdr_amount:.2f}") # This is if the user didn't want a reference

        account_info['balance'] -= wdr_amount 
        save_accounts() # Saving changes made
        eg.msgbox(f"Withdraw successful. New balance: ${account_info['balance']:.2f}") #Showing new balance
        again = eg.buttonbox("Another withdrawal?", choices=["Yes", "No"]) # If they would like to do another withdrawal
        if again != "Yes":
            return

# Show current balance to user
def check_balance(account_info):
    eg.msgbox(f"{account_info['first name']} {account_info['last name']} " # Account first name and last name
            f"({account_info['card number']})\n\nBalance: ${account_info['balance']:.2f}") # Showing the balance

# Show transaction history
def check_transactions(account_info):
    if not account_info['transactions']:
        eg.msgbox("No transactions found.") # If there are no transcations in transactions[]
    else: 
        eg.textbox("Transaction History", text="\n".join(account_info['transactions'])) #Transaction history

# Show exit message
def user_exit():
    eg.msgbox("Exiting...")

# User main menu after login
def main_menu(account_info):
    while True:
        choice = eg.buttonbox("Main Menu", choices=["Deposit", "Withdraw", "Check Balance", "Transaction History", "Exit" ]) # Main Menu Choices 
        if choice == "Deposit":
            deposit(account_info) # Deposit
        elif choice == "Withdraw":
            withdraw(account_info) # Withdraw
        elif choice == "Check Balance":
            check_balance(account_info) # Check Balance
        elif choice == "Transaction History":
            check_transactions(account_info) # Check Transcations 
        elif choice == "Exit":
            user_exit()
            break

# Main menu shown at the start of the program
def inital_menu():
    load_accounts()
    while True:
        choice = eg.buttonbox("Welcome to [Bank Name Here]", "Main Menu", choices=["Login", "Create Account", "Admin Login", "Exit"]) # The inital Menu

        #Inital Menu Choices:
        if choice == "Login":
            login_sys() # Login System
        elif choice == "Create Account":
            account_creation() # Account creation
        elif choice == "Admin Login":
            admin_login() # Admin Login
        elif choice == "Exit":
            user_exit() # User exits
            break

# Run the program
inital_menu()