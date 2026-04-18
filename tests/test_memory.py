"""Tests for conversation memory module."""
import pytest
from src.core.types import Message
from src.memory import ConversationMemory
from src.config import Settings


@pytest.fixture
def settings():
    """Fixture for settings."""
    settings = Settings()
    settings.max_conversation_memory = 3
    return settings


@pytest.fixture
def memory(settings):
    """Fixture for conversation memory."""
    return ConversationMemory(settings)


def test_add_message(memory):
    """Test adding a message."""
    msg = Message(role="user", content="Hello")
    memory.add_message(msg)
    assert len(memory.get_messages()) == 1


def test_memory_limit_enforcement(memory):
    """Test that memory limit is enforced."""
    for i in range(5):
        msg = Message(role="user", content=f"Message {i}")
        memory.add_message(msg)
    
    assert len(memory.get_messages()) <= memory.max_memory


def test_get_context_string(memory):
    """Test getting formatted context string."""
    memory.add_message(Message(role="user", content="Hi"))
    memory.add_message(Message(role="assistant", content="Hello"))
    
    context = memory.get_context_string()
    assert "USER:" in context
    assert "ASSISTANT:" in context


def test_clear_memory(memory):
    """Test clearing memory."""
    memory.add_message(Message(role="user", content="Test"))
    memory.clear()
    assert len(memory.get_messages()) == 0
