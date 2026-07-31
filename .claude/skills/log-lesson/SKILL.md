---
name: log-lesson
description: Commits finished exercise/lesson work to git with a traceable summary (questions asked, struggles, approach, self-check status), and appends a session entry to the ember-vault python-practice project note for cross-app progress tracking. Use when self-check passes on an exercise AND the user signals they're done with it (asking for the next exercise, saying thanks/done, or explicitly asking to log or commit progress). Do not use for every small edit or a failed self-check run.
---

# log-lesson

Goal: every completed lesson leaves two records — a git commit scoped to
that lesson's files, and a session entry in
`~/Documents/ember-vault/projects/python-practice.md` — so progress is
traceable both in this repo's history and across the user's other AI
apps via the vault. Vault path used throughout this skill:
`/Users/bensmith/Documents/ember-vault/projects/python-practice.md`.

## 1. Confirm there's something worth logging

- Run `git status` / `git diff` to see what actually changed under
  `exercises/`, `solutions/`, `projects/`, `README.md`, `CLAUDE.md` since
  the last commit.
- If nothing changed, say so and stop — don't fabricate a session.
- If the exercise's self-check still fails, don't log it as a finished
  lesson. It's fine to skip logging silently here; only commit/log
  partial work if the user explicitly asks to checkpoint in-progress
  work, and if so say clearly in both the commit and the vault entry
  that it's incomplete (state exactly what's left, like the
  `NotImplementedError` in `group_by_service` if that's still the case).

## 2. Reconstruct the session summary from the conversation

Pull from what actually happened in this session, not a generic
template:

- Which exercise (path + topic), and self-check status (pass/fail).
- Questions the user asked (concept lookups, "why isn't this working",
  syntax questions).
- Struggles: hints needed, mistakes made, bugs hit and what caused them
  — be specific enough that re-reading this in a month tells the real
  story, not "had some issues."
- Idioms used, learned, or discussed (e.g. switched to `.get()`,
  discovered `maxsplit`, learned `deque(maxlen=...)`).

Keep it dense — bullet points, scannable in 30 seconds. This mirrors the
vault's own session-entry guidelines (see
`~/Documents/ember-vault/_system/wrap-up-protocol.md` if you want the
full house style).

## 3. Review the final implementation and give feedback

Read the finished file (not just the diff) and actually assess the code
— this is the same "mention a cleaner idiom once it's passing" behavior
CLAUDE.md already asks for during the exercise, just made explicit here
so it isn't skipped and actually gets recorded. Look for things like:

- Duplicated logic that could be one helper instead of two copies.
- Manual patterns where a stdlib shortcut fits (`dict.get`, `setdefault`,
  `Counter`, comprehensions, sequence unpacking, etc.).
- Leftover debug prints, dead code, or unused variables.
- Genuine strengths worth naming, not just problems — e.g. systematic
  debugging (traced actual values instead of guessing), cleaning up
  after themselves unprompted, good edge-case instincts. Progress
  tracking needs the wins recorded too, not only the gaps.

Ground every point in the actual code you just read — don't invent
generic advice. This doesn't mean rewriting their code; per CLAUDE.md,
only mention it, don't apply it unless asked. Keep 2-4 bullets, the
sharpest observations, not an exhaustive lint pass.

## 4. Commit to git

- Stage only the files actually relevant to this lesson (the exercise
  file, and `README.md`/`CLAUDE.md` if they were updated as part of it)
  — never `git add -A` blindly.
- Commit message:
  - Subject: one line, what was done (e.g. `Solve log_analytics.py:
    parse_logs, group_by_service, error_rate_by_service`).
  - Body: the bullets from step 2, condensed. Keep the step 3 feedback
    out of the commit body — that belongs in the vault, not git history.
  - Footer: `Logged in ember-vault: projects/python-practice.md`
- After committing, get the short hash: `git rev-parse --short HEAD`.
  You'll reference it in the vault entry.

## 5. Update the vault project file

Path: `/Users/bensmith/Documents/ember-vault/projects/python-practice.md`

**If the file doesn't exist yet**, create it following the exact shape
of `~/Documents/ember-vault/projects/leetcode-prep.md` (same kind of
learning tracker — read it for the concrete example):

```
---
id: python-practice
name: Python Practice
category: Career
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_at: UNIX_MS
updated_at: UNIX_MS
---

## Where I left off
...

## Next action
...

## Stack
Python (stdlib-only for exercises), uv + ruff, plain-assert self-checks
(no pytest). Repo: python-practice.

## Key decisions
...

## Growth Areas
...

## Related
- [[leetcode-prep]] — same fundamentals-practice track

## Sessions
```

**Every run** (new or existing file):
- Rewrite `## Where I left off` with an accurate current-state summary.
- Rewrite `## Next action` with the single most useful next step.
- Add any genuinely new, durable idiom/decision to `## Key decisions`
  (don't duplicate ones already listed).
- Update `## Growth Areas` with the feedback from step 3:
  - This section tracks *recurring* patterns over time, not a per-session
    dump — it's what makes progress evaluable across sessions instead of
    feedback disappearing into a single chat.
  - If a pattern already listed shows up again, don't duplicate the
    bullet — instead note it's recurring (e.g. add "(seen again in
    log_analytics.py)" or similar) so it's visible this is a real trend,
    not a one-off.
  - If something previously listed as a growth area has clearly been
    fixed/internalized (the user used the idiom unprompted this time),
    move it to a "Resolved" subsection or note it as resolved rather than
    deleting it outright — that's itself useful progress signal.
  - Keep strengths in here too, not just gaps — a feedback log that's
    100% criticism is a worse read of actual progress than one that
    tracks both.
- Append a new entry to `## Sessions`, in the vault's standard format —
  read the last `sess-N` id in the file and increment it:
  ```
  <!-- session {"id":"sess-N","created_at":UNIX_TIMESTAMP} -->
  ### [Title] — YYYY-MM-DD
  - [bullets from step 2]
  - Feedback: [1-2 line condensed version of the step 3 review]
  - commit: <short-hash> "<commit subject>"
  <!-- /session -->
  ```
- Update frontmatter `updated` (date) and `updated_at` (unix ms) to now.
- Never rewrite or delete a past `<!-- session -->` block — only append.

Do **not** touch `~/Documents/ember-vault/_index.md` — the vault's own
`/ember_wrap` protocol doesn't touch it either; that table is maintained
manually by the user.

## 6. Report back

Tell the user, in a few sentences: what got committed (short hash +
subject), the code-quality feedback from step 3, and that the vault
entry was updated/created, with the vault file path.

## Don't

- Don't fire this for every small edit or every failed self-check run —
  only when a lesson is actually done (self-check passes, and the user
  is wrapping up or moving on).
- Don't fabricate struggles, questions, idioms, or feedback that didn't
  actually come up / actually appear in the code you read.
- Don't stage or commit unrelated in-progress work from other exercises.
- Don't touch `_index.md` in the vault.
- Don't turn the step 3 review into unsolicited code changes — feedback
  gets mentioned and logged, not applied, unless the user asks.
