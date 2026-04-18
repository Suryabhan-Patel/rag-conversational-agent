"""Tests for lead capture module."""
import pytest
import json
from pathlib import Path
from src.tools import LeadCaptureTool


@pytest.fixture
def temp_lead_path(tmp_path):
    """Fixture for temporary lead storage path."""
    return tmp_path / "test_leads.jsonl"


@pytest.fixture
def lead_capture(temp_lead_path):
    """Fixture for lead capture tool."""
    return LeadCaptureTool(temp_lead_path)


def test_capture_lead(lead_capture):
    """Test capturing a lead."""
    lead = lead_capture.capture_lead(
        name="John Doe",
        email="john@example.com",
        phone="555-1234",
        company="Acme Corp"
    )
    
    assert lead.name == "John Doe"
    assert lead.email == "john@example.com"
    assert lead.captured_at is not None


def test_save_and_retrieve_leads(lead_capture):
    """Test saving and retrieving leads."""
    lead_capture.capture_lead("Alice", "alice@example.com")
    lead_capture.capture_lead("Bob", "bob@example.com")
    
    leads = lead_capture.get_leads()
    assert len(leads) == 2
    assert leads[0]["name"] == "Alice"
    assert leads[1]["name"] == "Bob"
