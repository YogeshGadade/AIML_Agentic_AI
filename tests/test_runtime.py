from agentic_workflows.models import ApprovalDecision, TaskRequest
from agentic_workflows.policies import ToolPolicy
from agentic_workflows.runtime import AgentRuntime
from agentic_workflows.tools import Tool, ToolRegistry


def build_runtime(*, approval_required: bool = False) -> AgentRuntime:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="read_item",
            description="Return a fixed item",
            handler=lambda payload: {"item": payload["item"]},
        )
    )
    approval = frozenset({"read_item"}) if approval_required else frozenset()
    policy = ToolPolicy(allowed_tools=registry.names(), approval_required=approval)
    return AgentRuntime(registry, policy, max_steps=3)


def request(tool_name: str = "read_item") -> TaskRequest:
    return TaskRequest(
        task_id="test-1",
        objective="Read an item",
        tool_name=tool_name,
        tool_input={"item": "alpha"},
    )


def test_allowed_tool_executes_and_returns_structured_result() -> None:
    result = build_runtime().run(request())
    assert result.status == "completed"
    assert result.output == {"item": "alpha"}
    assert result.steps == 1


def test_unapproved_tool_waits_without_execution() -> None:
    result = build_runtime(approval_required=True).run(request())
    assert result.status == "awaiting_approval"
    assert result.steps == 0
    assert result.output is None


def test_rejected_approval_blocks_execution() -> None:
    result = build_runtime(approval_required=True).run(
        request(), approval=ApprovalDecision.REJECTED
    )
    assert result.status == "rejected"
    assert result.steps == 0


def test_approved_tool_executes() -> None:
    result = build_runtime(approval_required=True).run(
        request(), approval=ApprovalDecision.APPROVED
    )
    assert result.status == "completed"


def test_tool_not_on_allow_list_is_blocked() -> None:
    result = build_runtime().run(request("shell"))
    assert result.status == "failed"
    assert "not allow-listed" in (result.error or "")


def test_tool_exception_is_contained() -> None:
    registry = ToolRegistry()
    registry.register(
        Tool("explode", "Raises an exception", lambda _: (_ for _ in ()).throw(RuntimeError()))
    )
    runtime = AgentRuntime(registry, ToolPolicy(allowed_tools=registry.names()))
    result = runtime.run(
        TaskRequest(task_id="x", objective="test", tool_name="explode")
    )
    assert result.status == "failed"
    assert result.error == "Tool execution failed: RuntimeError"


def test_max_steps_must_be_positive() -> None:
    import pytest

    with pytest.raises(ValueError, match="max_steps"):
        AgentRuntime(ToolRegistry(), ToolPolicy(allowed_tools=frozenset()), max_steps=0)
