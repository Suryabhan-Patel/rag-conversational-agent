# Architecture & Code Organization Guide

## Project Overview

This is a **production-ready conversational AI agent** that combines:
- **Intent Classification**: Categorizes user messages into intents
- **RAG (Retrieval-Augmented Generation)**: Augments responses with local knowledge
- **Tool Calling**: Captures leads and integrates external services
- **Memory Management**: Maintains conversation context across turns
- **Async Processing**: Non-blocking, high-performance architecture

---

## 📁 Directory Structure & Explanations

### **Root Level**

```
new_project/
├── src/                      # Source code (main package)
├── knowledge_base/           # RAG knowledge base files
├── tests/                    # Unit and integration tests
├── logs/                     # Application logs (generated)
├── main.py                   # Entry point - Run this to start interactive agent
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Project overview
└── ARCHITECTURE.md           # This file
```

---

## 📦 Core Modules (`src/`)

### **1. `src/config/` - Configuration Management**

**Files:**
- `__init__.py` - Package exports
- `settings.py` - Pydantic BaseSettings for configuration

**Purpose:** Centralized configuration management using environment variables

**Key Class: `Settings`**
```python
# Loads from .env file:
- openai_api_key: API key for LLM
- model_name: Default "gpt-4-turbo-preview"
- temperature: Response creativity (0.7 default)
- knowledge_base_path: Path to RAG docs
- retrieval_top_k: How many docs to retrieve
- max_conversation_memory: Conversation history size limit
- enable_lead_capture: Toggle lead capture
```

**Why separate?** Keeps sensitive config away from code; easy environment switching.

---

### **2. `src/core/` - Base Classes & Type Definitions**

**Files:**
- `types.py` - Data models
- `base_agent.py` - Abstract base class
- `__init__.py` - Package exports

**Key Classes:**

**`Intent` (Enum)**
```python
GREETING = "greeting"           # "Hi", "Hello"
QUERY = "query"                 # Questions, info requests
HIGH_INTENT_LEAD = "high_intent_lead"  # "I want to buy..."
UNCLEAR = "unclear"             # Cannot determine
```

**`Message` (Dataclass)**
```python
role: str                        # "user" or "assistant"
content: str                     # The message text
metadata: Dict                   # Additional info
```

**`AgentState` (Dataclass)**
```python
messages: List[Message]          # Conversation history
current_intent: Intent           # Last detected intent
context: Dict                    # Contextual data
rag_context: str                 # Retrieved knowledge
tool_calls: List[Dict]           # Executed tool calls
```

**`BaseAgent` (ABC)**
```python
async process(user_input, state) -> state  # Core method
reset() -> None                            # Clear state
```

**Why separate?** Makes it easy to add new agent types by inheriting from BaseAgent.

---

### **3. `src/intent/` - Intent Detection**

**Files:**
- `detector.py` - Intent classification logic
- `__init__.py` - Package exports

**Key Class: `IntentDetector`**
```python
__init__(settings)               # Takes settings, initializes LLM
await detect(user_input)         # Async intent classification
```

**How it works:**
1. Takes user input
2. Sends to LLM with prompt template
3. Parses LLM response to Intent enum
4. Returns detected intent

**Why async?** LLM calls are I/O bound; async prevents blocking.

---

### **4. `src/memory/` - Conversation Memory**

**Files:**
- `conversation_memory.py` - Memory management
- `__init__.py` - Package exports

**Key Class: `ConversationMemory`**
```python
__init__(settings)               # Initialize with max size
add_message(message)             # Add to conversation
get_messages()                   # Retrieve all messages
get_context_string()             # Formatted chat history
clear()                          # Reset memory
```

**Features:**
- Automatic memory size enforcement (FIFO)
- Formatted context for prompt building
- Configurable memory strategy (buffer/summary)

**Why separate?** Can swap implementations (DB, Redis, etc.) without changing agent.

---

### **5. `src/rag/` - Retrieval-Augmented Generation**

**Files:**
- `retriever.py` - RAG implementation
- `__init__.py` - Package exports

**Key Class: `KnowledgeBaseRetriever`**
```python
__init__(settings)               # Load KB from files
retrieve(query: str) -> str      # Get relevant context
```

**Supports:**
- JSON files (auto-loaded)
- Markdown files (auto-loaded)
- Simple keyword-based retrieval (easily upgradeable to embeddings)

**How it works:**
1. Loads all `.json` and `.md` files from `knowledge_base/`
2. On query, scores documents by keyword overlap
3. Returns top-k most relevant documents

**Why separate?** Encapsulates all retrieval logic; easy to swap with vector DB later.

---

### **6. `src/tools/` - External Tools & Integrations**

**Files:**
- `lead_capture.py` - Lead capture implementation
- `__init__.py` - Package exports

**Key Class: `LeadCaptureTool`**
```python
capture_lead(name, email, phone, company, intent) -> Lead
get_leads() -> List[Lead]
```

**Features:**
- Captures lead info with timestamp
- Stores in JSONL format (append-only, scalable)
- Easy to extend with more tools

**Why separate?** Tool logic isolated; easy to add more tools later.

---

### **7. `src/agent/` - Main Agent Orchestration**

**Files:**
- `conversational_agent.py` - Main agent implementation
- `__init__.py` - Package exports

**Key Class: `ConversationalAgent`**
```python
__init__(settings)               # Initialize all components
async process(user_input, state) # Main processing pipeline
reset()                          # Reset agent
```

**Processing Pipeline:**
```
User Input
    ↓
Add to Memory
    ↓
Detect Intent
    ↓
Retrieve RAG Context
    ↓
Build Prompt
    ↓
Call LLM
    ↓
Add Response to Memory
    ↓
Return AgentState
```

**Why here?** Orchestrates all other components in a cohesive workflow.

---

## 🗂️ Knowledge Base (`knowledge_base/`)

**Contents:**
- `sample_faq.json` - FAQ in JSON format
- `about_company.md` - Company info in Markdown

**Format Support:**
```json
// JSON: List of objects with "content", "text", or "body" field
[
  {
    "id": "unique_id",
    "content": "Information text",
    "category": "optional_field"
  }
]
```

```markdown
# Markdown: Any text content
- All content is extracted and used for retrieval
- No specific format required
```

**Best Practices:**
- Keep documents focused on single topics
- Use clear titles and structure
- Add context fields for better retrieval
- Regularly update with new information

---

## 🧪 Tests (`tests/`)

**Files:**
- `test_intent_detector.py` - Intent detection unit tests
- `test_memory.py` - Memory management tests
- `test_lead_capture.py` - Lead capture tests

**Run tests:**
```bash
pytest tests/ -v                 # Run all tests
pytest tests/test_memory.py      # Run specific test
pytest --cov=src tests/          # With coverage
```

**Why comprehensive?** Ensures each module works independently.

---

## 🚀 Entry Point (`main.py`)

**Interactive CLI Agent**
```python
asyncio.run(main())              # Async event loop
```

**Features:**
- Interactive chat interface
- Shows detected intent for each message
- Support for "exit" and "reset" commands
- Error handling with user-friendly messages

**Usage:**
```bash
python main.py
You: Hello!
Assistant: Hi there! How can I help you?
[Intent: greeting]

You: exit
Goodbye!
```

---

## 🔧 Setup & Configuration

### **1. Environment Setup**
```bash
# Copy template
cp .env.example .env

# Edit .env with your settings
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
KNOWLEDGE_BASE_PATH=./knowledge_base
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Add Knowledge Base**
```bash
# Place your documents in knowledge_base/
# - JSON files: {key: "value"} or [{key: value}, ...]
# - Markdown files: Any .md file
```

### **4. Run Agent**
```bash
python main.py
```

---

## 📈 Scalability & Extension Points

### **Add New Intent Types**
```python
# In src/core/types.py
class Intent(str, Enum):
    FEEDBACK = "feedback"        # New intent
    COMPLAINT = "complaint"
```

### **Add New Tools**
```python
# Create src/tools/new_tool.py
class NewTool:
    def execute(self, **kwargs):
        pass

# Import in src/agent/conversational_agent.py
self.new_tool = NewTool()
```

### **Switch to Vector Database**
```python
# In src/rag/retriever.py
# Replace keyword matching with embedding similarity
from langchain_community.vectorstores import FAISS

class KnowledgeBaseRetriever:
    def __init__(self, settings):
        self.vectorstore = FAISS.from_documents(docs, embeddings)
    
    def retrieve(self, query):
        return self.vectorstore.similarity_search(query, k=self.top_k)
```

### **Add Database for Leads**
```python
# In src/tools/lead_capture.py
import sqlite3

class LeadCaptureTool:
    def __init__(self):
        self.db = sqlite3.connect("leads.db")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY,
                name TEXT, email TEXT, ...
            )
        """)
```

### **Implement Multi-Turn Workflows**
```python
# Build state machines for complex conversations
state_machine = {
    Intent.HIGH_INTENT_LEAD: {
        "next_step": "collect_email",
        "required_fields": ["name", "email", "company"]
    }
}
```

---

## 🏗️ Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Dependency Injection** | Settings passed to modules | Testable, flexible |
| **Abstract Base Class** | BaseAgent | Easy to create new agent types |
| **Dataclass** | Message, AgentState | Type-safe, clear structure |
| **Enum** | Intent | Type-safe intent classification |
| **Async/Await** | All I/O operations | Non-blocking, high performance |
| **Store & Separate** | Each module is independent | Loosely coupled, maintainable |

---

## 📊 Dependencies & Versions

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.1.10 | LLM framework |
| langgraph | 0.0.26 | Workflow orchestration (optional) |
| langchain-openai | 0.0.11 | OpenAI integration |
| pydantic | 2.5.0 | Data validation |
| python-dotenv | 1.0.0 | Environment variables |
| pytest | 7.4.3 | Testing framework |
| loguru | 0.7.2 | Advanced logging |

---

## ⚡ Performance Considerations

1. **Async Operations**: LLM calls are async, non-blocking
2. **Memory Limits**: Configurable conversation history prevents memory bloat
3. **Top-K Retrieval**: Only retrieves necessary documents
4. **Lazy Loading**: Knowledge base loaded on-demand
5. **JSONL Format**: Append-only, no full rewrites for leads

---

## 🔐 Security Notes

1. Never commit `.env` with real API keys
2. Use environment variables for sensitive data
3. Validate all user inputs
4. Log sensitive operations (without credentials)
5. Keep dependencies updated for security patches

---

## 📝 Next Steps

1. Replace `gpt-4-turbo-preview` with your preferred model
2. Populate `knowledge_base/` with your data
3. Customize intent detection prompt
4. Add domain-specific tools
5. Deploy with cloud platform (Docker recommended)

---

## 🆘 Troubleshooting

**Q: Error loading knowledge base?**  
A: Check `knowledge_base/` directory exists and files are valid JSON/Markdown

**Q: API key not recognized?**  
A: Ensure `.env` has `OPENAI_API_KEY` set correctly

**Q: Memory growing too large?**  
A: Reduce `MAX_CONVERSATION_MEMORY` in `.env`

**Q: Slow responses?**  
A: Reduce `RETRIEVAL_TOP_K` or use LangChain caching

---

## 📄 License

This project is provided as-is for educational and commercial use.
