"""Type definitions for the agent system."""
from dataclasses import dataclass
from typing import Any, Dict, List
from enum import Enum


class Intent(str, Enum):
    """Intent classifications."""
    GREETING = "greeting"
    QUERY = "query"
    HIGH_INTENT_LEAD = "high_intent_lead"
    UNCLEAR = "unclear"


@dataclass
class Message:
    """Represents a message in the conversation."""
    role: str  # "user" or "assistant"
    content: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AgentState:
    """Current state of the agent."""
    messages: List[Message]
    current_intent: Intent = Intent.UNCLEAR
    context: Dict[str, Any] = None
    rag_context: str = ""
    tool_calls: List[Dict[str, Any]] = None
    in_lead_capture: bool = False
    lead_name: str = None
    lead_email: str = None
    lead_platform: str = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.tool_calls is None:
            self.tool_calls = []
