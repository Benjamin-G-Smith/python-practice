# python-practice

Eight exercises, each modeled on a task you'd actually hit on the job. Every
exercise file has `TODO`-marked functions to fill in and a self-check block
at the bottom — run the file directly to see if you got it right.

## Setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd python-practice
uv venv
source .venv/bin/activate
uv pip install ruff
```

No third-party dependencies are required for the exercises themselves —
just the standard library.

## Exercises

| # | File | Scenario | Skills |
|---|------|----------|--------|
| 1 | `exercises/01_basics/messy_log_cleanup.py` | Clean up inconsistent server log lines | strings, f-strings, loops |
| 1b | `exercises/01_basics/log_analytics.py` | Part II of #1: batch-parse and group log lines into service-level stats | dict/list comprehensions, grouping, `str.split(maxsplit=...)`, sorting with a key function |
| 1c | `exercises/01_basics/review_aggregator.py` | Per-category review stats for an e-commerce team | `dict.get(key, 0)`/`collections.defaultdict` for per-key counting (reinforces a bug from #1b) |
| 1d | `exercises/01_basics/lazy_log_stream.py` | Process a log stream lazily instead of loading it all into memory | generators, `yield`, composing generators, stopping early |
| 1e | `exercises/01_basics/rolling_error_window.py` | Track a service's error rate over just its most recent entries | `collections.deque` sliding window, `enumerate`, max-with-key |
| 2 | `exercises/02_data_structures/inventory_manager.py` | Answer stock questions for a shop's inventory | dicts, lists, comprehensions |
| 3 | `exercises/03_functions/expense_report.py` | Build a monthly expense report | functions, `*args`/`**kwargs`, defaults |
| 4 | `exercises/04_files_and_errors/csv_import.py` | Import a messy sales CSV without crashing | file I/O, `csv` module, `try`/`except` |
| 5 | `exercises/05_classes/task_tracker.py` | Build a small in-memory task tracker | classes, methods, state |

## Workflow

1. Open an exercise file, read the scenario docstring, and fill in the
   `TODO` functions.
2. Run it:
   ```bash
   python exercises/01_basics/messy_log_cleanup.py
   ```
   You'll see `All checks passed.` if your implementation is correct, or
   an `AssertionError` telling you what's wrong.
3. Stuck, or want to compare? The finished version is in
   `solutions/<same path>`.

Work through them in order — later exercises assume you're comfortable
with the skills from earlier ones.

## Projects

`projects/` holds bigger, less rigid builds — no `TODO`/self-check
scaffolding, just a README with the goal and a starter file with a
loose skeleton to riff on.

| Project | Scenario | Skills |
|---------|----------|--------|
| `projects/live_log_monitor/` | Watch a log stream in real time and alert when a service's rolling error rate spikes | generators, `collections.deque`, streaming state |
