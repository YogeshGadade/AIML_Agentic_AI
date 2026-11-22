"""Bounded execution runtime with deterministic policy enforcement."""

from agentic_workflows.models import (
    ApprovalDecision,
    TaskRequest,
    WorkflowResult,
    WorkflowState,
)
from agentic_workflows.policies import ToolPolicy
from agentic_workflows.tools import ToolRegistry


class AgentRuntime:
    def __init__(
        self,
        registry: ToolRegistry,
        policy: ToolPolicy,
        max_steps: int = 5,
    ) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")
        self.registry = registry
        self.policy = policy
        self.max_steps = max_steps

    def run(
        self,
        task: TaskRequest,
        approval: ApprovalDecision = ApprovalDecision.PENDING,
    ) -> WorkflowResult:
        state = WorkflowState(task=task, approval=approval)

        try:
            self.policy.validate_tool(task.tool_name)
            decision = self.policy.authorize(task.tool_name, approval)
            state.approval = decision

            if decision == ApprovalDecision.PENDING:
                state.status = "awaiting_approval"
                return self._result(state)
            if decision == ApprovalDecision.REJECTED:
                state.status = "rejected"
                state.error = "Required approval was rejected"
                return self._result(state)

            while state.step_count < self.max_steps:
                state.step_count += 1
                tool = self.registry.get(task.tool_name)
                state.output = tool.handler(task.tool_input)
                state.status = "completed"
                return self._result(state)

            state.status = "limit_reached"
            state.error = "Maximum workflow step count reached"
        except (PermissionError, LookupError, ValueError) as exc:
            state.status = "failed"
            state.error = str(exc)
        except Exception as exc:  # Keep tool failures inside the workflow boundary.
            state.status = "failed"
            state.error = f"Tool execution failed: {type(exc).__name__}"

        return self._result(state)

    @staticmethod
    def _result(state: WorkflowState) -> WorkflowResult:
        return WorkflowResult(
            task_id=state.task.task_id,
            status=state.status,
            output=state.output,
            error=state.error,
            steps=state.step_count,
            approval=state.approval,
        )
