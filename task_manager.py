import task_functions
import users_manager
import data_manager

current_user = ""

while True:

    # START MENU
    start_choice = input(f"WELCOME\nPlease choose from the following options:\nL\t>\tLogin\nE\t>\tExit\n: ").lower()
    if start_choice == 'e':
        print("GOODBYE")
        exit()
    elif start_choice != 'l':
        print("Invalid choice")
        continue
    else:
        current_user = users_manager.login()

    # MAIN MENU
    while True:
        # presenting the menu to the user and making sure that the user input is converted to lower case.
        print("\nSelect one of the following options below:")
        if current_user == "admin":
            print(f"\t\tR\t>\tRegister a new user")
            print(f"\t\tS\t>\tDisplay Statistics")
        print('''\t\tA\t>\tAdd a new task
        VA\t>\tView all tasks
        VM\t>\tView my tasks
        GR\t>\tGenerate reports
        L\t>\tLog off''')
        menu = input("\t\t: ").lower()

        match menu:
            # ADD NEW USER - only admin can use this
            case 'r' if current_user == "admin":
                users_manager.add_new_user()
            # ADD NEW TASK
            case 'a':
                task_functions.add_new_task()
            # VIEW ALL TASKS
            case 'va':
                task_functions.view_all_tasks(current_user)
            # VIEW MY TASKS
            case 'vm':
                task_functions.view_my_tasks(current_user)
            # DISPLAY STATS - only admin can use this
            case 's' if current_user == "admin":
                data_manager.display_stats(current_user)
            # GENERATE REPORTS
            case 'gr':
                data_manager.generate_reports(current_user)
                print("\nReport files generated successfully")
            # LOG OUT
            case 'l':
                print("LOGGED OUT")
                break
            case _:
                print("\nInvalid choice. Please try again.\n")
