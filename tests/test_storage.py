from pathlib import Path
import json
import pytest
from todo_cli.core import Importance, Task, Urgency
from todo_cli.storage import load_tasks, save_tasks


def test_save_and_load_roundtrip(tmp_path: Path):
    p = tmp_path / "db.json"
    tasks = [
        Task(1, "a", Importance.HIGH, Urgency.LOW, done=False),
        Task(2, "b", Importance.LOW, Urgency.HIGH, done=True),
    ]
    save_tasks(p, tasks)
    loaded = load_tasks(p)
    assert loaded == tasks


def test_load_missing_file_returns_empty_list(tmp_path: Path):
    p = tmp_path / "missing.json"
    assert load_tasks(p) == []


def test_load_invalid_importance_raises(tmp_path: Path):
    p = tmp_path / "db.json"
    p.write_text(json.dumps([{
        "id": 1,
        "title": "x",
        "importance": "superhigh",
        "urgency": "low",
        "done": False
    }]), encoding="utf-8")

    with pytest.raises(ValueError):
        load_tasks(p)
