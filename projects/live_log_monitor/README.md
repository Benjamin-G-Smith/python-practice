# Live Log Monitor

This is a **project**, not a scaffolded exercise. There's no `TODO` +
`NotImplementedError` + plain-assert self-check pattern here, and there's
no answer key sitting in a `solutions/` folder. The function signatures
and docstrings in `live_log_monitor.py` are a starting skeleton — treat
them as a suggestion, not a fixed contract. Rename things, change return
shapes, add helper functions, restructure entirely if you want. The goal
is a working monitor you're satisfied with, not passing a fixed test.

## Scenario

`log_analytics.py` (Part II, in `exercises/02_data_structures/`) produces
a batch report after the fact — you feed it a full list of log lines and
it tells you what happened. Ops now wants something that watches lines
**as they arrive** and raises an alert the moment a service's error rate
gets bad, without waiting for a full batch.

## Prerequisites

This project combines two skills that each have their own dedicated
exercise. Do these first if you haven't — they isolate the exact two
techniques this project asks you to put together:

- `exercises/01_basics/lazy_log_stream.py` — generators,
  `yield`, composing generators, and stopping consumption early. Its
  self-check specifically proves your generator is *lazy* (it counts how
  many raw lines get pulled), which is the same property `stream_logs`
  here needs.
- `exercises/01_basics/rolling_error_window.py` —
  `collections.deque(maxlen=...)` for a fixed-size sliding window. It
  works on one flat list; this project's twist is doing that per
  service (a dict of deques instead of one deque).

## Goal

Build a small pipeline with three stages:

1. **Stream** — parse raw log lines lazily, one at a time, instead of
   building a full list up front. This is what makes it "live": a caller
   can start reacting before all the data exists.
2. **Rolling state** — for each service, track its error rate over just
   its most recent N entries (a sliding window), not its entire history.
   A service that had a bad minute an hour ago shouldn't still be
   flagged now.
3. **Alerting** — surface the moments where a service's rolling error
   rate crosses a threshold you choose.

## Suggested approach (feel free to ignore)

- Start with `stream_logs`. This is `parse_line` (already written for
  you — reusing what you already built in the exercises isn't the point
  of this project) wrapped in a generator, same shape as
  `stream_entries` in `lazy_log_stream.py`.
- For the rolling window, `rolling_error_rate` here is
  `rolling_error_window.py`'s function, but per service instead of one
  flat list — you'll need a `dict` mapping service name -> its own
  `deque(maxlen=N)`, instead of a single deque.
- Get `rolling_error_rate` working and just print its output for a bit
  before writing `find_alerts` — watching the rate change entry by entry
  will make it obvious whether your windowing logic is right.
- `find_alerts` is then mostly a filter over what `rolling_error_rate`
  already yields.

## Verifying it works

There's no assert-based self-check to run. Run the file directly:

```bash
python projects/live_log_monitor/live_log_monitor.py
```

and eyeball the printed alerts against `RAW_LOGS` — does the timing and
service match what you'd expect by reading the raw data yourself? If
you want tighter feedback, write your own small `assert` checks at the
bottom of the file as you go — that's encouraged, just not provided.

## Stretch goals

- Add a real-time feel: an optional `delay` parameter on `stream_logs`
  that calls `time.sleep(delay)` between yields, so running the demo
  actually unfolds over a few seconds.
- Track alerts using a small class instead of plain functions, so the
  monitor can hold configuration (window size, threshold) as state
  instead of passing it into every call.
- Once this feels solid, revisit wrapping it behind a real endpoint with
  FastAPI (a separate learning track from these stdlib-only exercises —
  worth doing once the core logic here doesn't need the training wheels).
