"""Model-provider boundary.

A production adapter should validate structured model output and treat all model
content as untrusted input. Authorization remains in the deterministic policy layer.
"""

from typing import Protocol

from agentic_workflows.models import TaskRequest


class Planner(Protocol):
    def choose_tool(self, task: TaskRequest) -> str:
        """Return a proposed tool name; this is a proposal, not authorization."""
