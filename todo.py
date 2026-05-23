import argparse
import json
import os

TASKS_FILE = "tasks.json"

PRIORITY_MARKS = {"high": "!!!", "medium": " ··", "low": "  ·"}


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def cmd_add(args):
    tasks = load_tasks()
    tasks.append({"text": args.text, "priority": args.priority})
    save_tasks(tasks)
    print(f"  + Added: {args.text}")


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("  (no tasks)")
        return
    print()
    for i, t in enumerate(tasks, 1):
        mark = PRIORITY_MARKS[t["priority"]]
        print(f"  {i:>2}. {mark}  {t['text']}")
    print()


def cmd_delete(args):
    tasks = load_tasks()
    idx = args.index - 1
    if 0 <= idx < len(tasks):
        removed = tasks.pop(idx)
        save_tasks(tasks)
        print(f"  - Deleted: {removed['text']}")
    else:
        print(f"  ! No task with index {args.index}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_add.add_argument("--priority", choices=["high", "medium", "low"], default="medium")
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
