from argparse import ArgumentParser
import json
from datetime import datetime

filename = 'tasks.json'

tasks = []

def read_file(func):
    def wrapper(*args, **kwargs):
        try:
            with open(filename, 'r') as file:
                tasks.extend(json.load(file))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

        result = func(*args, **kwargs)

        with open(filename, 'w') as file:
            json.dump(tasks, file, indent=4)

        return result

    return wrapper

@read_file
def add_task(args):
    tasks.append({
        "id": len(tasks) + 1,
        "description": args.description,
        "status": "todo",
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    print(f"Task added successfully (ID: {len(tasks)})")

@read_file
def update_task(args):
    for task in tasks:
        if task["id"] == args.id:
            task["description"] = args.description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Task updated successfully")
            break
    else:
        print("Task not Found")

@read_file
def delete_task(args):
    for task in tasks:
        if task["id"] == args.id:
            tasks.remove(task)
            print("Task deleted successfully")
            break
    
    else:
        print("Task not Found")

    for task in tasks:
        if task["id"] > args.id:
            task["id"] -= 1

@read_file
def mark_task_in_progress(args):
    for task in tasks:
        if task["id"] == args.id:
            task["status"] = "in-progress"
            print("Task in progress ...")
            break
    else:
        print("Task not Found")

@read_file
def mark_task_done(args):
    for task in tasks:
        if task["id"] == args.id:
            task["status"] = "done"
            print("Task done")
            break
    else:
        print("Task not Found")

@read_file
def list_task(args):
    for task in tasks:
        if args.status == None:
            print(task)
        elif task["status"] == args.status:
            print(task)

parser = ArgumentParser()
subparser = parser.add_subparsers(dest="command", required=True)

add = subparser.add_parser('add', help="Add task")
add.add_argument('description', type=str)
add.set_defaults(func=add_task)

update = subparser.add_parser('update', help="Update task")
update.add_argument('id', type=int)
update.add_argument('description', type=str)
update.set_defaults(func=update_task)

delete = subparser.add_parser('delete', help="Delete task")
delete.add_argument('id', type=int)
delete.set_defaults(func=delete_task)

mark_in_progress = subparser.add_parser('mark-in-progress', help="Mark task in progress")
mark_in_progress.add_argument('id', type=int)
mark_in_progress.set_defaults(func=mark_task_in_progress)

mark_done = subparser.add_parser('mark-done', help="Mark task done")
mark_done.add_argument('id', type=int)
mark_done.set_defaults(func=mark_task_done)

list_command = subparser.add_parser('list', help="List tasks")
list_command.add_argument('status', type=str)
list_command.set_defaults(func=list_task)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)