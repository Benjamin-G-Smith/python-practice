# python-practice

A personal repo for practicing Python fundamentals with realistic,
job-shaped exercises (log parsing, inventory logic, expense reports,
messy CSV imports, a small task-tracker class). See README.md for setup
and the exercise index.

## My role (read this first)

My goal here is to **learn**, not to get exercises finished fast. Optimize
every interaction for understanding, not for the shortest path to a
passing self-check.

When I'm working an exercise:
- Don't write the solution for me unless I explicitly ask for it ("just
  show me the code", "I'm stuck, give me the answer").
- Default to hints: name the concept, point at the relevant builtin or
  stdlib method, or ask a guiding question that gets me to the next step
  myself.
- If I ask "is this right?" or "why isn't this working?", run the file
  directly (`python path/to/file.py`) rather than eyeballing my code, and
  explain any `AssertionError` in terms of what my implementation
  actually does versus what's expected — not just "here's the fix".
- If my solution passes but is clunky, you can mention a cleaner idiom
  once I've got it working — don't rewrite working code unprompted.
- Solutions in `solutions/` are the answer key. Don't open or paste from
  them to "help" unless I ask — that defeats the point.

**Exception — quick syntax/reference lookups.** If I ask a general "how
does X work" question (f-string syntax, what a dict comprehension looks
like, the difference between `==` and `is`, how `try`/`except`/`else`
chains, etc.) rather than "how do I solve this exercise," answer it
directly and fully, like a cheat sheet — short explanation plus a small
generic example unrelated to the exercise's actual data. That's a
reference lookup, not a spoiler. The hints-only rule applies specifically
to *this exercise's solution*, not to Python knowledge in general.

## Creating new exercises

When I ask for another exercise, a harder one, to be quizzed, or what to
practice next, use the `refine-questions` skill
(`.claude/skills/refine-questions/SKILL.md`) — it looks at how I actually
solved the last exercise (mistakes, hints needed, idioms used) before
deciding whether the next one should reinforce or escalate. Don't just
generate the next topic in sequence blind.

## Logging finished lessons

When a lesson is actually done — self-check passes and I've signaled I'm
moving on (asking for the next exercise, saying thanks/done, or asking
directly to log/commit progress) — use the `log-lesson` skill
(`.claude/skills/log-lesson/SKILL.md`). It commits the lesson's files to
git with a summary of questions/struggles/approach, and appends a
session entry to `~/Documents/ember-vault/projects/python-practice.md`
so progress is traceable across my other AI apps too. Don't invoke it
for every small edit or a failed self-check — only on real completion.

The format below is what that skill (and any manual exercise creation)
must follow exactly:

- A module docstring with a real-world scenario (what job task this
  simulates) and the skills it drills.
- Sample data as module-level constants.
- Functions with docstrings describing the contract, bodies replaced with
  `# TODO: implement this function` + `raise NotImplementedError`.
- A `_self_check()` function at the bottom using plain `assert` with
  descriptive failure messages, called under `if __name__ == "__main__":`.
- A mirrored, fully-implemented version in `solutions/<same relative path>`.
- Add a row to the exercise table in README.md.

Prefer scenarios over algorithm-puzzle trivia: data cleaning, reporting,
small CLIs, config/file processing, simple API-shaped data (lists of
dicts), light OOP modeling. Favor the standard library — only introduce a
dependency if the exercise is specifically about that tool.

## Difficulty progression

Current order: basics -> data structures -> functions -> files & error
handling -> classes. When bumping difficulty, prefer combining skills
from earlier topics over introducing something totally new (e.g. a
"harder" files exercise might require both error handling and a small
class to hold parsed records).

## Structure

```
exercises/NN_topic/*.py   unsolved — TODOs + self-check
solutions/NN_topic/*.py   reference implementations
projects/<name>/          lightly scaffolded, no answer key — see below
README.md                 setup instructions + exercise index
```

## Projects (different from exercises)

`projects/` holds bigger, less rigid builds — no `TODO` +
`NotImplementedError` + plain-assert self-check format, no mirrored
`solutions/` entry, and no README.md exercise-table row. Each project
folder has its own README with the scenario, goal, and a suggested (not
mandatory) approach. Signatures/docstrings in the starter file are a
skeleton to riff on, not a fixed contract — encourage restructuring over
rigid compliance. Verification is "run it and eyeball the output" rather
than a fixed self-check, unless the user adds their own asserts.

Use this format when an exercise idea is a good escalation but doesn't
fit the fixed-contract/self-check shape well — e.g. anything with
open-ended design space, real I/O, or multiple reasonable architectures.

## Environment

`uv venv` + `ruff` (see pyproject.toml). No pytest — self-checks are
plain asserts, run directly with `python <file>`.

## Progress notes

Keep this section current as exercises get finished, so a future session
knows where I left off and what I found hard.

- [x] 01_basics — messy_log_cleanup: solved cleanly first pass (all 3 functions).
      Iterated on idioms after passing: switched manual if/not-in counting to
      `dict.get(key, 0) + 1`; discussed sequence-unpacking / `zip`+`dict` as
      alternatives to hardcoded split indexes but didn't apply them here. Added
      own edge-case assertions (empty input, unknown service, delimiter char
      inside message) and found a real bug: naive `split("|")` truncates a
      message that itself contains `|`. Fix is `split("|", maxsplit=3)`.
- [ ] 01_basics — log_analytics (Part II of messy_log_cleanup): escalation
      exercise targeting the maxsplit fix and hardcoded-index concern from
      messy_log_cleanup, plus grouping into a dict of lists, per-group
      aggregation, and `sorted(..., key=...)` with a tuple key for
      descending+alphabetical tiebreak. In progress as of 2026-07-31:
      `parse_logs` implemented correctly (keys-list + range loop over the
      maxsplit result). `group_by_service` builds the dict correctly in its
      loop but is missing `return groupedEntries` — it falls through to a
      leftover `raise NotImplementedError` that was never deleted, and
      there's a stray debug `print(groupedEntries)` still in the loop.
      `error_rate_by_service` and `top_error_services` not started. Originally
      created under `02_data_structures/`; moved to `01_basics/` (own choice,
      2026-07-31) — solutions/ moved to match.
- [ ] 01_basics — lazy_log_stream: new, targets generators (`yield`),
      lazy iteration, composing generators. Self-check proves real laziness
      (counts how many raw lines get pulled to find the first 2 errors, and
      fails if the implementation secretly materializes a full list). Built
      as a prerequisite for projects/live_log_monitor. Originally created
      under `02_data_structures/`; moved to `01_basics/` (own choice,
      2026-07-31). Not yet attempted.
- [ ] 01_basics — rolling_error_window: new, targets
      `collections.deque(maxlen=...)` for a fixed-size sliding window, plus
      `enumerate`/max-with-key. Works on a flat single-service list — the
      per-service dict-of-deques version is deferred to the project. Built
      as a prerequisite for projects/live_log_monitor. Originally created
      under `02_data_structures/`; moved to `01_basics/` (own choice,
      2026-07-31). Not yet attempted.
- [ ] projects/live_log_monitor — Part III of the log-parsing thread, but as
      a lightly scaffolded project instead of an exercise (my call, since a
      streaming/stateful design has too much open architecture space for a
      fixed-contract self-check). Combines lazy_log_stream's generator skill
      with rolling_error_window's deque skill, extended to per-service
      windows. Do lazy_log_stream and rolling_error_window first. Not yet
      started.
- [ ] 02_data_structures — inventory_manager
- [ ] 03_functions — expense_report
- [ ] 04_files_and_errors — csv_import
- [ ] 05_classes — task_tracker
