"""
Global Pydantic models for the PhantomBuster SDK.
"""

from pydantic import BaseModel, Field
from typing import List

class Branch(BaseModel):
    """Represents a single PhantomBuster branch."""
    id: int = Field(..., description="The unique identifier for the branch.")
    name: str = Field(..., description="The name of the branch.")
    scriptId: int = Field(..., description="The ID of the script this branch belongs to.")

class BranchListResponse(BaseModel):
    """Response model for a list of branches."""
    branches: List[Branch] = Field(..., description="A list of branches.")

class BranchDiff(BaseModel):
    """Represents the diff between staging and release for a script."""
    scriptId: int = Field(..., description="The ID of the script.")
    diff: int = Field(..., description="The length difference between staging and release branches.")

class BranchDiffResponse(BaseModel):
    """Response model for branch differences."""
    diffs: List[BranchDiff] = Field(..., description="A list of branch differences.")

class CreateBranchRequest(BaseModel):
    """Request model for creating a new branch."""
    scriptId: int = Field(..., description="The ID of the script to branch from.")
    name: str = Field(..., description="The name for the new branch.")

class DeleteBranchRequest(BaseModel):
    """Request model for deleting a branch."""
    branchId: int = Field(..., description="The ID of the branch to delete.")

class ReleaseBranchRequest(BaseModel):
    """Request model for releasing a branch."""
    branchId: int = Field(..., description="The ID of the branch to release.")

class SuccessResponse(BaseModel):
    """Generic success response model."""
    success: bool = Field(..., description="Indicates if the operation was successful.")
    message: str | None = Field(None, description="An optional success message.")

# TODO: Verify the full schema for the Script model from API documentation.
class Script(BaseModel):
    """Represents a PhantomBuster script."""

    id: str
    name: str
    version: int
    script: str  # The actual script code
    visibility: str  # e.g., 'private' or 'public'


class ScriptListResponse(BaseModel):
    """Represents a list of PhantomBuster scripts."""

    scripts: list[Script]


class UpdateScriptVisibilityRequest(BaseModel):
    """Request model for updating a script's visibility."""

    id: str
    visibility: str


class UpdateScriptAccessListRequest(BaseModel):
    """Request model for updating a script's access list."""

    id: str
    accessList: list[str]


class SaveScriptRequest(BaseModel):
    """Request model for saving (creating or updating) a script."""

    script: str
    id: str | None = None
    name: str | None = None


class DeleteScriptRequest(BaseModel):
    """Request model for deleting a script."""

    id: str


class OrgResources(BaseModel):
    """Represents the resources and usage for an organization."""

    id: int | None = None
    name: str | None = None
    plan: str | None = None
    execution_time: int | None = None
    slots: int | None = None
    storage_mb: int | None = None


class Container(BaseModel):
    """Represents a container."""

    id: int | None = None
    agent_id: int | None = None
    status: str | None = None


class ContainerListResponse(BaseModel):
    """Response model for a list of containers."""

    containers: list[Container]


class AgentGroup(BaseModel):
    """Represents an agent group."""

    id: int | None = None
    name: str | None = None
    agent_ids: list[int] | None = None


class AgentGroupListResponse(BaseModel):
    """Response model for a list of agent groups."""

    agent_groups: list[AgentGroup]


class Agent(BaseModel):
    """Represents an agent."""

    id: int | None = None
    name: str | None = None
    script_id: int | None = None
    org_id: int | None = None


class AgentListResponse(BaseModel):
    """Response model for a list of agents."""

    agents: list[Agent]


class LaunchAgentRequest(BaseModel):
    """Request model for launching an agent."""

    id: int


class SaveAgentRequest(BaseModel):
    """Request model for saving an agent."""

    id: int | None = None
    name: str
    script_id: int


class Lead(BaseModel):
    """Represents a lead in organization storage."""

    id: int
    data: dict[str, Any]


class LeadListResponse(BaseModel):
    """Response model for a list of leads."""

    leads: list[Lead]


class SaveLeadRequest(BaseModel):
    """Request model for saving a lead."""

    list_id: int
    data: dict[str, Any]
    id: int | None = None


class DeleteLeadsRequest(BaseModel):
    """Request model for deleting many leads."""

    lead_ids: list[int]


class DeleteListRequest(BaseModel):
    """Request model for deleting a list."""

    list_id: int


class Identity(BaseModel):
    """Represents an identity."""

    id: int
    name: str


class SaveIdentityRequest(BaseModel):
    """Request model for saving an identity with a token."""

    name: str
    token: str


class BrightDataSerpRequest(BaseModel):
    """Request model for a Bright Data SERP request."""


class LocationInfo(BaseModel):
    """Represents location information for an IP address."""


class HCaptchaRequest(BaseModel):
    """Request model for solving an hCaptcha."""

    sitekey: str
    pageurl: str


class RecaptchaRequest(BaseModel):
    """Request model for solving a reCAPTCHA."""

    sitekey: str
    pageurl: str


class CaptchaResponse(BaseModel):
    """Response model for a solved captcha."""


class AICompletionsRequest(BaseModel):
    """Request model for AI completions."""

    prompt: str
    max_tokens_to_sample: int
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    stop_sequences: list[str] | None = None


class AICompletionsResponse(BaseModel):
    """Response model for AI completions."""

    completion: str
    stop_reason: str
    stop: str | None = None


class User(BaseModel):
    """Represents a Phantombuster user."""

    id: int
    name: str
    email: str
    agents: list[Agent]


    token: str
    useragent: str
    error: str | None = None


    ip: str
    country: str
    city: str | None = None
    region: str | None = None


    q: str
    gl: str | None = None
    hl: str | None = None
    tbm: str | None = None
    start: int | None = None
    num: int | None = None
    uule: str | None = None
    brd_mobile: str | None = None
    brd_browser: str | None = None





