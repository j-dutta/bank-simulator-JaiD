#Bank Simulator
#Version 1
import random

#All Accounts created and information details are stored here
account_data = []

# User Defined Systems/Choices 
#Login system
def login_sys():
    while True:
        print('\n==Login==')
        user_input = input('Login Options: \n[1]Card Number\n[2]Pin Number\n[3]Exit\nEnter: ') # Login Menu & User choices for Card or Pin Number
        if not user_input.isdigit():
            print("\nInvalid Enter an Integer.") # If it is not a number, ask again
            continue
        login_options = int(user_input) # Convert user input to integer

        #Option 1 Card Number
        if login_options == 1:
            print('\n==Card-Number==')
            print("Please Enter your Card Number")
            cardnum_input = input("Enter: ") # Take card number as input

            # Search for card number in stored account data
            for account in account_data:
                if account['card number'] == cardnum_input:
                    print(f"\nLogin Successful. Welcome {account['first name']} {account['last name']}!")
                    main_menu(account) # Proceed to main menu if card number matches
                    return
            else:
                print("\nCard Number not found or invalid.") # If not found

        #Option 2 Pin Number
        elif login_options == 2:
            print("\n==Pin-Number==")
            print("Please Enter PIN Number")
            pinnum_input = input("Enter: ") # Take PIN as string to validate

            # Check if input is 4-digit number
            if not (pinnum_input.isdigit() and len(pinnum_input) == 4):
                print("\nPIN must be exactly 4 digits and only numbers.")
                continue

            pinnum_input = int(pinnum_input) # Convert to integer

            # Search for pin number in stored account data
            for account in account_data:
                if account['pin number'] == pinnum_input:
                    print(f"\nLogin Successful. Welcome {account['first name']} {account['last name']}!")
                    main_menu(account)
                    return
            else:
                print("\nPIN Number not found or invalid.") # If not found

        elif login_options == 3:
            print('\nExiting...') # Exit login system
            return
        else:
            print("\nInvalid Choice Please choose an option")

#Generating the card number in 5 digits
def generate_card_number():
    return ''.join(str(random.randint(0, 9)) for _ in range(5)) # Generate 5-digit random card number

#Account creation for new users 
def account_creation():
    while True:
        print("\n==Account-Creation==")
        # Get user details
        first_name = input("Please enter your first name.\nEnter: ")
        last_name = input("Please enter your last name.\nEnter: ")
        email_input = input("Please enter your email.\nEnter: ")
        pin_input = input("Please enter a 4-digit pin number.\nEnter: ")

        # Validate PIN
        if not (pin_input.isdigit() and len(pin_input) == 4):
            print("\nInvalid. PIN must be exactly 4 digits and only numbers.")
            continue
        pin_input = int(pin_input)

        # Validate names contain only letters
        if not first_name.isalpha() or not last_name.isalpha():
            print("\nInvalid. No numbers or symbols allowed.")
            continue

        # Validate email format
        if not '@' or not '.' in email_input:
            print("\nInvalid Email Format")
            continue

        # Check for duplicates in email or pin
        duplicate = False
        for account in account_data:
            if account['email'] == email_input:
                print("\nThis email is already in use.")
                duplicate = True
                break
            if account['pin number'] == pin_input:
                print("\nThis PIN is already in use.")
                duplicate = True
                break

        if duplicate:
            continue

        # If valid, create new account
        card_number = generate_card_number()
        account_info = {
            'card number': card_number,
            'first name': first_name,
            'last name': last_name,
            'email': email_input,
            'pin number': pin_input,
            'balance': 0.0,
            'transactions': []
        }

        account_data.append(account_info) # Store account info
        print(f"\nAccount created!\nYour card number is: {card_number}")

        account_info['balance'] += 150.00 # Initial balance bonus
        print('For choosing us, we donate you $150 for your balance.')
        return

#User deposit into account
def deposit(account_info):
    while True:
        print("\n==Deposit==")
        print(f'${account_info['balance']:.2f}') # Show current balance
        try:
            dpt_amount = float(input("Enter amount you would like to deposit.\nEnter:$")) # Get deposit amount
        except ValueError:
            print("Please enter a valid number.") # Handle invalid input
            continue
        if dpt_amount <= 0:
            print("Amount must be greater than 0.") # No zero or negative deposits
            continue

        # Reference option for deposit
        while True:
            print('\n==Reference==')
            print('Would you like to add reference?')
            user_input_1 = input("[1]Yes\n[2]No\nEnter: ")
            if not user_input_1.isdigit():
                print('\nInvalid Enter an Integer')
                continue
            opt_reference = int(user_input_1)
            if opt_reference == 1:
                user_reference = input("\nEnter Reference.\nEnter: ")
                account_info['transactions'].append(f'Deposited Amount ${dpt_amount:.2f} - {user_reference}') # Add with reference
            elif opt_reference == 2:
                account_info['transactions'].append(f'Deposited Amount ${dpt_amount:.2f}') # Add without reference
                break
            else:
                print('\nInvalid Option')

        print("\n==New-Balance==") 
        account_info['balance'] += dpt_amount # Update balance
        print(f"Deposit successful! New balance: ${account_info['balance']:.2f}")

        # Ask if user wants another deposit
        while True:
            user_input = input("\nWould you like to do another Deposit?\n[1]Yes\n[2]No\nEnter: ")
            if not user_input.isdigit():
                print("\nInvalid Enter an Integer.")
                continue
            again = int(user_input)
            if again == 1:
                break
            elif again == 2:
                return
            else:
                print('\nPlease enter [1] or [2].')

#User withdraw from account
def withdraw(account_info):
    while True:
        print("\n==Withdraw==")
        print(f'${account_info['balance']:.2f}') # Show current balance
        try:
            wdr_amount = float(input("Enter amount you would like to withdraw.\nEnter:$ ")) # Get withdrawal amount
        except ValueError:
            print("Please enter a valid number.")
            continue
        if wdr_amount <= 0:
            print("Amount must be greater than 0.")
            continue
        if wdr_amount > account_info['balance']:
            print("Insufficient funds")
            continue

        # Reference option for withdrawal
        while True:
            print('\n==Reference==')
            print('Would you like to add reference?')
            user_input_1 = input("[1]Yes\n[2]No\nEnter: ")
            if not user_input_1.isdigit():
                print('\nInvalid Enter an Integer')
                continue
            opt_reference = int(user_input_1)
            if opt_reference == 1:
                user_reference = input("\nEnter Reference.\nEnter: ")
                account_info['transactions'].append(f'Deposited Amount ${wdr_amount:.2f} - {user_reference}') # Add with reference
            elif opt_reference == 2:
                account_info['transactions'].append(f'Deposited Amount ${wdr_amount:.2f}') # Add without reference
                break
            else:
                print('\nInvalid Option')

        print('\n==New-balance==')
        account_info['balance'] -= wdr_amount # Update balance
        print(f"Withdraw successful! New balance: ${account_info['balance']:.2f}")

        # Ask if user wants another withdrawal
        while True:
            user_input = input("\nWould you like to do another Withdraw?\n[1]Yes\n[2]No\nEnter: ")
            if not user_input.isdigit():
                print("\nInvalid Enter an Integer")
                continue
            again = int(user_input)
            if again == 1:
                break
            elif again == 2:
                return
            else:
                print('\nPlease enter [1] or [2].')

#Balance display
def check_balance(account_info):
    print("\n==Balance==")
    print(f"{account_info['first name']} {account_info['last name']} {account_info['card number']}.\nYour balance is: ${account_info['balance']:.2f}")

#Transactions display
def check_transactions(account_info):
    print("\n==Transcations==")
    for item in account_info['transactions']:
        print(item) # Show each transaction
    if len(account_info['transactions']) == 0:
        print("\nNo Transaction Found") # No transactions yet

#Message when user exits
def user_exit():
    print('\nExiting...')

#Main Menu after login
def main_menu(account_info):
    while True:
        print("\n[Bank Name Here]")
        user_input = input('[1]Deposit\n[2]Withdraw\n[3]Check Balance\n[4]Check Transaction History\n[5]Exit\nEnter: ')
        if not user_input.isdigit():
            print('Invalid Enter an Integer')
            continue
        main_options = int(user_input)
        if main_options == 1:
            deposit(account_info)
        elif main_options == 2:
            withdraw(account_info)
        elif main_options == 3:
            check_balance(account_info)
        elif main_options == 4:
            check_transactions(account_info)
        elif main_options == 5:
            user_exit() # Exit back to login or main program
            break
        else:
            print('\nInvalid Option')

#Initial Menu
def inital_menu():
    while True:
        print('\nWelcome to [Bank Name Here]')
        user_input = input("[1]Login\n[2]Create Account\n[3]Exit\nEnter: ")
        if not user_input.isdigit():
            print("\nInvalid Enter an Integer.")
            continue

        inital_options = int(user_input)
        if inital_options == 1:
            login_sys()  # Call login function
        elif inital_options == 2:
            account_creation() # Call account creation function
        elif inital_options == 3:
            user_exit() # Exit program
            break
        else:
            print('\nInvalid Option')

# Run the program
inital_menu()
