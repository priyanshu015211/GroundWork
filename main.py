"""GroundWork CLI entry point for the Phase 1 foundation."""

import argparse

from groundwork.config import ConfigurationError, Settings
from groundwork.models import ResearchState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GroundWork — agentic research system")
    parser.add_argument("question", help="Research question or topic")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        settings = Settings.from_env(require_api_keys=False)
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}")
        return 2

    state = ResearchState(original_question=args.question)

    print("GroundWork foundation initialized")
    print(f"Question: {state.original_question}")
    print(f"Model: {settings.model}")
    print(f"Max research rounds: {settings.max_research_rounds}")
    print(f"Max revisions: {settings.max_revisions}")
    print(f"State: {state.summary()}")
    print("Next phase: connect the Planner and Researcher agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
