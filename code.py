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
        "description": args.task,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    print(f"Task added successfully (ID: {len(tasks)})")

@read_file
def update_task(args):
    for task in tasks:
        if task["id"] == args.id:
            task["description"] = args.description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    else:
        print("Task not Found")

parser = ArgumentParser()
subparser = parser.add_subparsers(dest="command", required=True)

add = subparser.add_parser('add', help="Add task")
add.add_argument('description', type=str)
add.set_defaults(func=add_task)

update = subparser.add_parser('update', help="Update task")
update.add_argument('id', type=int)
update.add_argument('description', type=str)
update.set_defaults(func=update_task)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)