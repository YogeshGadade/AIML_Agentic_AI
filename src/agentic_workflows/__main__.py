"""Run the deterministic example workflow."""

from agentic_workflows.models import ApprovalDecision, TaskRequest
from agentic_workflows.policies import ToolPolicy
from agentic_workflows.runtime import AgentRuntime
from agentic_workflows.tools import Tool, ToolRegistry


def main() -> None:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="lookup_note",
            description="Look up a note in a fixed local example dictionary",
            handler=lambda payload: {"note": f"Example note for {payload['topic']}"},
        )
    )
    policy = ToolPolicy(allowed_tools=registry.names())
    runtime = AgentRuntime(registry=registry, policy=policy)

    request = TaskRequest(
        task_id="demo-001",
        objective="Find the note about agent reliability",
        tool_name="lookup_note",
        tool_input={"topic": "agent reliability"},
    )
    print(runtime.run(request, approval=ApprovalDecision.APPROVED).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
