"""Phase-2 tests for minimal llm client behavior."""

from __future__ import annotations

from common.agent.llm_client import FakeLLMProvider, LLMClient, resolve_model_for_tier


def test_resolve_model_for_tier_from_env(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_TIER_FAST", "claude-haiku-4-5")

    model = resolve_model_for_tier("fast")

    assert model == "claude-haiku-4-5"


def test_resolve_model_for_tier_default(monkeypatch) -> None:
    monkeypatch.delenv("MODEL_TIER_FAST", raising=False)

    model = resolve_model_for_tier("fast")

    assert model == "fake-fast-model"


def test_generate_uses_provider_when_api_key_exists(monkeypatch) -> None:
    monkeypatch.setenv("LLM_API_KEY", "present")
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(provider=FakeLLMProvider(prefix="[provider]"))
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "provider"
    assert result.model == "model-fast"
    assert result.message == "[provider] model-fast: hello"


def test_generate_falls_back_without_api_key(monkeypatch) -> None:
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.setenv("MODEL_TIER_FAST", "model-fast")

    client = LLMClient(provider=FakeLLMProvider(prefix="[provider]"))
    result = client.generate("hello", model_tier="fast", fallback=lambda p: f"processed:{p}")

    assert result.mode == "fallback"
    assert result.model == "model-fast"
    assert result.message == "processed:hello"
