"""
Real-world scenario
--------------------
Your team's shared spreadsheet for tracking tasks has gotten unwieldy.
You're prototyping a small in-memory task tracker: add tasks with a
priority, mark them done, and pull reports (open tasks by priority,
overdue tasks). This is the same shape as the model layer behind tools
like Trello or Linear, just simplified.

Skills practiced: classes, __init__, instance methods, encapsulating
state instead of passing dicts/lists around everywhere, __repr__.

Run this file directly to see your output and self-check results:
    python task_tracker.py
"""

from datetime import date


class Task:
    """A single task. TODO: implement __init__."""

    def __init__(self, title: str, priority: str, due: date):
        """
        Store title, priority ("low", "medium", "high"), due (a date),
        and set done = False.

        TODO: implement this method.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        status = "done" if self.done else "open"
        return f"Task({self.title!r}, {self.priority}, due={self.due}, {status})"


class TaskTracker:
    """Manages a collection of Task objects."""

    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, title: str, priority: str, due: date) -> Task:
        """
        Create a Task, add it to self.tasks, and return it.

        TODO: implement this method.
        """
        raise NotImplementedError

    def complete(self, title: str) -> bool:
        """
        Mark the first task matching `title` as done (task.done = True).
        Return True if a task was found and marked, False otherwise.

        TODO: implement this method.
        """
        raise NotImplementedError

    def open_tasks_by_priority(self, priority: str) -> list[Task]:
        """
        Return all tasks with done == False and the given priority.

        TODO: implement this method.
        """
        raise NotImplementedError

    def overdue(self, as_of: date) -> list[Task]:
        """
        Return all open tasks (done == False) where task.due < as_of.

        TODO: implement this method.
        """
        raise NotImplementedError


def _self_check() -> None:
    tracker = TaskTracker()
    tracker.add("Write Q3 report", "high", date(2026, 7, 20))
    tracker.add("Reply to vendor email", "low", date(2026, 8, 5))
    tracker.add("Fix login bug", "high", date(2026, 7, 30))
    tracker.add("Clean up test suite", "medium", date(2026, 8, 15))

    assert len(tracker.tasks) == 4, f"expected 4 tasks, got {len(tracker.tasks)}"

    marked = tracker.complete("Reply to vendor email")
    assert marked is True, "expected complete() to return True for an existing task"
    not_found = tracker.complete("Nonexistent task")
    assert not_found is False, "expected complete() to return False for a missing task"

    high_priority_open = tracker.open_tasks_by_priority("high")
    titles = sorted(t.title for t in high_priority_open)
    assert titles == ["Fix login bug", "Write Q3 report"], f"unexpected: {titles}"

    overdue = tracker.overdue(as_of=date(2026, 7, 28))
    overdue_titles = sorted(t.title for t in overdue)
    assert overdue_titles == ["Write Q3 report"], f"unexpected overdue: {overdue_titles}"

    print("All checks passed.")
    print(f"Open high priority: {titles}")
    print(f"Overdue as of 2026-07-28: {overdue_titles}")


if __name__ == "__main__":
    _self_check()
