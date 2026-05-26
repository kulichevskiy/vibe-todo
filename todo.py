import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

PRIORITY_MARKS = {"high": "!!!", "medium": " ··", "low": "  ·"}


class TaskStore:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.todo_items = self._load_items()

    def _load_items(self):
        if not os.path.exists(self.storage_path):
            return []
        with open(self.storage_path) as fp:
            return json.load(fp)

    def save_items(self):
        with open(self.storage_path, "w") as fp:
            json.dump(self.todo_items, fp, indent=2, ensure_ascii=False)

    def add_item(self, title, priority, due_date):
        self.todo_items.append({"title": title, "priority": priority, "due_date": due_date})
        self.save_items()

    def delete_item(self, position):
        item_index = position - 1
        if 0 <= item_index < len(self.todo_items):
            deleted_item = self.todo_items.pop(item_index)
            self.save_items()
            return deleted_item
        return None


def cmd_add(args):
    store = TaskStore(TASKS_FILE)
    store.add_item(args.text, args.priority, args.due)
    print(f"  + Added: {args.text}")


def cmd_list(args):
    store = TaskStore(TASKS_FILE)
    if not store.todo_items:
        print("  (no tasks)")
        return
    print()
    for position, item in enumerate(store.todo_items, 1):
        priority_mark = PRIORITY_MARKS[item["priority"]]
        due_formatted = datetime.strptime(item["due_date"], "%Y-%m-%d").strftime("%d.%m")
        print(f"  {position:>2}. {priority_mark}  {item['title']:<30}  ⏰ {due_formatted}")
    print()


def cmd_delete(args):
    store = TaskStore(TASKS_FILE)
    deleted_item = store.delete_item(args.index)
    if deleted_item:
        print(f"  - Deleted: {deleted_item['title']}")
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
