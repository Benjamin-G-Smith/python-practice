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

## 3. Review the final implementation

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
- Time and space complexity: name the actual Big-O of what they wrote
  (per relevant function, not the whole file) and whether it's already
  optimal for the problem. This is an explicit standing priority (user
  is optimizing this practice for interview readiness) — always include
  it, not just when a complexity issue happens to stand out. If there's
  a genuine tradeoff in a choice they made (e.g. a data structure that
  costs O(k) extra space vs. one that doesn't, an O(n) approach vs. an
  O(n log n) one), name the tradeoff explicitly rather than assuming
  they'll notice it. If their solution is already optimal, say so
  plainly instead of inventing a nitpick — confirming optimality is
  itself useful signal, not a gap to fill.

Then separately, check for **conceptual** gaps — not the same thing as
code style. A function can be correct, idiomatic, and self-check-green
while the user still doesn't fully understand *why* it works: an
explanation earlier in the conversation that was slightly off before
being corrected, a "did I do this the right way" question that surfaced
a real subtlety, a pattern applied correctly but by copying shape rather
than reasoning (e.g. reused a tuple sort key without being able to say
why the tiebreak works). Pull these from the actual conversation, not
from re-reading the code alone — code review finds style issues,
conceptual gaps mostly show up in how the user talked about the problem.

Read `~/Documents/ember-vault/projects/python-practice.md`'s existing
`## Growth Areas` section (if the file exists) before finalizing either
list — a pattern worth flagging is one that either connects to
established history (recurring, or resolving one already tracked) or is
new and worth starting to track, not a one-off nitpick.

## 4. Present the evaluation and discuss — before committing

This is a checkpoint, not a formality. Tell the user directly, in chat:

- **Patterns to reinforce**: code-level habits from step 3, framed
  against history where relevant ("this is the third time X has come
  up" / "this is resolved — didn't recur this time"). Always include the
  time/space complexity read from step 3 here — either state the actual
  Big-O and confirm it's optimal, or ask the user a direct question
  about their solution's complexity (e.g. "what's the time complexity of
  this loop, and could it be tighter?") when there's a real tradeoff
  worth them reasoning through rather than just being told.
- **Where understanding might be incomplete**: the conceptual gaps from
  step 3, named plainly (what the idea actually is, not just that
  something was slightly off).
- **Genuine strengths**: don't skip these — an evaluation that's only
  gaps is a worse read of real progress than one that shows both.

Give the user room to respond — ask a follow-up, push back, fix
something — before moving on. Once that's settled (they confirm, ask a
question and you answer it, or say to just move on), continue to step 5.
Don't treat this step as skippable busywork before the "real" commit
step; the commit and vault entry in steps 5-6 should reflect whatever
came out of this discussion, not bypass it.

## 5. Commit to git

- Stage only the files actually relevant to this lesson (the exercise
  file, and `README.md`/`CLAUDE.md` if they were updated as part of it)
  — never `git add -A` blindly.
- Commit message:
  - Subject: one line, what was done (e.g. `Solve log_analytics.py:
    parse_logs, group_by_service, error_rate_by_service`).
  - Body: the bullets from step 2, condensed. Keep the step 3/4 feedback
    out of the commit body — that belongs in the vault, not git history.
  - Footer: `Logged in ember-vault: projects/python-practice.md`
- After committing, get the short hash: `git rev-parse --short HEAD`.
  You'll reference it in the vault entry.

## 6. Update the vault project file

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
- Update `## Growth Areas` with the evaluation from steps 3-4 — code
  patterns *and* conceptual gaps, plus anything that came out of the
  discussion in step 4 (a follow-up question, a correction, agreement):
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
  - Feedback: [1-2 line condensed version of the steps 3-4 evaluation]
  - commit: <short-hash> "<commit subject>"
  <!-- /session -->
  ```
- Update frontmatter `updated` (date) and `updated_at` (unix ms) to now.
- Never rewrite or delete a past `<!-- session -->` block — only append.

Do **not** touch `~/Documents/ember-vault/_index.md` — the vault's own
`/ember_wrap` protocol doesn't touch it either; that table is maintained
manually by the user.

## 7. Confirm it's logged

The substantive discussion already happened in step 4 — this is just a
short close-out, not a repeat of the evaluation. Tell the user, in a
sentence or two: what got committed (short hash + subject), and that
the vault entry was updated/created, with the vault file path.

## Don't

- Don't fire this for every small edit or every failed self-check run —
  only when a lesson is actually done (self-check passes, and the user
  is wrapping up or moving on).
- Don't fabricate struggles, questions, idioms, or feedback that didn't
  actually come up / actually appear in the code you read.
- Don't stage or commit unrelated in-progress work from other exercises.
- Don't touch `_index.md` in the vault.
- Don't turn the step 3/4 review into unsolicited code changes — feedback
  gets mentioned and logged, not applied, unless the user asks.
- Don't skip step 4 or fold it silently into step 7's close-out — the
  user asked for this specifically as a distinct discussion checkpoint
  before committing, not a line in a final summary.
