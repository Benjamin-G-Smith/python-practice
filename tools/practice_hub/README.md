# Practice Hub

A local web UI for this repo: a file explorer, code editor with syntax
highlighting, and a terminal panel, plus a button that invokes the real
`refine-questions` skill. It's a companion to Claude Code / Cowork, not
a replacement — you still work exercises the same way, this just gives
you a visual layer on top of the repo.

## Run it

```bash
python tools/practice_hub/server.py
```

Then open <http://localhost:8787>. Stdlib only — no dependencies to
install. It picks up `.venv/bin/python` automatically if you've run
`uv venv`, otherwise falls back to whatever Python started the server.

## What's real vs. still mocked

**Real, backed by this repo on disk:**

- File tree (`exercises/`, `projects/`) — walked live, so new files
  show up on refresh with no code changes needed.
- Self-check status per exercise (the ✓ / dot in the tree) — actually
  runs each file and caches the result by mtime, so it's always
  accurate, not a guess.
- File contents in the editor.
- The **Run** button — executes `python <file>` for real and shows the
  actual stdout/stderr in the terminal panel.
- The **Run refine-questions** button — shells out to
  `claude --dangerously-skip-permissions -p "..."` from the repo root,
  so the real `.claude/skills/refine-questions/SKILL.md` does the
  actual reasoning and writes the actual exercise file. The UI just
  triggers it, shows the raw output, and refreshes the tree.
- `solutions/` is never served by the API at all (not just hidden in
  the UI) — `safe_repo_path()` in `server.py` only allows `exercises/`
  and `projects/`, so the "don't casually browse the answer key" rule
  from `CLAUDE.md` holds server-side too.

**Still sample/mocked — not wired yet:**

- Growth Areas, Dashboard signals, and Sessions panels — still the
  static content from the original mockup. Wiring these means parsing
  `~/Documents/ember-vault/projects/python-practice.md`, which has a
  freeform bullet format (see `log-lesson`'s `SKILL.md`), not a fixed
  schema — worth doing as its own pass once you've seen a few real
  entries to parse against.
- The chat panel — two files (`rolling_error_window.py`,
  `live_log_monitor.py`) show real transcripts from earlier sessions,
  hardcoded in `index.html`'s `MOCK_CHATS`. Every other file shows a
  generic "not wired" message. Making this live means either shelling
  out per message (slow, stateless) or pulling in the Claude Agent SDK
  (a real dependency + ongoing API cost) — deliberately deferred.
- Flashcards deck — trimmed sample cards, not generated from your
  actual Growth Areas yet.
- The "predict your approach" box — UI-only, not persisted anywhere.
  `log-lesson`'s new predict-vs-actual comparison still has to happen
  in chat with Claude, same as before.

## The refine-questions button — permission mode, read before using

Running a skill headlessly needs *both* file-write access (to create
the exercise + edit `README.md`/`CLAUDE.md`) *and* Bash access (to run
the self-check while verifying it) without anything to interactively
approve. `server.py` uses:

```
claude --dangerously-skip-permissions -p "<prompt>"
```

`--dangerously-skip-permissions` disables all permission prompts —
Anthropic's own docs say to use it only in isolated/trusted
environments (see
<https://code.claude.com/docs/en/permission-modes>). This is your own
repo on your own machine, which is a reasonable case for it, but it's
worth knowing what the flag actually does before you click the button
repeatedly. If you want tighter control instead, the alternative is
`--permission-mode dontAsk` combined with an explicit `permissions.allow`
allowlist in `.claude/settings.local.json` naming exactly the paths and
Bash patterns `refine-questions` needs (`Edit(exercises/**)`,
`Edit(solutions/**)`, `Edit(README.md)`, `Edit(CLAUDE.md)`,
`Bash(python exercises/**)`) — more setup, but nothing outside that
list can run. Not built into `server.py` yet; swap the subprocess
command in `do_POST`'s `/api/refine-questions` branch if you want it.

First run may take a minute or two — it's a real model call doing real
file reads/writes, not a canned response.

## Where this lives

This is tooling, not a lesson — it doesn't follow the
`TODO`/`NotImplementedError`/self-check format `CLAUDE.md` defines for
`exercises/`, and it isn't listed in the README's exercise table. It's
also not a `projects/` entry in the pedagogical sense (no scenario
docstring, nothing to "solve"). It lives in `tools/` for that reason,
exempt from those conventions on purpose.

## Iterating on it

- `server.py` — one file, stdlib only, ~230 lines. The route handling
  is a plain if/elif chain in `do_GET`/`do_POST`; add a new endpoint by
  adding a branch.
- `static/index.html` — single file, vanilla JS, no build step. Reload
  the browser after editing; no compile/watch process needed.
- Restart the server after editing `server.py` (`Ctrl+C`, then re-run).
- Good next steps, in rough order of payoff: wire Growth Areas/Sessions
  to the real vault file; make the "predict" box actually persist
  somewhere `log-lesson` can read it back from; add a `log-lesson`
  button next to `refine-questions` for symmetry (same
  `--dangerously-skip-permissions` shell-out pattern, since it also
  needs to `git commit` and write files).
