from typing import Literal, Optional, Dict
from pydantic import BaseModel

class EmailInput(BaseModel):
    subject: str
    body: str
    from_email: str

class Classification(BaseModel):
    urgency: Literal["Low", "Medium", "High"]
    topic: Literal["Account", "Billing", "Bug", "Feature Request", "Technical Issue"]

class FollowUp(BaseModel):
    needed: bool
    reason: Optional[str] = None
    timeframe_hours: Optional[int] = None

class AgentDecision(BaseModel):
    action: Literal["auto_reply", "escalate"]
    rationale: Optional[str]=None

class WorkflowOutput(BaseModel):
    classification: Classification
    response_draft: str
    decision: str
    follow_up: str