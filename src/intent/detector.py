"""Intent detection logic using LLM."""
from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.types import Intent, AgentState
from src.config import Settings


class IntentDetector:
    """Detects user intent from messages."""
    
    INTENT_PROMPT = """Classify the user's message intent into one of these categories:
    - greeting: Simple greetings like "hello", "hi", "how are you"
    - query: Information requests or questions
    - high_intent_lead: Strong buying signals or explicit interest in services
    - unclear: Cannot determine intent
    
    User message: {message}
    
    Respond with ONLY the intent category (one word)."""
    
    def __init__(self, settings: Settings):
        """Initialize intent detector.
        
        Args:
            settings: Application settings
        """
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=settings.google_api_key,
            model=settings.model_name,
            temperature=0.1  # Low temperature for consistent classification
        )
    
    async def detect(self, user_input: str) -> Intent:
        """Detect intent from user input.
        
        Args:
            user_input: The user's message
            
        Returns:
            Detected intent
        """
        try:
            prompt = self.INTENT_PROMPT.format(message=user_input)
            response = await self.llm.ainvoke(prompt)
            
            # Handle both string and list responses
            if isinstance(response.content, list):
                text_parts = []
                for item in response.content:
                    if isinstance(item, dict) and 'text' in item:
                        text_parts.append(item['text'])
                    else:
                        text_parts.append(str(item))
                intent_text = ' '.join(text_parts).strip().lower()
            else:
                intent_text = response.content.strip().lower()
            
            for intent in Intent:
                if intent.value in intent_text:
                    return intent
            
            return Intent.UNCLEAR
        except Exception as e:
            print(f"Error detecting intent: {e}")
            return Intent.UNCLEAR
