# Project Structure Overview

```
new_project/
├── 📄 README.md                  # Project overview (START HERE)
├── 📄 ARCHITECTURE.md            # Detailed architecture & design decisions
├── 📄 IMPLEMENTATION_GUIDE.md     # Step-by-step implementation guide
├── 📄 ARCHITECTURE.visual.txt     # Visual structure diagram
├── 📄 .env.example               # Environment variables template
├── 📄 .gitignore                 # Git ignore patterns
├── 📄 requirements.txt           # Python dependencies (pip install -r)
├── 📄 pytest.ini                 # pytest configuration
├── 📄 main.py                    # ⭐ ENTRY POINT - Run this!
├── 📄 project_info.py            # Project structure checker & reference
│
├── 📁 src/                       # Main source code package
│   ├── 📄 __init__.py
│   │
│   ├── 📁 config/                # ⚙️ Configuration Management
│   │   ├── 📄 __init__.py
│   │   └── 📄 settings.py        # Pydantic settings from .env
│   │                             # Loads: API_KEY, model, temperature, etc.
│   │
│   ├── 📁 core/                  # 🧱 Base Classes & Types
│   │   ├── 📄 __init__.py
│   │   ├── 📄 base_agent.py      # Abstract BaseAgent class
│   │   └── 📄 types.py           # Intent, Message, AgentState enums/dataclasses
│   │                             # ⚡ Type-safe, immutable data structures
│   │
│   ├── 📁 intent/                # 🎯 Intent Detection
│   │   ├── 📄 __init__.py
│   │   └── 📄 detector.py        # IntentDetector class
│   │                             # Classifies: greeting, query, high_intent_lead
│   │
│   ├── 📁 memory/                # 💾 Conversation Memory
│   │   ├── 📄 __init__.py
│   │   └── 📄 conversation_memory.py  # ConversationMemory class
│   │                             # Maintains history, enforces size limits
│   │
│   ├── 📁 rag/                   # 📚 RAG & Knowledge Base Retrieval
│   │   ├── 📄 __init__.py
│   │   └── 📄 retriever.py       # KnowledgeBaseRetriever class
│   │                             # Loads JSON & Markdown, keyword-based search
│   │
│   ├── 📁 tools/                 # 🔧 External Tools & Integrations
│   │   ├── 📄 __init__.py
│   │   └── 📄 lead_capture.py    # LeadCaptureTool class
│   │                             # Captures leads → leads.jsonl
│   │
│   └── 📁 agent/                 # 🤖 Main Agent Orchestration
│       ├── 📄 __init__.py
│       └── 📄 conversational_agent.py  # ConversationalAgent class
│                                # Orchestrates all modules, main entrypoint
│
├── 📁 knowledge_base/            # 📖 RAG Knowledge Base
│   ├── 📄 sample_faq.json        # Example FAQ in JSON format
│   └── 📄 about_company.md       # Example company info in Markdown
│                                # ADD YOUR DOCUMENTS HERE!
│
├── 📁 tests/                     # 🧪 Unit & Integration Tests
│   ├── 📄 __init__.py
│   ├── 📄 test_intent_detector.py   # Intent detection tests
│   ├── 📄 test_memory.py            # Memory management tests
│   └── 📄 test_lead_capture.py      # Lead capture tests
│                                # Run: pytest tests/ -v
│
└── 📁 logs/                      # 📝 Application Logs (generated)
    └── (logs generated at runtime)

```

---

## Quick Navigation

### 📍 Where to Start?
1. **Overview**: [README.md](README.md)
2. **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) 
3. **How-To Guide**: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
4. **Run It**: Execute `python main.py`

### 🔍 Module at a Glance

| Module | File | Purpose | Key Class |
|--------|------|---------|-----------|
| **Config** | `src/config/settings.py` | Load settings from .env | `Settings` |
| **Core** | `src/core/types.py` | Data types & base classes | `Intent`, `Message`, `AgentState`, `BaseAgent` |
| **Intent** | `src/intent/detector.py` | Classify user intent | `IntentDetector` |
| **Memory** | `src/memory/conversation_memory.py` | Manage conversation history | `ConversationMemory` |
| **RAG** | `src/rag/retriever.py` | Retrieve from knowledge base | `KnowledgeBaseRetriever` |
| **Tools** | `src/tools/lead_capture.py` | Capture leads, external actions | `LeadCaptureTool` |
| **Agent** | `src/agent/conversational_agent.py` | Main orchestrator | `ConversationalAgent` |

---

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    CONVERSATIONAL AI AGENT                   │
└──────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌─────────────────┐   ┌──────────────┐
            │   main.py       │   │  TESTS       │
            │ Entry Point     │   │  pytest      │
            └─────────────────┘   └──────────────┘


             ┌─────────────────────────────────────┐
             │   ConversationalAgent (Main Brain)   │
             │        src/agent/                    │
             └──────────┬──────────────────────────┘
                        │
        ┌───────┬───────┼───────┬────────┬──────┐
        │       │       │       │        │      │
        ▼       ▼       ▼       ▼        ▼      ▼
    ┌─────┐┌──────┐┌──────┐┌────────┐┌──────┐┌────────┐
    │Conf-│Intent │Memory │  RAG   │ Tools │ Config │
    │ig   │Detec- │Manager│Retrieve│ Lead  │ Loader │
    │ig   │tor    │       │        │Capture│        │
    └─────┘└──────┘└──────┘└────────┘└──────┘└────────┘

        .env → Settings
               ↓
        [API_KEY, Model, Limits, etc.]

        knowledge_base/*.json/*.md → Retrieve
               ↓
        [Relevant Context]

        Conversation History → Memory
               ↓
        [Formatted Dialog]
```

---

## Setup Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Add `OPENAI_API_KEY` to `.env`
- [ ] Run `pip install -r requirements.txt`
- [ ] Add documents to `knowledge_base/`
- [ ] Run `python main.py` and test
- [ ] Run `pytest tests/` to verify tests pass
- [ ] (Optional) Customize prompts and intents

---

## What Each File Does

### Configuration
- **`.env.example`** - Template for environment variables (copy to `.env`)
- **`src/config/settings.py`** - Loads and validates settings using Pydantic

### Core Framework
- **`src/core/types.py`** - Type definitions (Intent enum, Message dataclass, etc.)
- **`src/core/base_agent.py`** - Abstract base agent class

### Intent Detection
- **`src/intent/detector.py`** - Uses LLM to classify user intent

### Conversation Memory
- **`src/memory/conversation_memory.py`** - Maintains conversation history with size limits

### Retrieval-Augmented Generation
- **`src/rag/retriever.py`** - Loads and retrieves from knowledge base (JSON/Markdown)

### Tools & Integrations
- **`src/tools/lead_capture.py`** - Captures lead information to JSONL

### Main Agent
- **`src/agent/conversational_agent.py`** - Orchestrates all components

### Testing
- **`tests/test_*.py`** - Unit tests for each module
- **`pytest.ini`** - pytest configuration

### Documentation
- **`README.md`** - Quick project overview
- **`ARCHITECTURE.md`** - Detailed architecture guide
- **`IMPLEMENTATION_GUIDE.md`** - Step-by-step implementation
- **`project_info.py`** - Project structure checker script

### Entry Points
- **`main.py`** - Interactive CLI agent (run this!)
- **`project_info.py`** - Verify structure and show docs

---

## Feature Summary

✅ **Intent Detection** - Classify user input into categories  
✅ **RAG System** - Retrieve from local knowledge base (JSON/Markdown)  
✅ **Tool Calling** - Lead capture with timestamps  
✅ **Conversation Memory** - Maintains context with configurable limits  
✅ **Async Processing** - Non-blocking LLM calls  
✅ **Modular Design** - Each component is testable and replaceable  
✅ **Configuration Management** - Easy .env setup  
✅ **Type Safety** - Pydantic, Enums, Dataclasses  
✅ **Unit Tests** - Included for each module  
✅ **Documentation** - Comprehensive guides  

---

## Production Checklist

- [ ] Replace keyword search with embeddings/vector DB
- [ ] Add database for leads (SQLite, PostgreSQL)
- [ ] Implement conversation summarization
- [ ] Add authentication/multi-user support
- [ ] Create REST API wrapper
- [ ] Add monitoring & logging
- [ ] Implement error handling & retry logic
- [ ] Load test and optimize
- [ ] Deploy to cloud (Docker recommended)
- [ ] Set up CI/CD pipeline

---

## Directory Independence Map

```
Module Dependencies:

agent/
├── depends on: config, core, intent, memory, rag, tools
├── depends on: langchain_openai
└── is a concrete implementation of: core.BaseAgent

intent/
├── depends on: config, core
├── depends on: langchain_openai
└── returns: core.Intent

memory/
├── depends on: config, core
├── depends on: (none)
└── manages: core.Message

rag/
├── depends on: config, core
├── depends on: (none)
└── reads from: knowledge_base/

tools/
├── depends on: (none)
├── depends on: (none)
└── writes to: leads.jsonl

core/
├── depends on: (none)
├── depends on: pydantic
└── provides: base types for all modules

config/
├── depends on: (none)
├── depends on: pydantic
└── provides: settings for all modules
```

---

## 🎯 Next Steps

1. **Read** the documentation files in order:
   - README.md
   - ARCHITECTURE.md
   - IMPLEMENTATION_GUIDE.md

2. **Setup** your environment:
   - Copy .env.example → .env
   - Add your OpenAI API key
   - Run: pip install -r requirements.txt

3. **Run** the agent:
   - python main.py
   - Test with various intents

4. **Test** the code:
   - pytest tests/ -v

5. **Extend** for your use case:
   - Add documents to knowledge_base/
   - Customize intent types
   - Add new tools

---

**Happy Coding! 🚀**
