"""Lightweight ScoringAgent - pure business logic on thick base."""

from __future__ import annotations

from typing import Any

from common.agent.base_agent import BaseAgent


class ScoringAgent(BaseAgent):
    """
    Compute driving risk score - example of minimal agent.

    Demonstrates thick base: only core_process is implemented.
    Input validation, output enrichment handled automatically.
    """

    agent_id = "scoring_agent"
    model_tier = "fast"
    system_prompt = "You are a driving risk scoring assistant."
    task_name = "scoring_agent.score_trip"
    queue_name = "scoring_queue"

    def input_schema(self) -> dict[str, Any]:
        """Define input validation."""
        return {
            "trip_id": {"type": "str", "required": True},
            "harsh_brakes": {"type": "int", "required": True, "min": 0},
            "speeding_events": {"type": "int", "required": True, "min": 0},
            "phone_distractions": {"type": "int", "required": True, "min": 0},
            "trip_km": {"type": "float", "required": True, "min": 0.1},
        }

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Pure business logic: compute risk score from validated inputs."""
        harsh_brakes = input_payload["harsh_brakes"]
        speeding_events = input_payload["speeding_events"]
        phone_distractions = input_payload["phone_distractions"]
        trip_km = input_payload["trip_km"]

        weighted_risk = (harsh_brakes * 4.0) + (speeding_events * 3.0) + (phone_distractions * 5.0)
        distance_factor = min(1.0, trip_km / 10.0)
        normalized_penalty = weighted_risk * (0.5 + (0.5 * distance_factor))
        score = max(0, round(100.0 - normalized_penalty, 2))

        if score >= 80:
            band = "low_risk"
        elif score >= 60:
            band = "moderate_risk"
        else:
            band = "high_risk"

        recommendations: list[str] = []
        if harsh_brakes > 0:
            recommendations.append("Reduce sudden braking by keeping more distance.")
        if speeding_events > 0:
            recommendations.append("Maintain speed within limit for better consistency.")
        if phone_distractions > 0:
            recommendations.append("Avoid phone use while driving to reduce risk.")
        if not recommendations:
            recommendations.append("Good driving profile. Maintain current behavior.")

        return {
            "trip_id": input_payload["trip_id"],
            "score": score,
            "band": band,
            "recommendations": recommendations,
            "metrics": {
                "harsh_brakes": harsh_brakes,
                "speeding_events": speeding_events,
                "phone_distractions": phone_distractions,
                "trip_km": trip_km,
            },
        }


def main() -> None:
    agent = ScoringAgent()
    sample = {
        "trip_id": "trip-001",
        "harsh_brakes": 3,
        "speeding_events": 2,
        "phone_distractions": 1,
        "trip_km": 12.4,
    }
    result = agent.run(sample)
    print(result)


if __name__ == "__main__":
    main()
