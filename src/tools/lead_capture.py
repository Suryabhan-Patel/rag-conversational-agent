"""Lead capture tool for collecting customer information."""
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Lead:
    """Lead information."""
    name: str
    email: str
    platform: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    intent: Optional[str] = None
    captured_at: str = None
    
    def __post_init__(self):
        if self.captured_at is None:
            self.captured_at = datetime.now().isoformat()


class LeadCaptureTool:
    """Tool for capturing and storing lead information."""
    
    def __init__(self, storage_path: Path = Path("./leads.jsonl")):
        """Initialize lead capture tool.
        
        Args:
            storage_path: Path to store leads
        """
        self.storage_path = storage_path
    
    def capture_lead(self, name: str, email: str, platform: str = None,
                    phone: str = None, company: str = None, intent: str = None) -> Lead:
        """Capture and store a lead.
        
        Args:
            name: Lead's name
            email: Lead's email
            platform: Lead's platform (YouTube, Instagram, etc.)
            phone: Lead's phone number
            company: Lead's company
            intent: Detected intent
            
        Returns:
            Captured lead object
        """
        lead = Lead(name=name, email=email, platform=platform, phone=phone, company=company, intent=intent)
        self._save_lead(lead)
        return lead
    
    def _save_lead(self, lead: Lead) -> None:
        """Save lead to storage.
        
        Args:
            lead: Lead to save
        """
        try:
            with open(self.storage_path, "a") as f:
                f.write(json.dumps(asdict(lead)) + "\n")
        except Exception as e:
            print(f"Error saving lead: {e}")
    
    def get_leads(self) -> list:
        """Get all captured leads.
        
        Returns:
            List of leads
        """
        leads = []
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r") as f:
                    for line in f:
                        if line.strip():
                            leads.append(json.loads(line))
            except Exception as e:
                print(f"Error reading leads: {e}")
        return leads


def mock_lead_capture(name: str, email: str, platform: str) -> dict:
    """Mock function for capturing lead details.
    
    This function simulates the lead capture process.
    In production, this would call an actual API or CRM.
    
    Args:
        name: Lead's name
        email: Lead's email
        platform: Lead's platform (YouTube, Instagram, TikTok, etc.)
        
    Returns:
        Dictionary with success status and message
    """
    return {
        "status": "success",
        "message": f"Lead '{name}' ({email}) on {platform} has been recorded.",
        "lead": {
            "name": name,
            "email": email,
            "platform": platform,
            "captured_at": datetime.now().isoformat()
        }
    }
