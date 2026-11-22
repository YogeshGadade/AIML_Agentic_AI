# Agentic AI Engineering Portfolio

A hands-on engineering portfolio for building reliable, observable, and testable agentic AI systems.

This repository is being developed as a set of **independent reference implementations**. It is not a mirror of employer code or a collection of copied tutorials.

## Engineering principles

- **Bounded autonomy:** agents operate within explicit step, retry, and tool policies.
- **Deterministic controls:** authorization, validation, and approval decisions stay outside model-generated text.
- **Typed contracts:** workflow state and tool inputs/outputs have explicit schemas.
- **Provider independence:** model access is behind an adapter so orchestration can be tested without a live LLM.
- **Evaluation before claims:** examples should include reproducible tests and measurable evaluation before performance claims are made.
- **Secure by design:** tools are allow-listed; secrets and untrusted code are never executed by this starter runtime.

## Repository map

| Area | Purpose |
|---|---|
| `src/agentic_workflows/` | Minimal typed orchestration runtime and policy layer |
| `tests/` | Deterministic unit tests for workflow behavior |
| `docs/architecture.md` | Architecture, trust boundaries, and design decisions |
| `.github/workflows/ci.yml` | Lint and test automation |

## Current implementation: bounded tool workflow

The initial vertical slice demonstrates:
1. A typed task and workflow state.
2. An allow-listed tool registry.
3. A policy gate that can require human approval before a tool runs.
4. A bounded execution loop with a maximum step count.
5. Explicit tool errors and workflow outcomes.
6. A provider protocol that can later connect to an LLM without coupling orchestration to a vendor SDK.

The current example uses a deterministic planner for reproducibility. It does **not** call a hosted LLM, perform RAG, or claim production readiness.

## Quick start

Requires Python 3.11 or later.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Run the example:

```bash
python -m agentic_workflows
```

## Example behavior

The example plans a simple read-only knowledge lookup, validates the requested tool against the allow-list, executes it, and returns a structured result. A second example demonstrates that a side-effecting action is blocked unless an approval decision is supplied.

## Roadmap

- [x] Typed workflow contracts and bounded execution loop
- [x] Tool allow-list and approval policy
- [x] Deterministic tests and CI workflow
- [ ] LLM planner adapter with structured output validation
- [ ] Human approval API and durable checkpoint/resume
- [ ] Retrieval-augmented generation with retrieval evaluation
- [ ] Tracing, token/cost accounting, and offline agent evaluation
- [ ] Deployment example with authentication and operational controls

## Security and limitations

This is a local reference implementation, not a production agent platform. Tools in this starter are in-process Python callables and must be trusted code. Do not register arbitrary user-supplied code, expose the runtime as a public execution service, or place credentials in source control. Production deployments need authentication, authorization, isolated tool execution, secret management, durable state, audit logs, rate limits, and operational monitoring.

## License

No license has been selected yet. Until a license is added, normal copyright restrictions apply; do not assume the code is available for unrestricted reuse.
