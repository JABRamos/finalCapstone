# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.
# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# dictionary for username_password
username_password = {}

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# list to store tasks
task_list = []


# function for reg_user
def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    while True:
        new_username = input("New Username: ")
        # checking if username already exists - as per task requirement
        if new_username in username_password.keys():
            print("Woah! Username already exists. Please enter a different username. ")
        else:
            break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise, present a relevant message.
    else:
        print("Passwords do not match")


# function for adding_task
def add_task():
    '''Allow a user to add a new task to the task.txt file.
    Prompt the user for the following:
    - A username of the person whom the task is assigned to.
    - A title of the task.
    - A description of the task.
    - The due date of the task.
    '''
    
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the specified format.")

import os
from datetime import datetime

task_list = []  # Assuming this variable is defined correctly elsewhere
username_password = {}  # Assuming this variable is defined correctly elsewhere

# function to generate task overview report
def generate_task_overview():
    total_tasks = len(task_list)
    complete_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - complete_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now())

    if total_tasks != 0:
        incomplete_percentage = (incomplete_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100
    else:
        incomplete_percentage = 0
        overdue_percentage = 0

    with open("task_overview.txt", "w") as report_file:
        report_file.write("Task Overview\n\n")
        report_file.write(f"Total Tasks: {total_tasks}\n")
        report_file.write(f"Complete Tasks: {complete_tasks}\n")
        report_file.write(f"Incomplete Tasks: {incomplete_tasks}\n")
        report_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        report_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
        report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    print("Task overview report generated successfully.")

# function to generate user overview report
def generate_user_overview():
    total_users = len(username_password.keys())
    total_tasks = len(task_list)

    with open("user_overview.txt", "w") as report_file:
        report_file.write("User Overview\n\n")
        report_file.write(f"Total Users: {total_users}\n")
        report_file.write(f"Total Tasks: {total_tasks}\n")

        for username in username_password.keys():
            user_tasks = [task for task in task_list if task['username'] == username]
            user_task_count = len(user_tasks)

            if user_task_count != 0:
                user_percentage = (user_task_count / total_tasks) * 100
                completed_percentage = (sum(task['completed'] for task in user_tasks) / user_task_count) * 100
                incomplete_percentage = (sum(not task['completed'] for task in user_tasks) / user_task_count) * 100
                overdue_percentage = (sum(not task['completed'] and task['due_date'] < datetime.now() for task in user_tasks) / user_task_count) * 100
            else:
                user_percentage = 0
                completed_percentage = 0
                incomplete_percentage = 0
                overdue_percentage = 0

            report_file.write(f"\nUsername: {username}\n")
            report_file.write(f"Total Tasks Assigned: {user_task_count}\n")
            report_file.write(f"Percentage of Total Tasks Assigned: {user_percentage:.2f}%\n")
            report_file.write(f"Percentage of Completed Tasks: {completed_percentage:.2f}%\n")
            report_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%\n")
            report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%\n")

    print("User overview report generated successfully.")

def display_statistics():
    # Generate task.txt and user.txt files if they don't exist
    if not os.path.exists("task_overview.txt"):
        generate_task_overview()
    if not os.path.exists("user_overview.txt"):
        generate_user_overview()

    # Read task overview report
    with open("task_overview.txt", "r") as task_file:
        task_report = task_file.read()
    # Read user overview report
    with open("user_overview.txt", "r") as user_file:
        user_report = user_file.read()

    # Display reports
    print("Task Overview Report:")
    print(task_report)
    print("User Overview Report:")
    print(user_report)


def generate_reports():

    '''Generates task and user overview reports'''
    task_username = curr_user
    generate_task_overview()
    generate_user_overview()

    
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # Create a list of task attributes in an order - including Yes/No
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))

        task_file.write("\n".join(task_list_to_write))

    print("Task successfully added.")

def view_all():
    '''Reads the task from tasks.txt file and prints to the console.'''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(curr_user):
    '''Reads the tasks from tasks.txt and prints those assigned to the (current) user'''
    tasks_assigned = []

    # iterate over each task in the 'task_list'. For each task, check if the value of the username matches the 'curr_user' - if it matches, the task is assigned
    for index, task in enumerate(task_list):
        if task['username'] == curr_user:
            tasks_assigned.append(task)
            print(f"Task: {index+1} \t {task['title']}")

            print(f"Assigned to: \t {task['username']}\n")
            print(f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            print(f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            print(f"Task Description: \n {task['description']}\n")

    # prints an empty line to provide separation and make it easier to read
    print()

    # if the length is 0, no tasks assigned - print a message saying no tasks assigned
    if len(tasks_assigned) == 0:
        print("No tasks assigned to you.")
        return

    while True:
        try:
            # asks the user to enter the number of the task they want to select or to go back to the main menu
            selected_task = int(input("Enter the number of the task you want to select (or -1 to return to the main menu): "))
            if selected_task == -1:
                return
            # if the user enters a task number outside the range, display a message and ask the user again
            elif selected_task < 1 or selected_task > len(tasks_assigned):
                print("Invalid task number. Please try again.")
            # if the user enters a valid task number, break out of the loop
            else:
                break
        # if the user enters a value that is not a number (integer), display an error message and ask the user again
        except ValueError:
            print("Invalid input. Please enter a number.")

    task = tasks_assigned[selected_task - 1]
    disp_str = ""
    disp_str += f"Task: \t\t {task['title']}\n"
    disp_str += f"Assigned to: \t {task['username']}\n"
    disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: \n {task['description']}\n"

    if not task['completed']:
        # if the task is not completed, enter the loop below
        while True:
            select = input("Choose an action: 1. Mark the task as complete, 2. Edit task")
            if select == '1':
                # option 1 for the user to select
                task['completed'] = True
                disp_str += "Task marked as completed"
                break
            elif select == '2':
                # option 2 i.e. edit the task
                if task['completed']:
                    # if the task is completed, it can't be edited (as per the task request)
                    disp_str += "The task has been completed and cannot be edited - we're sorry"
                    break
                # Ask the user for a new username or leave it blank to keep the same username
                new_username = input("Enter a new username of the person assigned to the task or leave blank to keep the same username: ")
                if new_username != "":
                    task['username'] = new_username

                # Enter a new due date for the task - if they can edit a task
                new_due_date = input("Enter the new due date of the task (YYYY-MM-DD) (or leave blank to keep the current due date): ")
                if new_due_date != "":
                    try:
                        task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    # if not in the right format, then an appropriate error message is displayed
                    except ValueError:
                        disp_str += "Not the right format. Please try again."
                disp_str += "Task updated."
                break
            else:
                print("Invalid input. Please choose a valid action.")
    else:
        disp_str += "This task has already been completed and cannot be edited."

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print(disp_str)
    print("Task successfully updated.")
    
    # Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if user != "":
        username, password = user.split(';')
        username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gt - Generate task overview report
gr - Generate report
gu - Generate user overview report
e - Exit ''').lower()

    # called when user selects 'r' to register a user
    if menu == 'r':
        reg_user()

    # called when a user selects 'a' to add a new task
    elif menu == 'a':
        add_task()

    # called when users type 'va' to view all the tasks listed in 'tasks.txt.'
    elif menu == 'va':
        view_all()

    # called when users type 'vm' to view all the tasks that have been assigned to them
    elif menu == 'vm':
        view_mine(curr_user)

    # called when user types 'gt' to generate task overview report
    elif menu == 'gt':
        generate_task_overview()

    # called when users type 'gu' to generate user overview report
    elif menu == 'gu':
        generate_user_overview()

    # call generate report
    elif menu == "gr":
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':
        # If the user is an admin, they can display statistics about the number of users and tasks.
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        break

    else:
        print("You have made a wrong choice. Please try again")


    
