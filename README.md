# Conversational AI Agent with LangChain/LangGraph

A production-ready conversational AI agent that combines intent detection, RAG, and tool calling for lead capture with persistent conversation state.

## Features

- 🎯 **Intent Detection**: Classify user inputs (greeting, query, high-intent lead)
- 📚 **RAG System**: Retrieves context from local knowledge base (JSON/Markdown)
- 🔧 **Tool Calling**: Automated lead capture and external tool integration
- 💾 **Conversation Memory**: Maintains context across multiple turns
- 🏗️ **Modular Architecture**: Clean separation of concerns for scalability
- 🧪 **Fully Testable**: Comprehensive test suite included

## Project Structure

```
new_project/
├── src/                          # Main source code
│   ├── agent/                    # Core agent orchestration
│   ├── core/                     # Base classes and utilities
│   ├── intent/                   # Intent detection module
│   ├── rag/                      # RAG/retrieval system
│   ├── memory/                   # Conversation memory management
│   ├── tools/                    # Tool definitions and handlers
│   ├── config/                   # Configuration management
│   └── __init__.py
├── knowledge_base/               # RAG knowledge base files
├── tests/                        # Unit and integration tests
├── logs/                         # Application logs
├── .env.example                  # Environment variables template
├── requirements.txt              # Python dependencies
├── main.py                       # Entry point
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Configure your API keys in .env
```

## Quick Start

```bash
python main.py
```

## Configuration

See `.env.example` for all available options.
