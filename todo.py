import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

PRIORITY_MARKS = {"high": "!!!", "medium": " ··", "low": "  ·"}


class TaskStore:
    def __init__(self, path):
        self.path = path
        self.tasks = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path) as f:
            return json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.tasks, f, indent=2, ensure_ascii=False)

    def add(self, text, priority, due_date):
        self.tasks.append({"text": text, "priority": priority, "due_date": due_date})
        self.save()

    def delete(self, index):
        idx = index - 1
        if 0 <= idx < len(self.tasks):
            removed = self.tasks.pop(idx)
            self.save()
            return removed
        return None


def cmd_add(args):
    store = TaskStore(TASKS_FILE)
    store.add(args.text, args.priority, args.due)
    print(f"  + Added: {args.text}")


def cmd_list(args):
    store = TaskStore(TASKS_FILE)
    if not store.tasks:
        print("  (no tasks)")
        return
    print()
    for i, t in enumerate(store.tasks, 1):
        mark = PRIORITY_MARKS[t["priority"]]
        due = datetime.strptime(t["due_date"], "%Y-%m-%d").strftime("%d.%m")
        print(f"  {i:>2}. {mark}  {t['text']:<30}  ⏰ {due}")
    print()


def cmd_delete(args):
    store = TaskStore(TASKS_FILE)
    removed = store.delete(args.index)
    if removed:
        print(f"  - Deleted: {removed['text']}")
    else:
        print(f"  ! No task with index {args.index}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_add.add_argument("--priority", choices=["high", "medium", "low"], default="medium")
    p_add.add_argument("--due", default=None, help="due date in YYYY-MM-DD")
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
