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

    TODO: implement this function.
    Hint: dict.get(key, 0) + 1, one line per review, no "if key not in
    dict" branch needed.
    """
    categoryCounts = {}
    for review in reviews:
         categoryCounts[review["category"]] = categoryCounts.get(review["category"],0 ) + 1
    
    return categoryCounts



def positive_rate_by_category(reviews: list[dict]) -> dict[str, float]:
    """
    Return a dict mapping category -> fraction of that category's
    reviews with rating >= 4 ("positive"), rounded to 2 decimal places.

    Each review counts toward its category's total *and*, separately,
    toward its category's positive count if rating >= 4 - these are two
    independent facts about the same review, not an either/or. Whatever
    approach you use, make sure a category's total count is exactly its
    number of reviews, regardless of what order positive/non-positive
    reviews appear in.

    TODO: implement this function.
    Hint: collections.defaultdict(int) (or two separate dict.get(key, 0)
    accumulators) can track "total" and "positive" as two independent
    counters per category without needing a branch for "first time
    seeing this category."
    """
    categoryCounts = count_by_category(reviews)
    percentPositive = {}
    positiveCounts = {}
    for review in reviews:
        if review["rating"] >= 4:
            positiveCounts[review["category"]] = positiveCounts.get(review["category"], 0 ) + 1


    for category in categoryCounts.keys():
        if category not in positiveCounts:
            percentPositive[category] = 0.0
        else:
            percent = round((positiveCounts[category] / categoryCounts[category]),2)
            percentPositive[category] = percentPositive.get(category, 0 ) + percent


    return percentPositive


def top_category(reviews: list[dict]) -> str:
    """
    Return the name of the category with the most reviews. If there's a
    tie, return whichever name is alphabetically first.

    TODO: implement this function.
    """
    categoryCounts = count_by_category(reviews)
    topReview = max(categoryCounts,key=lambda k: ( categoryCounts[k], k))


    # alternative 
    # highest_seen = 0
    # topReview = ""
    # for category in categoryCounts:
    #     if categoryCounts[category] > highest_seen:
    #         highest_seen = categoryCounts[category]
    #         topReview = category
    
    return topReview


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
