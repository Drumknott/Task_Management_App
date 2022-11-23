import json


users_data_file = "users.json"
task_data_file = "tasks.json"


def import_user_data():
    with open(users_data_file) as f:
        users_dictionary = json.load(f)
        return users_dictionary


def output_user_data(data):
    with open(users_data_file, 'w') as f:
        json.dump(data, f)

# load json list, return list of Tasks
def load_task_data():
    from task_functions import Task

    with open(task_data_file, 'r') as f:
        task_data = json.load(f)
        all_tasks = []
        for task_list in task_data:
            task = Task(task_list)
            all_tasks.append(task)
        return all_tasks


# take list of tasks, convert to lists for json serialisation
def save_task_data(all_tasks):

    task_list = []
    for task in all_tasks:
        task_list.append(task.to_list())

    with open(task_data_file, 'w') as f:
        json.dump(task_list, f)
