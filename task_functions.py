import datetime
import json_data_manager
from users_manager import select_user


class Task:

    def __init__(self, task_list):
        self.assigned_to = task_list[0]
        self.title = task_list[1]
        self.description = task_list[2]
        self.date_assigned = task_list[3]
        self.date_due = task_list[4]
        self.completed = task_list[5]
        self.changelog = ''

    def to_list(self):
        if self.changelog:
            return [self.assigned_to, self.title, self.description, self.date_assigned, self.date_due, self.completed,
                    self.changelog]
        else:
            return [self.assigned_to, self.title, self.description, self.date_assigned, self.date_due, self.completed]


full_time = datetime.datetime.today()
current_date = str(full_time)[:10]


def add_new_task():
    print("ADD NEW TASK")
    assigned_user = select_user()

    # enter task details
    task_title = input("Please enter the task title: ")
    task_description = input("Please enter a description of the task: ")
    due_date = input("In the format YYYY-MM-DD, when is this task due? ")

    task_components = [assigned_user, task_title, task_description, current_date, due_date, "No"]

    # save task to file
    all_tasks = json_data_manager.load_task_data()
    new_task = Task(task_components)
    all_tasks.append(new_task)
    json_data_manager.save_task_data(all_tasks)

    print("\nTask added to task list")


def print_tasks(task):
    print("-----------------------------------------------------------------------------------")
    print("")
    print(f"Task:\t\t\t\t{task.title}")
    print(f"Assigned to:\t\t{task.assigned_to}")
    print(f"Date assigned:\t\t{task.date_assigned}")
    print(f"Date due:\t\t\t{task.date_due}")
    print(f"Task complete?\t\t{task.completed}")
    print(f"Task Description:")
    print(f"\t{task.description}")
    print("")
    print("-----------------------------------------------------------------------------------\n")


def view_all_tasks(current_user):
    print("VIEW ALL TASKS")

    view_complete_tasks = False
    view_incomplete_tasks = False
    edit_tasks = False

    if current_user == "admin":
        while True:
            print("A > Display all tasks")
            print("C > Display only completed tasks")
            print("I > Display only incomplete tasks")
            print("E > Edit task")
            admin_input = input(": ").lower()

            match admin_input:
                case 'a':
                    break
                case 'c':
                    view_complete_tasks = True
                    break
                case 'i':
                    view_incomplete_tasks = True
                    break
                case 'e':
                    edit_tasks = True
                    break
                case _:
                    print("Invalid command. Please try again.")

    all_tasks = json_data_manager.load_task_data()
    for index, task in enumerate(all_tasks):
        if view_complete_tasks:
            if task.completed == "Yes":
                print_tasks(task)
        elif view_incomplete_tasks:
            if task.completed == "No":
                print_tasks(task)
        else:
            print(f"Task {index + 1}:")
            print_tasks(task)

    if edit_tasks:
        edit_task(all_tasks, current_user)


# edit task, then save the changes to the task file along with a log of the changes
def edit_task(all_tasks, current_user):
    for index, task in enumerate(all_tasks):
        if task.assigned_to == current_user or current_user == "admin":
            print(f"{index + 1}: {task.title}")

    while True:
        try:
            chosen_task = int(input("\nWhich task would you like to edit? Enter -1 to go back: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
        except IndexError:
            print("That wasn't on the list!")
        else:
            break

    if chosen_task == -1:
        return

    edited_task = all_tasks[chosen_task]
    if edited_task.completed.strip() == "Yes":
        print("You can't edit a task after it's been completed")
    else:
        while True:
            print("\nC > Mark task as complete")
            print("T > Edit task description")
            print("A > Change the assigned User")
            print("D > Change the date task is due\n")
            choice = input(": ").lower()

            match choice:
                case 'c':
                    edited_task.completed = "Yes"
                    edited_task.changelog = f"Task Completed by {current_user} on {current_date}"
                    break
                case 't':
                    new_description = input("Enter new description for this task: ")
                    edited_task.description = new_description
                    edited_task.changelog = f"Task description updated by {current_user} on {current_date}"
                    break
                case 'a':
                    assigned_user = select_user()
                    edited_task.assigned_to = assigned_user
                    edited_task.changelog = f"Task assigned to {assigned_user} by {current_user} on {current_date}"
                    break
                case 'd':
                    new_date = input("In the format YYYY-MM-DD please enter the new due date for this task: ")
                    edited_task.date_due = new_date
                    edited_task.changelog = f"Due date updated by {current_user} on {current_date}"
                    break
                case _:
                    print("Invalid command. Please try again.")

        print(edited_task.changelog)

        for _task in all_tasks:
            if _task.title == edited_task.title:
                _task = edited_task

        json_data_manager.save_task_data(all_tasks)


def view_my_tasks(current_user):
    print("VIEW MY TASKS")
    assigned_task = False

    all_tasks = json_data_manager.load_task_data()
    index = 0
    for task in all_tasks:
        if task.assigned_to == current_user:
            assigned_task = True
            print(f"Task {index}:")
            print_tasks(task)
            index += 1

    if not assigned_task:
        print("You don't have any tasks currently assigned to you.")
        return

    edit_tasks = input("Would you like to edit a task? Y/N ").lower()
    if edit_tasks == 'y':
        edit_task(all_tasks, current_user)
    elif not edit_tasks == 'n':
        print("Invalid command")
