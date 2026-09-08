# Groundwork

An autonomous research agent. Give it a topic — it plans sub-questions, searches
the web, extracts sourced claims, iteratively figures out what's still missing,
critiques its own draft, and writes a cited report.

The interesting part isn't the search step — it's the loop: deciding what to
look up next based on what's already been found, and checking whether the
final report actually answers the question instead of just dumping info.

## How it works

```
topic
  │
  ▼
Planner ──► generates 3-5 sub-questions
  │
  ▼
┌─────────────────────────────┐
│  Research loop (per round)  │
│  search → read → extract    │──► sourced claims
│  claims for each question   │
└─────────────────────────────┘
  │
  ▼
Planner (again) ──► "what's still missing/contradicted?" ──► more sub-questions
  │                                                              │
  │◄─────────────────────────────────────────────────────────────┘
  ▼ (repeat until sufficient or max rounds)
Writer ──► draft report with [n] citations
  │
  ▼
Critic ──► checks for unsourced claims, un-synthesized info dumps,
│           unacknowledged contradictions, dodged questions
  ▼
Revise (if issues found) ──► final report
```

## Setup

```bash
git clone <this repo>
cd groundwork
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in ANTHROPIC_API_KEY and TAVILY_API_KEY in .env
```

You'll need:
- An [Anthropic API key](https://console.anthropic.com/)
- A [Tavily API key](https://tavily.com/) (free tier is enough to get started)

Load the `.env` file however you like — e.g. `export $(cat .env | xargs)`,
or use `python-dotenv` if you'd rather load it in code.

## Usage

```bash
python main.py "Impact of remote work on urban commercial real estate"
```

Options:

```bash
python main.py "Your topic here" \
  --rounds 2 \        # max research loop rounds (default: 3)
  --revisions 1 \     # max critique/revision passes (default: 1)
  --out report.md     # write to a file instead of stdout
```

## Project structure

```
groundwork/
├── groundwork/
│   ├── __init__.py
│   └── agent.py       # planner, researcher, critic, writer, main loop
├── main.py             # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Where this tends to break (and what to try)

- **Shallow sub-questions** — if the planner keeps generating generic
  questions, try giving it a few examples of good vs. bad sub-questions
  in the prompt.
- **Endless looping** — if it never converges, tighten the "sufficient"
  criteria in the planner prompt, or just lower `--rounds`.
- **Citation hallucination** — the critic pass catches a lot of this, but
  for anything high-stakes you'd want a dedicated step that checks each
  cited claim against the actual extracted source text, not just trusts
  the model's self-report.
- **Low-quality search results** — Tavily filters some SEO spam already,
  but for niche topics you may want to add a relevance/quality filter
  before extracting claims.

## Roadmap ideas

- Parallelize claim extraction across sources (currently sequential)
- Add a dedicated citation-verification step (claim text vs. source text)
- Cache search results/claims so repeated runs on the same topic are cheap
- Swap in a different search provider or add multi-provider fallback
- Export to PDF/HTML in addition to markdown
