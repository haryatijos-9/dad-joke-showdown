#!/usr/bin/env python3
"""Dad Joke Showdown — @haryatijos-9 entry.

Scores six original dad jokes against the judge's five criteria
(weights 5/4/3/2/1, most important first) and writes the winner to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt). The gate needs
1-200 UTF-8 characters of non-whitespace text.
"""

import os

# Criteria, most important first: (name, weight)
CRITERIA = [
    ("dad_joke", 5),   # a dad joke a father would tell at the table
    ("clean_pun", 4),  # the turn lands on the first read, no explaining
    ("fresh", 3),      # fresh, not a joke told a thousand times
    ("tight", 2),      # every word earns its place, punchline at the end
    ("aloud", 1),      # reads naturally aloud, dinner-table rhythm
]

# Candidate jokes, each with a 0-5 score per criterion (in CRITERIA order).
# Scores are my own judgement of each line against the published brief.
CANDIDATES = [
    {
        "text": "I told my guitar it was out of tune. It said, \"I'm just fretting about it.\"",
        "scores": [5, 5, 5, 5, 5],
    },
    {
        "text": "I told the microwave it was too loud. It beeped at me for five minutes — I guess I really pushed its buttons.",
        "scores": [5, 4, 4, 3, 4],
    },
    {
        "text": "The sink was leaking, so I called a plumber. He said, \"Looks like you've got a draining problem.\"",
        "scores": [5, 4, 3, 4, 4],
    },
    {
        "text": "I told my computer I needed a break. Now it won't stop sending me KitKat ads.",
        "scores": [4, 4, 3, 4, 4],
    },
    {
        "text": "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
        "scores": [5, 4, 2, 4, 4],
    },
    {
        "text": "I asked the calendar for a day off. It said, \"Sorry, I'm booked solid through December.\"",
        "scores": [4, 3, 3, 4, 3],
    },
]


def total(candidate):
    return sum(score * weight for score, (_, weight) in zip(candidate["scores"], CRITERIA))


def pick_winner():
    ranked = sorted(CANDIDATES, key=total, reverse=True)
    return ranked[0], ranked


def main():
    winner, ranked = pick_winner()
    joke = winner["text"]
    assert 1 <= len(joke) <= 200, f"joke must be 1-200 chars, got {len(joke)}"
    assert joke.strip(), "joke must not be only whitespace"
    # The winner must beat the runner-up outright: a tie would make the
    # pick depend on list order instead of the scores.
    margin = total(ranked[0]) - total(ranked[1])
    assert margin > 0, "winner must beat runner-up outright"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(joke)
    for cand in ranked:
        print(f"{total(cand):3d}  {cand['text']}")
    print(f"winner ({len(joke)} chars, margin +{margin}): {joke}")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
