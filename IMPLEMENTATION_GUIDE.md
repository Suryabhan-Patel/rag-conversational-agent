# Conversational AI Agent - Implementation Guide

## Quick Start (5 minutes)

### 1. Setup
```bash
cd new_project
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure
Edit `.env` with your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run
```bash
python main.py
```

---

## Project Structure At a Glance

```
new_project/
├── src/
│   ├── agent/                   ← Main orchestrator
│   ├── config/                  ← Settings & config
│   ├── core/                    ← Base classes & types
│   ├── intent/                  ← Intent detection
│   ├── memory/                  ← Conversation history
│   ├── rag/                     ← Document retrieval
│   └── tools/                   ← Lead capture, etc.
├── knowledge_base/              ← Your documents (JSON/MD)
├── tests/                       ← Unit tests
├── main.py                      ← Entry point
└── requirements.txt             ← Dependencies
```

---

## Module Breakdown

### **Agent** (`src/agent/`) - The Brain
**What it does:**
- Orchestrates all other components
- Processes user input → detects intent → retrieves context → generates response

**Key file:** `conversational_agent.py`

**Flow:**
```
User Input
  → Intent Detection (what does user want?)
  → RAG Retrieval (what knowledge is relevant?)
  → Memory Check (what's the conversation history?)
  → LLM Call (generate response)
  → Store in Memory
  → Return Response
```

---

### **Intent** (`src/intent/`) - The Classifier
**What it does:**
- Classifies each user message into categories:
  - `greeting` - "Hi", "Hello"
  - `query` - Questions about info
  - `high_intent_lead` - "I want to buy..."
  - `unclear` - Can't determine

**Key file:** `detector.py`

**Usage:**
```python
detector = IntentDetector(settings)
intent = await detector.detect("Hello!")  # Returns Intent.GREETING
```

---

### **Memory** (`src/memory/`) - The Historian
**What it does:**
- Keeps track of conversation history
- Limits memory size (configurable)
- Provides formatted context for prompts

**Key file:** `conversation_memory.py`

**Example:**
```python
memory = ConversationMemory(settings)
memory.add_message(Message(role="user", content="Hi"))
memory.add_message(Message(role="assistant", content="Hello!"))
context = memory.get_context_string()
# OUTPUT:
# USER: Hi
# ASSISTANT: Hello!
```

---

### **RAG** (`src/rag/`) - The Knowledge Base
**What it does:**
- Loads documents from `knowledge_base/` folder
- Retrieves relevant info for user queries
- Supports JSON and Markdown files

**Key file:** `retriever.py`

**Example:**
```python
retriever = KnowledgeBaseRetriever(settings)
context = retriever.retrieve("What is your pricing?")
# Returns relevant docs from knowledge_base/
```

**Add your own documents:**
```
knowledge_base/
├── sample_faq.json       # Your FAQs
├── about_company.md      # Company info
├── products.json         # Product catalog
└── pricing.md            # Pricing info
```

---

### **Tools** (`src/tools/`) - The Actions
**What it does:**
- Executes actions like capturing leads
- Integrates external services
- Extensible for custom tools

**Key file:** `lead_capture.py`

**Example:**
```python
lead_tool = LeadCaptureTool()
lead = lead_tool.capture_lead(
    name="John Doe",
    email="john@example.com",
    phone="555-1234",
    company="Acme Corp"
)
# Saved to leads.jsonl with timestamp
```

---

### **Config** (`src/config/`) - The Settings
**What it does:**
- Loads configuration from `.env` file
- Provides settings to all modules
- Type-safe with Pydantic

**Key file:** `settings.py`

**Example:**
```python
settings = Settings()
print(settings.openai_api_key)     # From .env
print(settings.max_conversation_memory)  # Default: 10
```

---

### **Core** (`src/core/`) - The Foundation
**What it does:**
- Defines base classes and data types
- Ensures consistency across modules

**Key files:**
- `types.py` - Intent, Message, AgentState enums/dataclasses
- `base_agent.py` - Abstract agent interface

---

## Data Flow Diagram

```
┌─────────────┐
│  User Input │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Config/Settings  │ Loads API keys, model name, limits
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Intent Detector  │ Classifies: greeting/query/lead
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Memory Manager   │ Retrieves conversation history
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ RAG Retriever    │ Gets relevant docs from knowledge_base/
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Build Prompt    │ Combines context + history
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  LLM Call        │ OpenAI API
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Store Response   │ Add to memory
└──────────────────┘
       │
       ▼
┌────────────────┐
│ Return to User │
└────────────────┘
```

---

## Configuration Guide

### **`.env` File - All Available Settings**

```bash
# LLM Configuration
OPENAI_API_KEY=sk-...                    # Your API key (REQUIRED)
MODEL_NAME=gpt-4-turbo-preview           # Which model to use
TEMPERATURE=0.7                          # Response creativity (0-1)

# RAG Configuration
KNOWLEDGE_BASE_PATH=./knowledge_base     # Where your docs are
VECTOR_STORE_PATH=./vector_store         # For future vector DB
RETRIEVAL_TOP_K=3                        # How many docs to retrieve

# Agent Configuration
MAX_CONVERSATION_MEMORY=10               # Max messages to keep
MEMORY_TYPE=conversation_buffer          # buffer or summary
ENABLE_LOGGING=true                      # Log everything
LOG_LEVEL=INFO                           # DEBUG/INFO/WARNING/ERROR

# Tool Configuration
ENABLE_LEAD_CAPTURE=true                 # Enable lead capture
ENABLE_EXTERNAL_TOOLS=false              # For future extensions
```

---

## Usage Examples

### **Example 1: Run Interactive Agent**
```bash
python main.py

You: Hello!
Assistant: Hi! How can I help you today?
[Intent: greeting]

You: What services do you offer?
Assistant: We offer consulting, software development...
[Intent: query]

You: I'm interested in your AI solutions
Assistant: Great! I'd love to help...
[Intent: high_intent_lead]

You: exit
Goodbye!
```

### **Example 2: Programmatic Usage**
```python
import asyncio
from src.config import Settings
from src.agent import ConversationalAgent
from src.core.types import AgentState

async def main():
    settings = Settings()
    agent = ConversationalAgent(settings)
    
    state = AgentState(messages=[], context={})
    
    # Single turn
    state = await agent.process("What's your pricing?", state)
    print(state.messages[-1].content)  # Print response
    
    # Multi-turn (conversation continues)
    state = await agent.process("Can you give me a discount?", state)
    print(state.messages[-1].content)  # Print response

asyncio.run(main())
```

### **Example 3: Add Custom Knowledge**
```bash
# Create knowledge_base/products.json
[
  {
    "name": "Product A",
    "price": "$99",
    "description": "Best-in-class AI solution"
  },
  {
    "name": "Product B",
    "price": "$199",
    "description": "Enterprise edition"
  }
]

# Or create knowledge_base/docs.md
# Product Documentation

## Getting Started
1. Install the SDK
2. Configure API keys
3. Start building

## Pricing
- Starter: $99/month
- Professional: $199/month
```

---

## Testing

### **Run Tests**
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_intent_detector.py

# Run with coverage
pytest --cov=src tests/

# Verbose output
pytest tests/ -v
```

### **Add New Tests**
```python
# tests/test_my_feature.py
import pytest
from src.my_module import MyClass

def test_my_feature():
    obj = MyClass()
    result = obj.do_something()
    assert result == "expected"

@pytest.mark.asyncio
async def test_async_feature():
    obj = MyClass()
    result = await obj.async_method()
    assert result == "expected"
```

---

## Extending the System

### **Add New Intent Type**
```python
# 1. src/core/types.py
class Intent(str, Enum):
    COMPLAINT = "complaint"  # New type

# 2. src/intent/detector.py - update prompt
INTENT_PROMPT = """...options..., complaint: User complaints/issues, ..."""

# 3. src/agent/conversational_agent.py - handle it
if state.current_intent == Intent.COMPLAINT:
    # Special handling for complaints
    prompt = "Respond empathetically to:"
```

### **Add New Tool**
```python
# 1. Create src/tools/my_tool.py
class MyTool:
    def execute(self, **kwargs):
        # Do something
        return result

# 2. src/agent/conversational_agent.py
from src.tools import MyTool

class ConversationalAgent:
    def __init__(self, settings):
        ...
        self.my_tool = MyTool()

# 3. Use in process()
if should_use_tool:
    result = self.my_tool.execute(param=value)
    state.tool_calls.append({...})
```

### **Upgrade to Vector Search**
```python
# src/rag/retriever.py
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class KnowledgeBaseRetriever:
    def __init__(self, settings):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key
        )
        self.vectorstore = FAISS.load_local(
            settings.vector_store_path,
            self.embeddings
        )
    
    def retrieve(self, query):
        return self.vectorstore.similarity_search(query, k=self.top_k)
```

---

## Deployment

### **Docker**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### **Environment Variables**
```bash
# Production settings
export OPENAI_API_KEY=sk-...
export MODEL_NAME=gpt-4-turbo-preview
export LOG_LEVEL=INFO
python main.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check `.env` has `OPENAI_API_KEY` |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Knowledge base empty" | Add `.json` or `.md` files to `knowledge_base/` |
| "Slow responses" | Reduce `RETRIEVAL_TOP_K` or use caching |
| "Memory growing" | Lower `MAX_CONVERSATION_MEMORY` |
| "Tests failing" | Run `pip install pytest pytest-asyncio` |

---

## Performance Tips

1. **Use Embeddings**: Replace keyword search with vector similarity
2. **Cache Results**: Store retrieved docs for repeated queries
3. **Batch Processing**: Process multiple user inputs in parallel
4. **Async All I/O**: Already implemented with `async/await`
5. **Limit Memory**: Lower `MAX_CONVERSATION_MEMORY` for long-running sessions

---

## Architecture Decisions & Why

| Decision | Why |
|----------|-----|
| Async/Await | LLM calls are I/O bound; non-blocking for better throughput |
| Dataclasses | Type-safe, immutable (after init), clear structure |
| Enums for Intent | Prevents invalid intent values, IDE autocomplete |
| Separate Modules | Each module is testable, replaceable independently |
| Pydantic Settings | Type validation, environment variable binding, docs |
| JSONL for Leads | Append-only, scalable, easy to process with streaming |

---

## What's Next?

- [ ] Add database for leads (SQLite, PostgreSQL)
- [ ] Implement vector embeddings for better retrieval
- [ ] Add multi-user session management
- [ ] Create REST API wrapper
- [ ] Add more tools (email, CRM integration)
- [ ] Implement conversation summarization
- [ ] Deploy to cloud (AWS, Azure, GCP)

---

**Happy Building! 🚀**
