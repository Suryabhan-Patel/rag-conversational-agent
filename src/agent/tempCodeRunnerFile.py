"""Main conversational agent that orchestrates all components."""
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.base_agent import BaseAgent
from src.core.types import AgentState, Message, Intent
from src.config import Settings
from src.intent import IntentDetector
from src.memory import ConversationMemory
from src.rag import KnowledgeBaseRetriever
from src.tools import LeadCaptureTool


class ConversationalAgent(BaseAgent):
    """Main conversational agent orchestrating all components."""
    
    def __init__(self, settings: Settings):
        """Initialize the conversational agent.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.google_api_key,
            model=settings.model_name,
            temperature=settings.temperature
        )
        self.intent_detector = IntentDetector(settings)
        self.memory = ConversationMemory(settings)
        self.retriever = KnowledgeBaseRetriever(settings)
        self.lead_capture = LeadCaptureTool() if settings.enable_lead_capture else None
    
    async def process(self, user_input: str, state: AgentState = None) -> AgentState:
        """Process user input and generate response.
        
        Args:
            user_input: User message
            state: Current agent state (optional)
            
        Returns:
            Updated agent state
        """
        if state is None:
            state = AgentState(messages=[], context={})
        
        # Add user message to memory
        user_message = Message(role="user", content=user_input)
        self.memory.add_message(user_message)
        state.messages.append(user_message)
        
        # Detect intent
        intent = await self.intent_detector.detect(user_input)
        state.current_intent = intent
        
        # Retrieve relevant context
        context = self.retriever.retrieve(user_input)
        state.rag_context = context
        
        # Build prompt with context
        prompt = self._build_prompt(user_input, intent, context)
        
        # Generate response
        response = await self.llm.ainvoke(prompt)
        
        # Handle both string and list responses
        if isinstance(response.content, list):
            # Extract text from dict objects in the list
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                else:
                    text_parts.append(str(item))
            response_text = ' '.join(text_parts)
        else:
            response_text = response.content
            
        assistant_message = Message(role="assistant", content=response_text)
        
        self.memory.add_message(assistant_message)
        state.messages.append(assistant_message)
        
        return state
    
    def _build_prompt(self, user_input: str, intent: Intent, context: str) -> str:
        """Build prompt for LLM with context.
        
        Args:
            user_input: User message
            intent: Detected intent
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        conversation_history = self.memory.get_context_string()
        
        prompt = f"""You are an AI sales assistant for a SaaS product called AutoStream.

Your job is to:
1. Answer product-related questions using ONLY the provided context
2. Detect high-intent users who want to sign up
3. Collect lead details (name, email, platform) step-by-step
4. Maintain a natural conversation

-----------------------------
IMPORTANT RULES:

1. STRICT RAG:
- Use ONLY the provided CONTEXT to answer questions
- Do NOT use your own knowledge
- If answer is not in context, say: "I don't have that information"

2. INTENT HANDLING:
- GREETING → Respond friendly
- QUERY → Answer using CONTEXT
