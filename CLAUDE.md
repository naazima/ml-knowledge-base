# ML Knowledge Base

A personal, offline study companion built from my MIT Applied Data Science Program (via Great Learning) materials, my own notes and my own notebooks. Purpose: keep my ML fundamentals accessible after course access ends, and give me quick daily refreshers I can use in my AI projects.

## Rules (always follow)

1. **Never copy course slides or PDFs verbatim into `cards/`.** Read them for understanding, then write cards in plain, original language. Short technical terms and formulas are fine.
2. **`materials/` is private and must never be committed.** It is in `.gitignore`. Do not move, rename or copy files out of it.
3. **My own work comes first.** When a card can link to one of my notebooks in `notebooks/`, link it.
4. Keep explanations beginner-friendly but technically correct. If unsure about something, say so in the card under "Open questions" rather than guessing.
5. Work in small steps. Finish one card or one feature before starting the next.

## Folder layout

```
materials/        # PRIVATE downloaded course files, one folder per course (gitignored)
notebooks/        # my own notebooks, submissions, capstone, hackathon
cards/<course>/   # one markdown card per algorithm or concept
scripts/          # helper scripts (text extraction, quiz)
mkdocs.yml        # local searchable site
```

Course folders (use these slugs):
foundations-python-stats, data-analysis-visualization, machine-learning, practical-data-science, deep-learning, recommendation-systems, genai, elective-project, capstone-project

## Card template

Every card in `cards/` uses this structure:

```markdown
# <Algorithm / concept name>

**Course:** <course name>
**Type:** supervised | unsupervised | technique | metric | other

## In one sentence
## When to use it
## How it works (simple)
## Key parameters / choices
## Common pitfalls
## How to evaluate it
## Minimal example
(short runnable Python snippet, written fresh, not copied from slides)
## My work
(links to my notebooks that used this, if any)
## Quick quiz
(3 short questions with answers in a collapsible block)
## Open questions
```

## Build phases

- **Phase 1:** folder setup, `.gitignore`, PDF text extraction script, first course's cards (start with `foundations-python-stats`).
- **Phase 2:** MkDocs site with search, run locally (`mkdocs serve`).
- **Phase 3:** `scripts/quiz.py` that picks a random card and asks its quiz questions (daily refresher).
- **Phase 4 (optional):** ask-my-notes chat (RAG over `cards/` and `notebooks/` only, never over `materials/` output shown publicly).

## Tech

Python 3, pypdf (text extraction), MkDocs with Material theme, plain markdown.
