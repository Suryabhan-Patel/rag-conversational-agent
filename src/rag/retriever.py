"""Knowledge base retrieval and RAG system."""
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from src.config import Settings


class KnowledgeBaseRetriever:
    """Retrieves relevant context from local knowledge base."""
    
    def __init__(self, settings: Settings):
        """Initialize knowledge base retriever.
        
        Args:
            settings: Application settings
        """
        self.kb_path = settings.knowledge_base_path
        self.top_k = settings.retrieval_top_k
        self.documents = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> List[Dict[str, Any]]:
        """Load knowledge base from JSON and Markdown files.
        
        Returns:
            List of knowledge base documents
        """
        documents = []
        
        if not self.kb_path.exists():
            self.kb_path.mkdir(parents=True, exist_ok=True)
            return documents
        
        # Load JSON files
        for json_file in self.kb_path.glob("*.json"):
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        documents.extend(data)
                    elif isinstance(data, dict):
                        documents.append(data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        # Load Markdown files
        for md_file in self.kb_path.glob("*.md"):
            try:
                with open(md_file, "r") as f:
                    content = f.read()
                    documents.append({
                        "id": md_file.stem,
                        "content": content,
                        "source": md_file.name
                    })
            except Exception as e:
                print(f"Error loading {md_file}: {e}")
        
        return documents
    
    def retrieve(self, query: str) -> str:
        """Retrieve relevant context for a query.
        
        Args:
            query: Search query
            
        Returns:
            Concatenated relevant context
        """
        if not self.documents:
            return "No knowledge base available."
        
        # Simple keyword matching (can be replaced with embeddings)
        scored_docs = []
        query_keywords = set(query.lower().split())
        
        for doc in self.documents:
            doc_text = self._extract_text(doc).lower()
            doc_keywords = set(doc_text.split())
            
            # Calculate relevance score (simple overlap)
            matches = len(query_keywords & doc_keywords)
            if matches > 0:
                scored_docs.append((doc, matches))
        
        # Sort by relevance and get top-k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = scored_docs[:self.top_k]
        
        if not top_docs:
            return "No relevant information found in knowledge base."
        
        # Concatenate context
        context = "\n\n".join([
            self._extract_text(doc[0]) for doc in top_docs
        ])
        
        return context
    
    @staticmethod
    def _extract_text(doc: Dict[str, Any]) -> str:
        """Extract text content from document."""
        if isinstance(doc, dict):
            # Try common field names
            for field in ["content", "text", "body", "description"]:
                if field in doc:
                    return doc[field]
            # If no specific field, concatenate all string values
            return " ".join(str(v) for v in doc.values() if isinstance(v, str))
        return str(doc)
