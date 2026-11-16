
from argparse import ArgumentParser
import json

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
        "description": args.task
    })

    print(f"Task added successfully (ID: {len(tasks)})")


parser = ArgumentParser()
subparser = parser.add_subparsers(dest="command", required=True)

add = subparser.add_parser('add', help="Add task")
add.add_argument('task', type=str)
add.set_defaults(func=add_task)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)