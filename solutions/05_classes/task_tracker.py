"""Solution for exercises/05_classes/task_tracker.py"""

from datetime import date


class Task:
    def __init__(self, title: str, priority: str, due: date):
        self.title = title
        self.priority = priority
        self.due = due
        self.done = False

    def __repr__(self) -> str:
        status = "done" if self.done else "open"
        return f"Task({self.title!r}, {self.priority}, due={self.due}, {status})"


class TaskTracker:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, title: str, priority: str, due: date) -> Task:
        task = Task(title, priority, due)
        self.tasks.append(task)
        return task

    def complete(self, title: str) -> bool:
        for task in self.tasks:
            if task.title == title:
                task.done = True
                return True
        return False

    def open_tasks_by_priority(self, priority: str) -> list[Task]:
        return [t for t in self.tasks if not t.done and t.priority == priority]

    def overdue(self, as_of: date) -> list[Task]:
        return [t for t in self.tasks if not t.done and t.due < as_of]


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
