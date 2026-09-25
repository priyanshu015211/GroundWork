"""Application configuration for GroundWork."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(ValueError):
    """Raised when required GroundWork configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str
    tavily_api_key: str
    model: str = "claude-sonnet-4-5"
    max_research_rounds: int = 3
    max_revisions: int = 1

    @classmethod
    def from_env(cls, *, require_api_keys: bool = True) -> "Settings":
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        tavily_key = os.getenv("TAVILY_API_KEY", "").strip()

        if require_api_keys and not anthropic_key:
            raise ConfigurationError("ANTHROPIC_API_KEY is not set.")
        if require_api_keys and not tavily_key:
            raise ConfigurationError("TAVILY_API_KEY is not set.")

        rounds = _positive_int("MAX_RESEARCH_ROUNDS", 3)
        revisions = _non_negative_int("MAX_REVISIONS", 1)
        model = os.getenv("GROUNDWORK_MODEL", "claude-sonnet-4-5").strip()

        if not model:
            raise ConfigurationError("GROUNDWORK_MODEL cannot be empty.")

        return cls(
            anthropic_api_key=anthropic_key,
            tavily_api_key=tavily_key,
            model=model,
            max_research_rounds=rounds,
            max_revisions=revisions,
        )


def _positive_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default)).strip()
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer.") from exc
    if parsed < 1:
        raise ConfigurationError(f"{name} must be >= 1.")
    return parsed


def _non_negative_int(name: str, default: int) -> int:
    value = os.getenv(name, str(default)).strip()
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer.") from exc
    if parsed < 0:
        raise ConfigurationError(f"{name} must be >= 0.")
    return parsed
