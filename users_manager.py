import json_data_manager

users_data_file = "users.json"


def login():
    # LOGIN
    valid_user = False
    no_user = True
    while not valid_user:
        username = input("\nLOGIN\nPlease enter your Username: ")

        user_data = json_data_manager.import_user_data()

        for key, value in user_data.items():
            if key != username:
                continue
            else:
                no_user = False
                password = input("Please enter your password: ")
                if password != value:
                    print("\nI'm sorry, that's the wrong password. Please try again.")
                    break
                else:
                    valid_user = True
                    print(f"\nLogged in\nWelcome back, {username}")
                    return username
        if no_user:
            print("No user with that username. Please try again")  # catch


# VALIDATE PASSWORD
def check_new_password_is_valid():
    special_chars = ['!', '£', '$', '%', '&', '*', '.', ',', '?', '@', '_', '-', '<', '>']
    valid_password = False  # set bool to false to enter the loop
    while not valid_password:
        valid_password = True   # defaults to true, will be set to false if password conditions not met
        new_password = input("Please enter a password: ")
        if len(new_password) < 6:
            print("The password needs to be at least 6 characters long")
            valid_password = False
        if len(new_password) > 20:
            print("The password cannot be longer than 20 characters")
            valid_password = False
        if not any(char.lower() for char in new_password):
            print("The password must contain at least one lower case character")
            valid_password = False
        if not any(char.upper() for char in new_password):
            print("The password must contain at least one upper case character")
            valid_password = False
        if not any(char.isdigit() for char in new_password):
            print("The password must contain at least one number")
            valid_password = False
        if not any(char in special_chars for char in new_password):
            print("The password must contain at least one special character")
            valid_password = False
        if not valid_password:
            print("Please try another password using the tips above")
            continue
        else:   # password is valid
            check_password = input("Please re-enter your password: ")

            if new_password != check_password:  # re-enter password
                print("Those password's don't match. Please try again.")
                continue
            else:
                return new_password


def add_new_user():
    new_user_added = False
    new_username = ""

    while not new_user_added:  # loop to add new user
        print("ADD NEW USER")

        users_dictionary = json_data_manager.import_user_data()

        valid_username = False
        while not valid_username:  # loop to make sure username isn't already taken
            valid_username = True
            new_username = input("\nPlease enter the new user's Username: ")

            for key, value in users_dictionary.items():
                if key == new_username:
                    print("There is already a user with this username.")
                    valid_username = False

        new_password = check_new_password_is_valid()
        users_dictionary[new_username] = new_password

        json_data_manager.output_user_data(users_dictionary)

        new_user_added = True  # to break out of the loop
        print(f"New user added: {new_username}. Keep your password safe!")


# choose a user to assign a task to and check they're a registered user
def select_user():
    print("Who are you assigning this task to?")

    users_dictionary = json_data_manager.import_user_data()

    while True:  # loop to make sure the task is assigned to an existing user
        print(f"Available users: {users_dictionary.keys()}")
        assigned_user = input(": ")
        if assigned_user not in users_dictionary.keys():
            print("Invalid user entered. Try again.")
        else:
            return assigned_user
