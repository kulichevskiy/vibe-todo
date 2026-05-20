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


def cmd_delete(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f"Deleted: {removed}")
    else:
        print(f"No task with index {args.index}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    p_del = sub.add_parser("delete")
    p_del.add_argument("index", type=int)
    p_del.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
