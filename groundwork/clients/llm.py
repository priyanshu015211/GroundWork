"""Thin Anthropic client wrapper used by GroundWork agents."""

from anthropic import Anthropic

from groundwork.config import Settings


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.anthropic_api_key:
            raise ValueError("Anthropic API key is required to initialize LLMClient.")
        self._client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model

    def generate(self, prompt: str, *, system: str | None = None, max_tokens: int = 2000) -> str:
        """Generate text while keeping provider-specific details out of agents."""
        if not prompt.strip():
            raise ValueError("prompt cannot be empty.")

        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system or "You are a research assistant. Return accurate, structured output.",
            messages=[{"role": "user", "content": prompt}],
        )

        return "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        ).strip()
