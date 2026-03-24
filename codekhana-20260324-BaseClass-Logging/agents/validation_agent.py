"""Schema validation agent - minimal business logic layer."""

from __future__ import annotations

from typing import Any

from common.agent.base_agent import BaseAgent


class ValidationAgent(BaseAgent):
    """
    Validates input data against a predefined schema.
    
    Demonstrates: Simple pass-through validation agent with output enrichment.
    Pure business logic delegates to base class validation.
    """

    agent_id = "validation_agent"
    model_tier = "fast"
    task_name = "validation_agent.validate"
    queue_name = "validation_queue"

    def input_schema(self) -> dict[str, Any]:
        """Define schema for data to validate."""
        return {
            "data": {"type": "dict", "required": True},
            "schema_name": {"type": "str", "required": True},
        }

    def output_schema(self) -> dict[str, Any]:
        """Output always has is_valid and errors."""
        return {
            "is_valid": {"type": "bool"},
            "errors": {"type": "list"},
        }

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """
        Pure business logic: validate data structure.
        
        For demo, just checks required keys exist.
        In production, would load schema from registry and enforce fully.
        """
        data = input_payload.get("data", {})
        schema_name = input_payload.get("schema_name", "")

        # Simplified validation logic
        errors = []
        
        if not isinstance(data, dict):
            errors.append(f"data must be dict, got {type(data).__name__}")
        
        if schema_name == "trip":
            required_keys = ["trip_id", "duration_min", "distance_km"]
            for key in required_keys:
                if key not in data:
                    errors.append(f"Missing required field: {key}")
        
        elif schema_name == "user":
            required_keys = ["user_id", "email", "name"]
            for key in required_keys:
                if key not in data:
                    errors.append(f"Missing required field: {key}")
        
        else:
            errors.append(f"Unknown schema: {schema_name}")

        is_valid = len(errors) == 0

        return {
            "is_valid": is_valid,
            "errors": errors,
            "validated_schema": schema_name,
        }


def main() -> None:
    agent = ValidationAgent()
    
    # Valid trip data
    valid_trip = {
        "data": {
            "trip_id": "trip-123",
            "duration_min": 45,
            "distance_km": 25.5,
        },
        "schema_name": "trip",
    }
    
    result = agent.run(valid_trip)
    print("\nValid Result:")
    print(result)
    
    # Invalid trip data (missing field)
    invalid_trip = {
        "data": {
            "trip_id": "trip-124",
            "duration_min": 30,
        },
        "schema_name": "trip",
    }
    
    result = agent.run(invalid_trip)
    print("\nInvalid Result:")
    print(result)


if __name__ == "__main__":
    main()
