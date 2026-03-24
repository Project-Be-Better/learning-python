"""Phase-2 tests for minimal llm client behavior."""

from __future__ import annotations

from common.agent.llm_client import (
    LLMClient,
    resolve_model_for_tier,
)


class StubProvider:
    def __init__(self, value: str) -> None:
        self.value = value

    def invoke(self, prompt: str, model: str) -> str:
        return f"{self.value} {model}: {prompt}"


class FailingProvider:
    def invoke(self, prompt: str, model: str) -> str:
        raise RuntimeError("provider failure")


def test_resolve_model_for_tier_from_env(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_TIER_FAST", "claude-haiku-4-5")

    model = resolve_model_for_tier("fast")

    assert model == "claude-haiku-4-5"


def test_resolve_model_for_tier_default(monkeypatch) -> None:
    monkeypatch.delenv("MODEL_TIER_FAST", raising=False)

    model = resolve_model_for_tier("fast")

    assert model == "fake-fast-model"


def test_generate_uses_openai_as_primary_when_key_exists(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "present")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(openai_provider=StubProvider("[openai]"))
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "openai_primary"
    assert result.model == "model-fast"
    assert result.message == "[openai] model-fast: hello"


def test_generate_uses_claude_as_backup_when_openai_missing(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "present")
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(claude_provider=StubProvider("[claude]"))
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "claude_backup"
    assert result.model == "model-fast"
    assert result.message == "[claude] model-fast: hello"


def test_generate_uses_claude_when_openai_provider_fails(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "present")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "present")
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(
        openai_provider=FailingProvider(),
        claude_provider=StubProvider("[claude]"),
    )
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "claude_backup"
    assert result.message == "[claude] model-fast: hello"


def test_generate_falls_back_without_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(openai_provider=StubProvider("[openai]"), claude_provider=StubProvider("[claude]"))
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "fallback"
    assert result.model == "model-fast"
    assert result.message == "processed:hello"


def test_generate_falls_back_when_both_providers_fail(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "present")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "present")
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(openai_provider=FailingProvider(), claude_provider=FailingProvider())
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "fallback"
    assert result.message == "processed:hello"
