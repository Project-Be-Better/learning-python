"""Minimal LLM client wrapper for Phase 2 wiring.

Behavior:
- Resolves model by tier from environment.
- Uses fake provider by default.
- Falls back to deterministic callback when API key is missing.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol


def resolve_model_for_tier(model_tier: str) -> str:
    """Resolve model id from environment for the given tier."""
    tier = model_tier.strip().upper()
    env_name = f"MODEL_TIER_{tier}"
    return os.getenv(env_name, f"fake-{model_tier}-model")


class LLMProvider(Protocol):
    """Simple provider protocol to allow swapping implementations."""

    def invoke(self, prompt: str, model: str) -> str:
        """Return model-generated text for prompt and model id."""


@dataclass
class FakeLLMProvider:
    """Default fake provider used for local development."""

    prefix: str = "[fake]"

    def invoke(self, prompt: str, model: str) -> str:
        return f"{self.prefix} {model}: {prompt}"


@dataclass
class LLMResult:
    """Structured result of an LLM request."""

    message: str
    model: str
    mode: str  # provider | fallback


class LLMClient:
    """Minimal client that supports provider and deterministic fallback."""

    def __init__(self, provider: LLMProvider | None = None, api_key_env: str = "LLM_API_KEY") -> None:
        self.provider = provider or FakeLLMProvider()
        self.api_key_env = api_key_env

    def has_api_key(self) -> bool:
        primary = os.getenv(self.api_key_env, "").strip()
        if primary:
            return True

        # Compatibility path for provider-specific env naming.
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        return bool(openai_key)

    def generate(self, prompt: str, model_tier: str, fallback: callable) -> LLMResult:
        model = resolve_model_for_tier(model_tier)

        if not self.has_api_key():
            return LLMResult(message=fallback(prompt), model=model, mode="fallback")

        return LLMResult(message=self.provider.invoke(prompt, model), model=model, mode="provider")
