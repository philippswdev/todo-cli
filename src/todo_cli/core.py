from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Iterable, List, Sequence


class Importance(Enum):
    LOW = "low"
    HIGH = "high"


class Urgency(Enum):
    LOW = "low"
    HIGH = "high"


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    importance: Importance
    urgency: Urgency
    done: bool = False


def quadrant(task: Task) -> int:
    imp_high = task.importance is Importance.HIGH
    urg_high = task.urgency is Urgency.HIGH

    if imp_high and urg_high:
        return 1
    if imp_high and not urg_high:
        return 2
    if not imp_high and urg_high:
        return 3
    return 4


def sorted_tasks(tasks: Iterable[Task]) -> List[Task]:
    # Sortierung bleibt: unerledigt -> Quadrant -> Titel
    return sorted(list(tasks), key=lambda t: (t.done, quadrant(t), t.title.lower()))


def next_id(tasks: Sequence[Task]) -> int:
    # fortlaufend: 1, 2, 3 ... (Lücken sind ok)
    return max((t.id for t in tasks), default=0) + 1


def add_task(tasks: Sequence[Task], title: str, importance: Importance, urgency: Urgency) -> List[Task]:
    new = Task(
        id=next_id(tasks),
        title=title,
        importance=importance,
        urgency=urgency,
        done=False,
    )
    return list(tasks) + [new]


def mark_done(tasks: Sequence[Task], task_id: int) -> List[Task]:
    """
    Returns a new list where the task with id=task_id is marked done.
    Raises KeyError if task_id not found.
    """
    updated: List[Task] = []
    found = False

    for t in tasks:
        if t.id == task_id:
            updated.append(replace(t, done=True))
            found = True
        else:
            updated.append(t)

    if not found:
        raise KeyError(f"No task with id {task_id}")

    return updated
