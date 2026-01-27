from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Mapping

from todo_cli.core import Importance, Task, Urgency


def default_db_path() -> Path:
    # Einfacher Start: Datei im Home-Verzeichnis des Users
    return Path.home() / ".todo_cli.json"


def task_to_json(t: Task) -> dict[str, Any]:
    return {
        "id": t.id,
        "title": t.title,
        "importance": t.importance.value,
        "urgency": t.urgency.value,
        "done": t.done,
    }


def task_from_json(d: Mapping[str, Any]) -> Task:
    return Task(
        id=int(d["id"]),
        title=str(d["title"]),
        importance=Importance(str(d["importance"])),
        urgency=Urgency(str(d["urgency"])),
        done=bool(d.get("done", False)),
    )


def load_tasks(path: Path) -> List[Task]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("DB file must contain a JSON list")
    return [task_from_json(item) for item in raw]


def save_tasks(path: Path, tasks: List[Task]) -> None:
    payload = [task_to_json(t) for t in tasks]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
