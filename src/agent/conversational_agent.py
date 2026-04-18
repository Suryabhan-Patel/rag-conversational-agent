"""Main conversational agent that orchestrates all components."""
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.base_agent import BaseAgent
from src.core.types import AgentState, Message, Intent
from src.config import Settings
from src.intent import IntentDetector
from src.memory import ConversationMemory
from src.rag import KnowledgeBaseRetriever
from src.tools import LeadCaptureTool
from src.tools.lead_capture import mock_lead_capture


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
        
        # Maintain high intent once detected
        if state.current_intent == Intent.HIGH_INTENT_LEAD:
            intent = Intent.HIGH_INTENT_LEAD
        state.current_intent = intent
        
        # Enter lead capture mode if high intent detected
        if intent == Intent.HIGH_INTENT_LEAD and not state.in_lead_capture:
            state.in_lead_capture = True
        
        # Handle lead capture flow
        if state.in_lead_capture:
            response_text = self._handle_lead_capture(user_input, state)
        # Handle greeting without RAG context
        elif intent == Intent.GREETING:
            response_text = self._handle_greeting()
        # Handle query with RAG context
        else:
            # Retrieve relevant context
            context = self.retriever.retrieve(user_input)
            state.rag_context = context
            
            # Build prompt with context
            prompt = self._build_prompt(user_input, intent, context)
            
            # Generate response
            response = await self.llm.ainvoke(prompt)
            response_text = self._extract_response_text(response)
        
        assistant_message = Message(role="assistant", content=response_text)
        self.memory.add_message(assistant_message)
        state.messages.append(assistant_message)
        
        return state
    
    def _handle_greeting(self) -> str:
        """Handle greeting intent with natural response.
        
        Returns:
            Natural greeting response
        """
        return "Hi! How can I help you today?"
    
    def _handle_lead_capture(self, user_input: str, state: AgentState) -> str:
        """Handle lead capture flow step-by-step.
        
        Args:
            user_input: User's input
            state: Current agent state
            
        Returns:
            Agent response
        """
        # Step 1: Collect name
        if state.lead_name is None:
            state.lead_name = user_input.strip()
            return "Great! What's your email address?"
        
        # Step 2: Collect email
        if state.lead_email is None:
            state.lead_email = user_input.strip()
            return "Perfect! Which platform are you interested in? (e.g., YouTube, Instagram, TikTok, etc.)"
        
        # Step 3: Collect platform
        if state.lead_platform is None:
            state.lead_platform = user_input.strip()
            
            # All data collected - call mock_lead_capture
            try:
                result = mock_lead_capture(
                    name=state.lead_name,
                    email=state.lead_email,
                    platform=state.lead_platform
                )
                
                if self.lead_capture:
                    self.lead_capture.capture_lead(
                        name=state.lead_name,
                        email=state.lead_email,
                        platform=state.lead_platform
                    )
                
                return f"Thank you! Your details have been recorded. We'll be in touch with you at {state.lead_email} soon."
            except Exception as e:
                return f"Thank you for your interest! We'll follow up soon."
        
        # Lead already captured, handle follow-up
        return "Is there anything else I can help you with?"
    
    def _extract_response_text(self, response) -> str:
        """Extract text from LLM response.
        
        Args:
            response: LLM response object
            
        Returns:
            Extracted text
        """
        if isinstance(response.content, list):
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                else:
                    text_parts.append(str(item))
            return ' '.join(text_parts)
        else:
            return response.content
    
    def _build_prompt(self, user_input: str, intent: Intent, context: str) -> str:
        """Build prompt for LLM with strict RAG enforcement.
        
        Args:
            user_input: User message
            intent: Detected intent
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        conversation_history = self.memory.get_context_string()
        
        prompt = f"""You are an AI sales assistant for a SaaS product called AutoStream.

Your job is to answer product-related questions using ONLY the provided context.

CRITICAL INSTRUCTIONS:
1. ONLY use information from the provided CONTEXT below
2. Do NOT use your training knowledge
3. Do NOT add information not explicitly in the context
4. Do NOT mention custom pricing, enterprise plans, or make assumptions
5. Do NOT hallucinate or invent features
6. If the answer is NOT in the provided context, respond with: "I don't have that information"

CONTEXT FROM KNOWLEDGE BASE:
{context}

CONVERSATION HISTORY:
{conversation_history}

USER MESSAGE:
{user_input}

Generate a response using ONLY the provided context. Be concise and natural.
"""
        
        return prompt
    
    def reset(self) -> None:
        """Reset agent state."""
        self.memory.clear()
