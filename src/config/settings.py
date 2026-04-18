"""Application configuration and settings management."""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    google_api_key: str
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.7
    
    # RAG Configuration
    knowledge_base_path: Path = Path("./knowledge_base")
    vector_store_path: Path = Path("./vector_store")
    retrieval_top_k: int = 3
    
    # Agent Configuration
    max_conversation_memory: int = 10
    memory_type: str = "conversation_buffer"
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # Tool Configuration
    enable_lead_capture: bool = True
    enable_external_tools: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
