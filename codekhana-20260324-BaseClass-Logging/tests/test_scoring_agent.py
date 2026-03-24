"""Tests for the ScoringAgent lifecycle and scoring behavior."""

from __future__ import annotations

from agents.scoring_agent import ScoringAgent



def test_scoring_agent_returns_expected_shape() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "trip_id": "trip-101",
            "harsh_brakes": 1,
            "speeding_events": 0,
            "phone_distractions": 0,
            "trip_km": 8,
        }
    )

    assert output["agent"] == "scoring_agent"
    assert output["trip_id"] == "trip-101"
    assert isinstance(output["score"], float)
    assert output["band"] in {"low_risk", "moderate_risk", "high_risk"}
    assert isinstance(output["recommendations"], list)



def test_scoring_agent_high_risk_path() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "trip_id": "trip-202",
            "harsh_brakes": 8,
            "speeding_events": 6,
            "phone_distractions": 4,
            "trip_km": 15,
        }
    )

    assert output["band"] == "high_risk"
    assert output["score"] < 60



def test_scoring_agent_low_risk_path() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "trip_id": "trip-303",
            "harsh_brakes": 0,
            "speeding_events": 0,
            "phone_distractions": 0,
            "trip_km": 5,
        }
    )

    assert output["band"] == "low_risk"
    assert output["score"] >= 80



def test_scoring_agent_uses_supported_engine() -> None:
    agent = ScoringAgent()
    _ = agent.run({
        "trip_id": "trip-404",
        "harsh_brakes": 0,
        "speeding_events": 0,
        "phone_distractions": 0,
        "trip_km": 5.0,
    })

    assert agent.execution_state["engine"] in {"langgraph", "sequential"}
    assert agent.execution_trace == ["pre_process", "core_process", "post_process"]
