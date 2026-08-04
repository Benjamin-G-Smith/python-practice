"""
Real-world scenario
--------------------
A small e-commerce team dumps customer reviews into a list of dicts and
wants per-category stats: how many reviews each category got, and what
fraction were positive (rating 4 or 5).

This is a different scenario from the log-parsing exercises, but the
same underlying shape: for each category you need to track two related
counts at once (a total, and a subset of that total) as you loop once
over the data - the same shape that caused the off-by-one bug in
log_analytics.py's error_rate_by_service, where treating "increment the
subset counter" and "increment the total counter" as mutually exclusive
(instead of independent) undercounted the total whenever the first
entry for a category happened to land in the subset.

Skills practiced: per-key counting with dict.get(key, 0) + 1 or
collections.defaultdict instead of manual "if key not in dict" branching,
especially when a key needs more than one independent counter.

Run this file directly to see your output and self-check results:
    python review_aggregator.py
"""

from collections import defaultdict

REVIEWS = [
    {"category": "kitchen", "rating": 5},
    {"category": "kitchen", "rating": 2},
    {"category": "outdoor", "rating": 3},
    {"category": "outdoor", "rating": 4},
    {"category": "outdoor", "rating": 5},
    {"category": "kitchen", "rating": 4},
    {"category": "office", "rating": 5},
    {"category": "office", "rating": 1},
    {"category": "outdoor", "rating": 2},
    {"category": "office", "rating": 4},
    {"category": "toys", "rating": 3},
]


def count_by_category(reviews: list[dict]) -> dict[str, int]:
    """
    Return a dict mapping category -> total number of reviews in that
    category.
    """
    counts: dict[str, int] = {}
    for review in reviews:
        counts[review["category"]] = counts.get(review["category"], 0) + 1
    return counts


def positive_rate_by_category(reviews: list[dict]) -> dict[str, float]:
    """
    Return a dict mapping category -> fraction of that category's
    reviews with rating >= 4 ("positive"), rounded to 2 decimal places.

    Each review counts toward its category's total *and*, separately,
    toward its category's positive count if rating >= 4 - these are two
    independent facts about the same review, not an either/or.
    """
    totals: dict[str, int] = defaultdict(int)
    positives: dict[str, int] = defaultdict(int)
    for review in reviews:
        category = review["category"]
        totals[category] += 1
        if review["rating"] >= 4:
            positives[category] += 1
    return {category: round(positives[category] / total, 2) for category, total in totals.items()}


def top_category(reviews: list[dict]) -> str:
    """
    Return the name of the category with the most reviews. If there's a
    tie, return whichever name is alphabetically first.
    """
    counts = count_by_category(reviews)
    return max(counts, key=lambda category: (counts[category], category))


def _self_check() -> None:
    counts = count_by_category(REVIEWS)
    assert counts == {
        "kitchen": 3,
        "outdoor": 4,
        "office": 3,
        "toys": 1,
    }, f"unexpected counts: {counts}"

    rates = positive_rate_by_category(REVIEWS)
    assert rates == {
        "kitchen": 0.67,
        "outdoor": 0.5,
        "office": 0.67,
        "toys": 0.0,
    }, f"unexpected positive rates: {rates}"

    assert top_category(REVIEWS) == "outdoor", f"unexpected top category: {top_category(REVIEWS)}"

    print("All checks passed.")
    print(f"Positive rates: {rates}")


if __name__ == "__main__":
    _self_check()
