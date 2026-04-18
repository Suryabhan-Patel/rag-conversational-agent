"""Base agent class defining the interface."""
from abc import ABC, abstractmethod
from .types import AgentState, Message


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    @abstractmethod
    async def process(self, user_input: str, state: AgentState) -> AgentState:
        """Process user input and update agent state.
        
        Args:
            user_input: The user's message
            state: Current agent state
            
        Returns:
            Updated agent state with response
        """
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset the agent to initial state."""
        pass
