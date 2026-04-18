#!/usr/bin/env python3
"""Quick reference and module dependency checker."""

import sys
from pathlib import Path

def check_structure():
    """Verify project structure is complete."""
    project_root = Path(__file__).parent
    required_dirs = [
        "src", "src/agent", "src/core", "src/config", "src/intent",
        "src/memory", "src/rag", "src/tools", "knowledge_base", "tests", "logs"
    ]
    
    required_files = [
        "main.py", "requirements.txt", ".env.example", "README.md",
        "ARCHITECTURE.md", "IMPLEMENTATION_GUIDE.md"
    ]
    
    print("📋 Checking Project Structure...\n")
    
    # Check directories
    print("📁 Directories:")
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        status = "✓" if dir_path.exists() else "✗"
        print(f"  {status} {dir_name}/")
    
    print("\n📄 Files:")
    for file_name in required_files:
        file_path = project_root / file_name
        status = "✓" if file_path.exists() else "✗"
        print(f"  {status} {file_name}")
    
    print("\n" + "="*50)
    print("✓ Project Structure Verified!")
    print("="*50)

def show_modules():
    """Display module documentation."""
    modules = {
        "src.config": {
            "purpose": "Application configuration & settings",
            "key_class": "Settings",
            "usage": "settings = Settings()",
        },
        "src.core": {
            "purpose": "Base classes, types, enums",
            "key_class": "BaseAgent, Message, AgentState, Intent",
            "usage": "Inherited by other modules",
        },
        "src.intent": {
            "purpose": "Intent classification from user input",
            "key_class": "IntentDetector",
            "usage": "intent = await detector.detect(user_input)",
        },
        "src.memory": {
            "purpose": "Conversation history management",
            "key_class": "ConversationMemory",
            "usage": "memory.add_message(msg); context = memory.get_context_string()",
        },
        "src.rag": {
            "purpose": "Document retrieval from knowledge base",
            "key_class": "KnowledgeBaseRetriever",
            "usage": "context = retriever.retrieve(query)",
        },
        "src.tools": {
            "purpose": "Tool implementations (lead capture, etc)",
            "key_class": "LeadCaptureTool",
            "usage": "lead = lead_tool.capture_lead(...)",
        },
        "src.agent": {
            "purpose": "Main agent orchestration",
            "key_class": "ConversationalAgent",
            "usage": "agent = ConversationalAgent(settings); state = await agent.process(input)",
        },
    }
    
    print("\n📚 Module Reference:\n")
    for module, info in modules.items():
        print(f"📦 {module}")
        print(f"   Purpose:   {info['purpose']}")
        print(f"   Key Class: {info['key_class']}")
        print(f"   Example:   {info['usage']}")
        print()

def show_quick_start():
    """Display quick start guide."""
    print("\n🚀 Quick Start:\n")
    print("1. Copy .env.example to .env")
    print("   $ cp .env.example .env")
    print()
    print("2. Edit .env with your OpenAI API key")
    print("   OPENAI_API_KEY=sk-...")
    print()
    print("3. Install dependencies")
    print("   $ pip install -r requirements.txt")
    print()
    print("4. Run the agent")
    print("   $ python main.py")
    print()
    print("5. Test it")
    print("   $ pytest tests/ -v")
    print()

def show_file_summary():
    """Show what each file does."""
    files = {
        "main.py": "Entry point - run this to start interactive agent",
        "requirements.txt": "Python package dependencies",
        ".env.example": "Template for environment variables",
        "README.md": "Project overview",
        "ARCHITECTURE.md": "Detailed architecture documentation",
        "IMPLEMENTATION_GUIDE.md": "Step-by-step implementation guide",
        "pytest.ini": "pytest configuration",
        ".gitignore": "Git ignore patterns",
    }
    
    print("\n📋 File Descriptions:\n")
    for filename, description in files.items():
        print(f"  • {filename:25} - {description}")
    print()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 Conversational AI Agent Project")
    print("="*50)
    
    check_structure()
    show_modules()
    show_quick_start()
    show_file_summary()
    
    print("📖 For more details, see:")
    print("  • ARCHITECTURE.md - Deep dive into system design")
    print("  • IMPLEMENTATION_GUIDE.md - Step-by-step guide")
    print("  • README.md - Quick overview")
    print()
