# Skeleton-First Common Module Implementation Plan

Build a minimal, runnable common module that can initialize and execute one concrete agent end-to-end with no external infrastructure first, then add one capability per phase (security, infra, validation, observability, orchestration, and evaluation). This de-risks architecture early and keeps each step testable.

## Implementation Phases

### Phase 1 — Bare package and BaseAgent core

1. Create package skeleton: `common/`, `common/agent/`, `agents/`, `tests/`
2. Add minimal `BaseAgent` with only: manifest fields, `run()` method, and two hooks (`pre_process`, `post_process`)
3. Add concrete `MinimalAgent` under `agents/` that returns deterministic output (no LLM)
4. Add execution entry point to instantiate and run MinimalAgent with sample payload
5. Add unit tests for lifecycle order and malformed input handling

**Verification:** Unit tests pass proving MinimalAgent executes deterministically with no external services

---

### Phase 2 — Minimal LLM wiring

6. Add `llm_client` wrapper interface with fake/mock provider by default
7. Add model tier config lookup from environment (one tier: `fast`)
8. Support fallback to deterministic stub when API key is missing

**Verification:** Tests pass for tier resolution and fallback path

---

### Phase 3 — Security slice 1 (capsule shape only)

9. Add `IntentCapsule` and `ScopedToken` data models with schema validation
10. Add optional capsule field to `BaseAgent` with schema validation
11. Allow local dev mode when capsule is absent

**Verification:** Schema validation tests pass for valid/invalid payloads

---

### Phase 4 — Infrastructure abstraction stubs

12. Add `context_store` interface with in-memory implementation (dict + event list)
13. Add `db_writer` interface with in-memory implementation and table permission guard
14. Wire `BaseAgent` to use abstractions instead of direct library imports

**Verification:** Tests prove no direct Redis/SQLAlchemy imports; table guard blocks unauthorized writes

---

### Phase 5 — Security slice 2 (real enforcement)

15. Add `intent_gate` verification pipeline (schema + HMAC + step_index + TTL)
16. Add strict enforcement mode flag to `BaseAgent`
17. On violation: emit forensic snapshot through `db_writer`

**Verification:** Tests pass for tampered HMAC, expired token, wrong step_index

---

### Phase 6 — Real infra adapters

18. Add Redis adapter for `context_store` (get/set/publish)
19. Add Postgres adapter for `db_writer` with migrations for `agent_audit_log` and `task_execution_logs`
20. Keep in-memory adapters for local tests

**Verification:** Integration tests pass against both in-memory and real adapters

---

### Phase 7 — Worker/task orchestration

21. Add `task_queue` abstraction with Celery adapter (Windows-safe with `--pool=solo`)
22. Register MinimalAgent task via manifest fields
23. Validate end-to-end: enqueue → execute → publish event

**Verification:** Integration test passes for one task roundtrip

---

### Phase 8 — Output validation and sanitization

24. Add `output_validator` with minimal Pydantic schema
25. Add `sanitise_input` and `sanitise_outgoing` with starter ruleset
26. Implement retry-on-invalid-output once, then fail cleanly

**Verification:** Tests pass for invalid output, sanitization, no-PII-leakage baseline

---

### Phase 9 — Observability and cost

27. Add structured logger and tracer timing around pipeline steps
28. Add cost_monitor hooks in `llm_client` (tokens/cost optional)
29. Emit required audit log fields for each locked step

**Verification:** Audit events include all required fields

---

### Phase 10 — Workflow and policy wiring

30. Add `workflow_registry` loader for one minimal YAML workflow
31. Add `skill_registry` startup consistency check
32. Wire orchestrator-compatible dispatch with step_index advancement

**Verification:** Workflow YAML parses; manifest mismatch fails fast

---

### Phase 11 — Evaluation harnesses and CI

33. Add DeepEval skeleton with one scoring test
34. Add Promptfoo skeleton with one regression test
35. Add CI baseline (pytest + lint + optional Trivy)
36. Expand MinimalAgent to ScoringAgent as first production-like reference

**Verification:** DeepEval and Promptfoo baseline tests pass; CI pipeline green

---

## Key Architectural Decisions

- **Skeleton-first:** Get a working agent immediately instead of waiting for full infrastructure
- **Adapter pattern:** Keep in-memory adapters available while Redis/Postgres/Celery are introduced
- **One concrete agent:** MinimalAgent is a permanent contract test harness
- **Local first:** Phases 1–4 run in pure local mode before Docker services
- **Vertical slicing:** Each capability is independently verifiable before moving to the next

---

## File Structure (as built)

```

common/
**init**.py
agent/
base_agent.py ← BaseAgent lifecycle
llm_client.py ← LLM interface + tier resolution
output_validator.py ← Pydantic validation
infra/
context_store.py ← In-memory, then Redis adapter
db_writer.py ← In-memory, then Postgres adapter
intent_gate.py ← Capsule verification (Phase 5+)
task_queue.py ← Celery abstraction (Phase 7+)
workflow_registry.py ← YAML loader (Phase 10+)

agents/
minimal_agent.py ← First concrete agent
scoring_agent.py ← First production-like agent (Phase 11)

tests/
test_base_agent.py ← Lifecycle and lifecycle order
test_llm_client.py
test_adapters.py ← In-memory and real backends
test_security.py ← HMAC, token, step_index
deepeval/ ← Evaluation tests (Phase 11)
promptfoo/ ← Regression tests (Phase 11)

```

---

## Recommended Pace

- **Phase 1–2:** 1–2 days (local runnable base)
- **Phase 3–4:** 1 day (interfaces and stubs)
- **Phase 5:** 1 day (security enforcement)
- **Phase 6–7:** 2 days (real adapters + queue)
- **Phase 8–9:** 1 day (validation + observability)
- **Phase 10–11:** 2 days (workflow + evaluation + ScoringAgent)

**Total:** ~1 week end-to-end for a complete, testable common module with one production-like agent reference.
