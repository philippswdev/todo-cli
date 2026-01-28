from __future__ import annotations

import argparse
import sys
from pathlib import Path

from todo_cli.core import Importance, Urgency, add_task, mark_done, sorted_tasks
from todo_cli.storage import default_db_path, load_tasks, save_tasks

def parse_importance(s: str) -> Importance:
    try:
        return Importance(s.lower())
    except ValueError as e:
        raise argparse.ArgumentTypeError("importance must be 'high' or 'low'") from e


def parse_urgency(s: str) -> Urgency:
    try:
        return Urgency(s.lower())
    except ValueError as e:
        raise argparse.ArgumentTypeError("urgency must be 'high' or 'low'") from e


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="Todo CLI (Eisenhower: importance/urgency).")
    p.add_argument("--db", type=Path, default=default_db_path(), help="Path to JSON db file")

    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title")
    add.add_argument("--importance", "-i", type=parse_importance, default=Importance.HIGH)
    add.add_argument("--urgency", "-u", type=parse_urgency, default=Urgency.LOW)

    ls = sub.add_parser("list", help="List tasks")
    ls.add_argument("--all", action="store_true", help="Include completed tasks")

    done = sub.add_parser("done", help="Mark a task done")
    done.add_argument("id", type=int, help="Task id")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        tasks = load_tasks(args.db)
    except Exception as e:
        print(f"Error loading DB: {e}", file=sys.stderr)
        return 2

    if args.cmd == "add":
        tasks = add_task(tasks, args.title, args.importance, args.urgency)
        save_tasks(args.db, tasks)
        print(f"Added task #{tasks[-1].id}: {tasks[-1].title}")
        return 0

    if args.cmd == "list":
        ordered = sorted_tasks(tasks)
        if not args.all:
            ordered = [t for t in ordered if not t.done]
        for t in ordered:
            status = "✓" if t.done else " "
            print(f"[{status}] #{t.id} {t.title} (imp={t.importance.value}, urg={t.urgency.value})")
        return 0

    if args.cmd == "done":
        try:
            tasks = mark_done(tasks, args.id)
        except KeyError as e:
            print(str(e), file=sys.stderr)
            return 2
        save_tasks(args.db, tasks)
        print(f"Marked #{args.id} as done.")
        return 0

    return 1
