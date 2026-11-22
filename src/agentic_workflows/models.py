"""Typed contracts shared by the workflow runtime."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ApprovalDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


class TaskRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    task_id: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    tool_name: str = Field(min_length=1)
    tool_input: dict[str, Any] = Field(default_factory=dict)


class WorkflowState(BaseModel):
    task: TaskRequest
    step_count: int = 0
    status: str = "pending"
    output: Any | None = None
    error: str | None = None
    approval: ApprovalDecision = ApprovalDecision.PENDING


class WorkflowResult(BaseModel):
    task_id: str
    status: str
    output: Any | None = None
    error: str | None = None
    steps: int
    approval: ApprovalDecision
