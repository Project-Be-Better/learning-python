"""Tests for the ScoringAgent lifecycle and scoring behavior."""

from __future__ import annotations

from agents.scoring_agent import ScoringAgent



def test_scoring_agent_returns_expected_shape() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "context": {
                "trip_id": "trip-101",
                "trip_summary": {"distance_km": 8.0, "duration_minutes": 15},
            },
            "smoothness_logs": [
                {"jerk_mean": 1.3, "accel_std": 1.2, "speed_std": 6.5, "rpm_std": 360, "idle_ratio": 0.06},
            ],
            "harsh_events": [],
        }
    )

    assert output["agent"] == "scoring_agent"
    assert output["trip_id"] == "trip-101"
    assert isinstance(output["trip_score"], float)
    assert output["score_label"] in {"Excellent", "Good", "Average", "Below Average", "Poor"}
    assert "score_breakdown" in output
    assert "coaching_flags" in output
    assert "fairness_flags" in output
    assert isinstance(output["recommendations"], list)



def test_scoring_agent_poor_smoothness_path() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "context": {
                "trip_id": "trip-202",
                "trip_summary": {"distance_km": 15.0, "duration_minutes": 45},
            },
            "smoothness_logs": [
                {"jerk_mean": 3.8, "accel_std": 3.2, "speed_std": 21.0, "rpm_std": 980, "idle_ratio": 0.28},
                {"jerk_mean": 4.2, "accel_std": 3.5, "speed_std": 23.0, "rpm_std": 1050, "idle_ratio": 0.30},
            ],
            # harsh events are intentionally not part of score calculation
            "harsh_events": [{"event_type": "harsh_brake"}] * 10,
        }
    )

    assert output["score_label"] in {"Below Average", "Poor"}
    assert output["score"] < 60



def test_scoring_agent_good_smoothness_path() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "context": {
                "trip_id": "trip-303",
                "trip_summary": {"distance_km": 12.0, "duration_minutes": 35},
            },
            "smoothness_logs": [
                {"jerk_mean": 1.1, "accel_std": 1.05, "speed_std": 5.8, "rpm_std": 340, "idle_ratio": 0.04},
                {"jerk_mean": 1.2, "accel_std": 1.1, "speed_std": 6.1, "rpm_std": 350, "idle_ratio": 0.05},
            ],
            "harsh_events": [],
        }
    )

    assert output["score_label"] in {"Excellent", "Good"}
    assert output["score"] >= 80


def test_scoring_agent_coaching_uses_harsh_events_not_score() -> None:
    agent = ScoringAgent()
    output = agent.run(
        {
            "context": {
                "trip_id": "trip-350",
                "trip_summary": {"distance_km": 20.0, "duration_minutes": 40},
            },
            # smooth driving should keep score high
            "smoothness_logs": [
                {"jerk_mean": 1.1, "accel_std": 1.1, "speed_std": 6.0, "rpm_std": 350, "idle_ratio": 0.05},
            ],
            # many harsh events should trigger coaching flag independently
            "harsh_events": [{"event_type": "harsh_brake", "safety_context": {"recommended_action": "coach"}}] * 3,
        }
    )

    assert output["trip_score"] >= 80
    assert output["coaching_flags"]["coaching_required"] is True
    assert output["coaching_flags"]["events_per_100km"] >= 4.0



def test_scoring_agent_uses_supported_engine() -> None:
    agent = ScoringAgent()
    _ = agent.run(
        {
            "context": {
                "trip_id": "trip-404",
                "trip_summary": {"distance_km": 10.0},
            },
            "smoothness_logs": [
                {"jerk_mean": 1.4, "accel_std": 1.3, "speed_std": 6.4, "rpm_std": 365, "idle_ratio": 0.07},
            ],
            "harsh_events": [],
        }
    )

    assert agent.execution_state["engine"] in {"langgraph", "sequential"}
    assert agent.execution_trace == ["pre_process", "core_process", "post_process"]
