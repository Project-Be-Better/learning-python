"""Data fetch agent - retrieves and transforms data with minimal business logic."""

from __future__ import annotations

from typing import Any

from common.agent.base_agent import BaseAgent


class DataFetchAgent(BaseAgent):
    """
    Fetch and transform data from a data source.
    
    Demonstrates: Multi-step business logic (fetch + transform).
    Input schema enforces data source and query parameters.
    Output schema guarantees result structure.
    """

    agent_id = "data_fetch_agent"
    model_tier = "balanced"
    task_name = "data_fetch_agent.fetch_transform"
    queue_name = "data_fetch_queue"
    max_retries = 2

    def input_schema(self) -> dict[str, Any]:
        """Define input requirements."""
        return {
            "source": {"type": "str", "required": True},  # "trips" | "users"
            "query_id": {"type": "str", "required": True},
            "limit": {"type": "int", "required": False, "default": 10, "min": 1, "max": 100},
        }

    def output_schema(self) -> dict[str, Any]:
        """Define output structure."""
        return {
            "source": {"type": "str"},
            "query_id": {"type": "str"},
            "record_count": {"type": "int", "min": 0},
        }

    def core_process(self, input_payload: dict[str, Any]) -> dict[str, Any]:
        """
        Pure business logic: fetch data and compute aggregates.
        
        In production, would query actual data sources.
        Here simulates with mock data.
        """
        source = input_payload["source"]
        query_id = input_payload["query_id"]
        limit = input_payload.get("limit", 10)

        # Simulate fetching from a data source
        if source == "trips":
            records = self._fetch_trips(query_id, limit)
        elif source == "users":
            records = self._fetch_users(query_id, limit)
        else:
            records = []

        # Compute simple stats
        total_value = sum(r.get("value", 0) for r in records)

        return {
            "source": source,
            "query_id": query_id,
            "record_count": len(records),
            "total_value": total_value,
            "sample_record": records[0] if records else None,
        }

    def _fetch_trips(self, query_id: str, limit: int) -> list[dict]:
        """Mock trip data fetch."""
        base_trips = [
            {"trip_id": f"trip-{i:03d}", "distance_km": 20.5 + i, "value": 100 + (i * 10)}
            for i in range(1, limit + 1)
        ]
        return base_trips

    def _fetch_users(self, query_id: str, limit: int) -> list[dict]:
        """Mock user data fetch."""
        base_users = [
            {"user_id": f"user-{i:03d}", "score": 85 - (i % 20), "value": 50 + (i * 5)}
            for i in range(1, limit + 1)
        ]
        return base_users


def main() -> None:
    agent = DataFetchAgent()

    # Fetch trips
    trips_query = {
        "source": "trips",
        "query_id": "q-trips-001",
        "limit": 5,
    }

    result = agent.run(trips_query)
    print("\nTrips Fetch Result:")
    print(result)

    # Fetch users
    users_query = {
        "source": "users",
        "query_id": "q-users-001",
        "limit": 3,
    }

    result = agent.run(users_query)
    print("\nUsers Fetch Result:")
    print(result)


if __name__ == "__main__":
    main()
