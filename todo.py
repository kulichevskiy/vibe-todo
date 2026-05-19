import argparse
import os

TASKS_FILE = "tasks.txt"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE) as f:
        return [line.strip() for line in f if line.strip()]


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        for t in tasks:
            f.write(t + "\n")


def cmd_add(args):
    tasks = load_tasks()
    tasks.append(args.text)
    save_tasks(tasks)
    print(f"Added: {args.text}")


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks")
        return
    for i, t in enumerate(tasks, 1):
        print(f"{i}. {t}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
