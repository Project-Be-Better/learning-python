"""Production-oriented LLM client wrapper.

Behavior:
- Resolves model by tier from environment.
- Uses OpenAI as primary provider when key is available.
- Uses Claude (Anthropic) as backup provider when available.
- Falls back to deterministic callback if both providers are unavailable/fail.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from time import sleep
from typing import Callable, Protocol


def resolve_model_for_tier(model_tier: str) -> str:
    """Resolve model id from environment for the given tier."""
    tier = model_tier.strip().upper()
    env_name = f"MODEL_TIER_{tier}"
    return os.getenv(env_name, f"fake-{model_tier}-model")


class LLMProvider(Protocol):
    """Simple provider protocol to allow swapping implementations."""

    def invoke(self, prompt: str, model: str) -> str:
        """Return model-generated text for prompt and model id."""


class ProviderUnavailableError(RuntimeError):
    """Raised when provider cannot be used due to missing credentials."""


class ProviderInvokeError(RuntimeError):
    """Raised when provider fails after retries."""


@dataclass
class LLMResult:
    """Structured result of an LLM request."""

    message: str
    model: str
    mode: str  # openai_primary | claude_backup | fallback


@dataclass
class OpenAIProvider:
    """OpenAI chat provider with basic retry handling."""

    api_key: str
    timeout_seconds: float = 20.0
    max_retries: int = 2

    def invoke(self, prompt: str, model: str) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderInvokeError("openai package is not installed") from exc

        client = OpenAI(api_key=self.api_key, timeout=self.timeout_seconds)
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = client.responses.create(model=model, input=prompt)
                text = getattr(response, "output_text", "")
                if text:
                    return text
                raise ProviderInvokeError("OpenAI response contained no output_text")
            except Exception as exc:  # SDK-specific errors vary by version.
                last_error = exc
                if attempt < self.max_retries:
                    sleep(0.5 * (attempt + 1))
                    continue
                break

        raise ProviderInvokeError(f"OpenAI invocation failed: {last_error}")


@dataclass
class ClaudeProvider:
    """Anthropic messages provider with basic retry handling."""

    api_key: str
    timeout_seconds: float = 20.0
    max_retries: int = 2

    def invoke(self, prompt: str, model: str) -> str:
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ProviderInvokeError("anthropic package is not installed") from exc

        client = Anthropic(api_key=self.api_key, timeout=self.timeout_seconds)
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=512,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = getattr(response, "content", [])
                if not content:
                    raise ProviderInvokeError("Anthropic response content is empty")
                text = getattr(content[0], "text", "")
                if text:
                    return text
                raise ProviderInvokeError("Anthropic response had no text segment")
            except Exception as exc:  # SDK-specific errors vary by version.
                last_error = exc
                if attempt < self.max_retries:
                    sleep(0.5 * (attempt + 1))
                    continue
                break

        raise ProviderInvokeError(f"Anthropic invocation failed: {last_error}")


class LLMClient:
    """Minimal client with provider priority and deterministic fallback."""

    def __init__(
        self,
        openai_provider: LLMProvider | None = None,
        claude_provider: LLMProvider | None = None,
    ) -> None:
        self._openai_provider = openai_provider
        self._claude_provider = claude_provider

    def has_openai_key(self) -> bool:
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        if openai_key:
            return True

        # Compatibility path from earlier phase naming.
        generic_key = os.getenv("LLM_API_KEY", "").strip()
        return bool(generic_key)

    def has_claude_key(self) -> bool:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if anthropic_key:
            return True

        claude_key = os.getenv("CLAUDE_API_KEY", "").strip()
        return bool(claude_key)

    def _get_openai_provider(self) -> LLMProvider:
        if self._openai_provider is not None:
            return self._openai_provider

        openai_key = os.getenv("OPENAI_API_KEY", "").strip() or os.getenv("LLM_API_KEY", "").strip()
        if not openai_key:
            raise ProviderUnavailableError("OpenAI key not available")
        self._openai_provider = OpenAIProvider(api_key=openai_key)
        return self._openai_provider

    def _get_claude_provider(self) -> LLMProvider:
        if self._claude_provider is not None:
            return self._claude_provider

        claude_key = os.getenv("ANTHROPIC_API_KEY", "").strip() or os.getenv("CLAUDE_API_KEY", "").strip()
        if not claude_key:
            raise ProviderUnavailableError("Claude key not available")
        self._claude_provider = ClaudeProvider(api_key=claude_key)
        return self._claude_provider

    def generate(self, prompt: str, model_tier: str, fallback: Callable[[str], str]) -> LLMResult:
        model = resolve_model_for_tier(model_tier)

        if self.has_openai_key():
            try:
                provider = self._get_openai_provider()
                return LLMResult(
                    message=provider.invoke(prompt, model),
                    model=model,
                    mode="openai_primary",
                )
            except Exception:
                # Continue to Claude backup path.
                pass

        if self.has_claude_key():
            try:
                provider = self._get_claude_provider()
                return LLMResult(
                    message=provider.invoke(prompt, model),
                    model=model,
                    mode="claude_backup",
                )
            except Exception:
                # Final deterministic fallback below.
                pass

        return LLMResult(message=fallback(prompt), model=model, mode="fallback")
