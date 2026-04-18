"""Tests for intent detection module."""
import pytest
from src.core.types import Intent
from src.intent import IntentDetector
from src.config import Settings


@pytest.fixture
def settings():
    """Fixture for settings."""
    return Settings()


@pytest.fixture
def detector(settings):
    """Fixture for intent detector."""
    return IntentDetector(settings)


@pytest.mark.asyncio
async def test_detect_greeting(detector):
    """Test greeting intent detection."""
    result = await detector.detect("Hello there!")
    assert result in (Intent.GREETING, Intent.UNCLEAR)


@pytest.mark.asyncio
async def test_detect_query(detector):
    """Test query intent detection."""
    result = await detector.detect("What is machine learning?")
    assert result in (Intent.QUERY, Intent.UNCLEAR)


@pytest.mark.asyncio
async def test_detect_high_intent_lead(detector):
    """Test high intent lead detection."""
    result = await detector.detect("I'm interested in buying your product")
    assert result in (Intent.HIGH_INTENT_LEAD, Intent.UNCLEAR)
