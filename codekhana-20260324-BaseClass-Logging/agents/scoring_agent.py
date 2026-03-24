"""Lightweight ScoringAgent - pure business logic on thick base."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    from common.agent.base_agent import BaseAgent
except ModuleNotFoundError:
    # Support direct script execution: `python agents/scoring_agent.py`
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
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
    scoring_version = "sprint2-rule-based-v2"
    permitted_tools = ["redis_read", "redis_write", "llm_call"]
    permitted_tables = {
        "read": ["trips", "telemetry_events"],
        "write": ["trip_scores", "fairness_audit_log", "driver_scores"],
    }

    def input_schema(self) -> dict[str, Any]:
        """Define top-level input contract with defaults for optional lists."""
        return {
            "trip_id": {"type": "str", "required": False, "default": "unknown-trip"},
            "context": {"type": "dict", "required": False, "default": {}},
            "smoothness_logs": {"type": "list", "required": False, "default": []},
            "harsh_events": {"type": "list", "required": False, "default": []},
            # Legacy fallback fields (kept for compatibility)
            "harsh_brakes": {"type": "int", "required": False, "default": 0, "min": 0},
            "speeding_events": {"type": "int", "required": False, "default": 0, "min": 0},
            "phone_distractions": {"type": "int", "required": False, "default": 0, "min": 0},
            "trip_km": {"type": "float", "required": False, "default": 1.0, "min": 0.1},
        }

    def pre_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Normalize both spec-contract input and legacy flat input into one internal shape."""
        context = input_payload.get("context") or {}
        smoothness_logs = input_payload.get("smoothness_logs") or []
        harsh_events = input_payload.get("harsh_events") or []

        trip_id = str(
            context.get("trip_id")
            or input_payload.get("trip_id")
            or "unknown-trip"
        )

        summary = context.get("trip_summary") or {}
        trip_km = float(summary.get("distance_km") or input_payload.get("trip_km") or 1.0)
        trip_km = max(0.1, trip_km)

        # Backward-compatible fallback: if no harsh event list is provided, synthesize counts.
        if not harsh_events:
            harsh_brakes = int(input_payload.get("harsh_brakes", 0))
            speeding_events = int(input_payload.get("speeding_events", 0))
            phone_distractions = int(input_payload.get("phone_distractions", 0))
            synthetic_count = max(0, harsh_brakes + speeding_events + phone_distractions)
            harsh_events = [{"event_type": "harsh_brake"} for _ in range(synthetic_count)]

        return {
            "trip_id": trip_id,
            "context": context,
            "smoothness_logs": smoothness_logs,
            "harsh_events": harsh_events,
            "trip_km": trip_km,
        }

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """Compute smoothness score and separate harsh-event coaching flags."""
        trip_id = input_payload["trip_id"]
        trip_km = float(input_payload["trip_km"])
        smoothness_logs = input_payload.get("smoothness_logs", [])
        harsh_events = input_payload.get("harsh_events", [])

        smoothness_features = self._extract_smoothness_features(smoothness_logs)
        scoring = self._score_from_smoothness(smoothness_features)
        coaching_flags = self._build_coaching_flags(harsh_events, trip_km)

        # Compatibility fields for existing tests/consumers.
        score = scoring["trip_score"]
        if score >= 80:
            band = "low_risk"
        elif score >= 60:
            band = "moderate_risk"
        else:
            band = "high_risk"

        recommendations = list(coaching_flags["recommended_actions"])
        if not recommendations:
            recommendations = ["Good driving profile. Maintain current behavior."]

        return {
            "trip_id": trip_id,
            "trip_score": scoring["trip_score"],
            "score_label": scoring["score_label"],
            "score_breakdown": scoring["score_breakdown"],
            "coaching_flags": coaching_flags,
            "shap_values": {},
            "fairness_flags": {
                "status": "not_computed",
                "demographic_parity_check": False,
            },
            "scoring_version": self.scoring_version,
            # Backward-compatible fields
            "score": scoring["trip_score"],
            "band": band,
            "recommendations": recommendations,
            "metrics": {
                "trip_km": trip_km,
                "harsh_event_count": len(harsh_events),
                **smoothness_features,
            },
        }

    def _extract_smoothness_features(self, windows: list[dict[str, Any]]) -> dict[str, float]:
        """Aggregate smoothness windows into model-like numeric features."""
        if not windows:
            return {
                "jerk_mean_avg": 1.8,
                "accel_std_avg": 1.7,
                "speed_std_avg": 8.0,
                "rpm_std_avg": 420.0,
                "idle_ratio": 0.10,
            }

        def _to_float(record: dict[str, Any], keys: list[str], default: float) -> float:
            for key in keys:
                value = record.get(key)
                if value is not None:
                    try:
                        return float(value)
                    except (TypeError, ValueError):
                        continue
            return default

        jerk_vals = [_to_float(w, ["jerk_mean", "jerk_std", "jerk_rms"], 1.8) for w in windows]
        accel_vals = [_to_float(w, ["accel_std", "accel_variance", "accel_rms"], 1.7) for w in windows]
        speed_vals = [_to_float(w, ["speed_std", "speed_variance"], 8.0) for w in windows]
        rpm_vals = [_to_float(w, ["rpm_std", "engine_rpm_std"], 420.0) for w in windows]
        idle_vals = [_to_float(w, ["idle_ratio", "idle_time_ratio"], 0.10) for w in windows]

        return {
            "jerk_mean_avg": round(sum(jerk_vals) / len(jerk_vals), 4),
            "accel_std_avg": round(sum(accel_vals) / len(accel_vals), 4),
            "speed_std_avg": round(sum(speed_vals) / len(speed_vals), 4),
            "rpm_std_avg": round(sum(rpm_vals) / len(rpm_vals), 4),
            "idle_ratio": round(sum(idle_vals) / len(idle_vals), 4),
        }

    def _score_from_smoothness(self, features: dict[str, float]) -> dict[str, Any]:
        """Rule-based smoothness score (harsh events are excluded by design)."""
        jerk_penalty = min(30.0, max(0.0, (features["jerk_mean_avg"] - 1.0) * 12.0))
        accel_penalty = min(20.0, max(0.0, (features["accel_std_avg"] - 1.0) * 10.0))
        speed_penalty = min(15.0, max(0.0, (features["speed_std_avg"] - 6.0) * 1.2))
        rpm_penalty = min(10.0, max(0.0, (features["rpm_std_avg"] - 350.0) * 0.02))
        idle_penalty = min(8.0, max(0.0, (features["idle_ratio"] - 0.08) * 30.0))

        total_penalty = jerk_penalty + accel_penalty + speed_penalty + rpm_penalty + idle_penalty
        trip_score = round(max(0.0, min(100.0, 100.0 - total_penalty)), 2)

        if trip_score >= 85:
            label = "Excellent"
        elif trip_score >= 70:
            label = "Good"
        elif trip_score >= 55:
            label = "Average"
        elif trip_score >= 40:
            label = "Below Average"
        else:
            label = "Poor"

        return {
            "trip_score": trip_score,
            "score_label": label,
            "score_breakdown": {
                "base": 100.0,
                "penalties": {
                    "jerk": round(jerk_penalty, 2),
                    "acceleration_variability": round(accel_penalty, 2),
                    "speed_variability": round(speed_penalty, 2),
                    "rpm_variability": round(rpm_penalty, 2),
                    "idle_ratio": round(idle_penalty, 2),
                },
                "total_penalty": round(total_penalty, 2),
            },
        }

    def _build_coaching_flags(self, harsh_events: list[dict[str, Any]], trip_km: float) -> dict[str, Any]:
        """Build coaching decision from harsh-event density and safety context."""
        event_count = len(harsh_events)
        events_per_100km = round((event_count / max(trip_km, 0.1)) * 100.0, 2)

        recommended_actions: list[str] = []
        recommended_action_levels = [
            (event.get("safety_context") or {}).get("recommended_action", "")
            for event in harsh_events
        ]
        has_escalate = any(level == "escalate" for level in recommended_action_levels)
        has_coach = any(level == "coach" for level in recommended_action_levels)

        if has_escalate:
            recommended_actions.append("Escalate to fleet manager due to safety-critical context.")
        elif has_coach:
            recommended_actions.append("Coaching recommended from Safety Agent event context.")

        if trip_km < 10.0:
            coaching_required = False
            reason = "trip_below_min_distance"
        elif events_per_100km >= 8.0:
            coaching_required = True
            reason = "high_harsh_event_density"
            recommended_actions.append("High harsh-event rate per 100km. Prioritize coaching review.")
        elif events_per_100km >= 4.0:
            coaching_required = True
            reason = "moderate_harsh_event_density"
            recommended_actions.append("Moderate harsh-event rate. Monitor and coach where needed.")
        else:
            coaching_required = False
            reason = "within_threshold"

        # Keep action list stable and deduplicated.
        dedup_actions = list(dict.fromkeys(recommended_actions))

        return {
            "coaching_required": coaching_required,
            "reason": reason,
            "harsh_event_count": event_count,
            "events_per_100km": events_per_100km,
            "recommended_actions": dedup_actions,
        }


def main() -> None:
    agent = ScoringAgent()
    sample = {
        "context": {
            "trip_id": "trip-001",
            "trip_summary": {
                "distance_km": 12.4,
                "duration_minutes": 24,
                "window_count": 2,
            },
        },
        "smoothness_logs": [
            {"jerk_mean": 1.6, "accel_std": 1.4, "speed_std": 7.2, "rpm_std": 410, "idle_ratio": 0.08},
            {"jerk_mean": 1.9, "accel_std": 1.6, "speed_std": 8.3, "rpm_std": 430, "idle_ratio": 0.10},
        ],
        "harsh_events": [
            {"event_type": "harsh_brake", "safety_context": {"recommended_action": "coach"}},
            {"event_type": "harsh_brake", "safety_context": {"recommended_action": "monitor"}},
        ],
    }
    result = agent.run(sample)
    print(result)


if __name__ == "__main__":
    main()
