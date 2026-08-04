---
name: refine-questions
description: Looks at how the user actually solved their most recent exercise (mistakes, hints needed, idioms used, self-check pass/fail) and generates the next exercise calibrated to that — reinforcing a weak spot or escalating difficulty. Use when the user asks for another exercise, a harder problem, wants to be quizzed, or asks what to practice next.
---

# refine-questions

Goal: never hand out the next exercise blind. Read the signal from the last
one first, then decide whether to reinforce or escalate, then build it.

## 1. Gather signal

- Find the exercise the user most recently touched (check file mtimes under
  `exercises/`, or ask if ambiguous).
- Run its self-check: `python exercises/NN_topic/file.py`. Note whether it
  currently passes.
- Diff their implementation against `solutions/NN_topic/file.py` — not to
  judge correctness (the self-check already did that), but to see *how*
  they solved it: loops vs comprehensions, manual dict building vs
  `.get()`/`setdefault`, repeated code vs a helper, whether they used
  stdlib tools the solution uses (`csv`, `pathlib`, etc.).
- Recall from the conversation whether they asked for hints, how many
  attempts it took, and what kind of mistake showed up (off-by-one, wrong
  data structure, mutation bug, missed edge case, etc.).
- Check the "Progress notes" section in `CLAUDE.md` for anything logged
  about this topic before.

## 2. Decide the next exercise

Pick one, in this priority order:

- **Struggled** (multiple failed self-check runs, needed more than one
  hint, or a conceptual mistake like mutating input or off-by-one): write
  a **reinforcing** exercise. Same topic, same skill level, a new
  real-world scenario, but isolate the specific sub-skill that tripped
  them up so it can't be avoided.
- **Passed but non-idiomatic** (self-check green, but they hand-rolled
  something the solution does more simply): write an exercise whose clean
  solution leans on the idiom they missed, without naming it directly —
  let them discover it.
- **Solved cleanly and fast**: escalate. Prefer combining this topic's
  skill with an earlier one (e.g. files + classes) over introducing a
  brand-new isolated concept — real work rarely uses one skill at a time.

Only escalate one step at a time. Don't jump two topics ahead because one
exercise went well.

## 3. Build it

Follow the exact format described in `CLAUDE.md` under "Creating new
exercises": scenario docstring naming the skills it drills, sample data as
module constants, TODO functions raising `NotImplementedError`, a
`_self_check()` with descriptive asserts, a mirrored file in `solutions/`,
and a new row in the README table. Put it in the matching `exercises/NN_topic/`
folder — only create a new topic folder when genuinely moving to a new
subject area, not for a harder variant of an existing one.

Verify the new exercise before handing it over: temporarily fill in the
TODOs using the solution logic, run the self-check, confirm it passes,
then confirm the unsolved exercise version fails cleanly (raises
`NotImplementedError`, not a crash from bad sample data).

### Number it by recommended order, not creation order

The README table's `#` column (`1`, `1b`, `1c`, ...) is read top-to-bottom
as "do them in this order" — it is not a creation log. When the new
exercise belongs *before* other exercises that already exist and are
still unsolved (e.g. a reinforcing exercise inserted ahead of an
already-planned escalation, because the weak spot needs fixing before
building on top of it), give it the number that reflects where it should
actually be attempted, and bump every existing unsolved row after that
point up a letter to keep the sequence unbroken. Solved exercises don't
need renumbering — only reorder rows for exercises that are still
pending, since past history shouldn't shift.

Also update anything else that names the old numbering/order:
- Any "prerequisite" or "do X first" language in other exercises'
  docstrings or `projects/*/README.md` files that reference the
  reordered exercises by name.
- The `CLAUDE.md` "Progress notes" bullet for any exercise that's now
  positioned after the new one — add an explicit "do `<new exercise>`
  first" note if it doesn't already reflect the new order.

If the new exercise is a straightforward escalation appended after
everything else (the common case), it just gets the next letter/number
in sequence — no reordering needed.

## 4. Hand it over

Tell the user in one or two sentences what this exercise reinforces or
escalates and why — not a lecture, just enough intent that they understand
the point. Don't describe the solution approach; that's theirs to find.

## 5. Log it

Append a short line to the "Progress notes" section of `CLAUDE.md`: what
was practiced, what went well or was shaky, and what the new exercise is
targeting. Keep it to one line per exercise so the file stays scannable.

## Don't

- Don't generate more than one new exercise per request unless asked.
- Don't write the new exercise's solution in your chat response — only in
  `solutions/`.
- Don't skip step 1. Generating a generic "next" exercise without checking
  how the last one actually went defeats the entire point of this skill.
