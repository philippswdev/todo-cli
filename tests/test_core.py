import pytest

from todo_cli.core import Importance, Task, Urgency, add_task, mark_done, quadrant, sorted_tasks


def test_quadrant_mapping():
    assert quadrant(Task(1, "q1", Importance.HIGH, Urgency.HIGH)) == 1
    assert quadrant(Task(2, "q2", Importance.HIGH, Urgency.LOW)) == 2
    assert quadrant(Task(3, "q3", Importance.LOW, Urgency.HIGH)) == 3
    assert quadrant(Task(4, "q4", Importance.LOW, Urgency.LOW)) == 4


def test_sorted_tasks_orders_by_done_then_quadrant_then_title():
    tasks = [
        Task(10, "zzz", Importance.HIGH, Urgency.HIGH, done=True),
        Task(11, "b", Importance.HIGH, Urgency.HIGH, done=False),
        Task(12, "a", Importance.HIGH, Urgency.HIGH, done=False),
        Task(13, "x", Importance.LOW, Urgency.LOW, done=False),
    ]
    ordered = sorted_tasks(tasks)
    assert [t.title for t in ordered] == ["a", "b", "x", "zzz"]


def test_add_task_assigns_incrementing_ids():
    tasks = []
    tasks = add_task(tasks, "t0", Importance.HIGH, Urgency.HIGH)
    tasks = add_task(tasks, "t1", Importance.LOW, Urgency.LOW)
    assert [t.id for t in tasks] == [1, 2]


def test_mark_done_by_id_does_not_depend_on_sort_order():
    tasks = []
    tasks = add_task(tasks, "lowlow", Importance.LOW, Urgency.LOW)     # id 1
    tasks = add_task(tasks, "highhigh", Importance.HIGH, Urgency.HIGH) # id 2

    # sortiert wäre id 2 zuerst, aber done soll trotzdem über id 1/2 stabil gehen
    updated = mark_done(tasks, 1)
    assert updated[0].id == 1 and updated[0].done is True
    assert updated[1].id == 2 and updated[1].done is False


def test_mark_done_unknown_id_raises():
    tasks = [Task(1, "t0", Importance.HIGH, Urgency.HIGH)]
    with pytest.raises(KeyError):
        mark_done(tasks, 999)
