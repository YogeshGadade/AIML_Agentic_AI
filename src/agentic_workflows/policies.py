"""Deterministic policy checks; never delegate authorization to the model."""

from dataclasses import dataclass

from agentic_workflows.models import ApprovalDecision


@dataclass(frozen=True)
class ToolPolicy:
    allowed_tools: frozenset[str]
    approval_required: frozenset[str] = frozenset()

    def validate_tool(self, tool_name: str) -> None:
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"Tool '{tool_name}' is not allow-listed")

    def authorize(
        self, tool_name: str, decision: ApprovalDecision
    ) -> ApprovalDecision:
        self.validate_tool(tool_name)
        if tool_name not in self.approval_required:
            return ApprovalDecision.APPROVED
        return decision
