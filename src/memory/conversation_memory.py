"""Conversation memory management for maintaining context."""
from typing import List
from src.core.types import Message
from src.config import Settings


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, settings: Settings):
        """Initialize conversation memory.
        
        Args:
            settings: Application settings
        """
        self.messages: List[Message] = []
        self.max_memory = settings.max_conversation_memory
        self.memory_type = settings.memory_type
    
    def add_message(self, message: Message) -> None:
        """Add a message to memory.
        
        Args:
            message: Message to add
        """
        self.messages.append(message)
        self._enforce_memory_limit()
    
    def get_messages(self) -> List[Message]:
        """Get all messages in memory.
        
        Returns:
            List of messages
        """
        return self.messages.copy()
    
    def get_context_string(self) -> str:
        """Get formatted conversation context.
        
        Returns:
            Formatted conversation history
        """
        context = []
        for msg in self.messages:
            context.append(f"{msg.role.upper()}: {msg.content}")
        return "\n".join(context)
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages = []
    
    def _enforce_memory_limit(self) -> None:
        """Enforce maximum memory size by removing oldest messages."""
        if len(self.messages) > self.max_memory:
            # Keep system message if exists, remove oldest user/assistant messages
            self.messages = self.messages[-self.max_memory:]
