# ML Knowledge Base

A personal, offline study companion for machine learning, built with [Claude Code](https://claude.com/claude-code) from what I learned in the MIT Applied Data Science Program. I'm building it so I keep access to my ML fundamentals after my course account closes, and so I have quick daily refreshers for my own AI projects.

This is a work in progress and a learning project, not a course or a reference to rely on.

## How it works

- **Private course files stay local.** They live in `materials/`, which is gitignored and never committed.
- **An extraction script turns notebooks into text.** `scripts/extract_notebooks.py` converts notebooks into plain text that I (and Claude) can read for understanding.
- **Cards are written in my own words.** Each concept or algorithm gets one markdown card in `cards/<course>/`, following a fixed template: one-sentence summary, when to use it, how it works, key parameters, pitfalls, evaluation, a minimal example, links to my own notebooks, a short quiz, and open questions where I'm unsure.

## Progress

Currently working through **Foundations > Data Visualization** (see the [card index](cards/foundations-python-stats/README.md)):

- Done: Boxplot, Histogram
- Remaining: 7 more cards in this section

Other courses are not started yet.

## Roadmap

1. **Phase 1 (in progress):** project setup, extraction script, first course's cards.
2. **Phase 2:** a local, searchable MkDocs site (Material theme), run with `mkdocs serve`.
3. **Phase 3:** `scripts/quiz.py`, which picks a random card and asks its quiz questions as a daily refresher.
4. **Phase 4 (optional):** an ask-my-notes chat over my own cards and notebooks.

## How I work

I use Claude Code with a simple loop: **explore → plan → code → commit.** I look at what exists, agree on a small plan, build one card or feature at a time, then commit it before starting the next.
