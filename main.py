"""Main entry point for the conversational AI agent."""
import asyncio
from pathlib import Path
from src.config import Settings
from src.agent import ConversationalAgent
from src.core.types import AgentState


async def main():
    """Run the conversational AI agent."""
    # Load settings
    settings = Settings()
    
    # Initialize agent
    agent = ConversationalAgent(settings)
    
    print("Conversational AI Agent Started")
    print("Type 'exit' to quit, 'reset' to clear history")
    print("-" * 50)
    
    state = AgentState(messages=[], context={})
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if user_input.lower() == "reset":
                agent.reset()
                state = AgentState(messages=[], context={})
                print("Conversation reset.")
                continue
            
            # Process input
            state = await agent.process(user_input, state)
            
            # Print response
            if state.messages:
                last_message = state.messages[-1]
                if last_message.role == "assistant":
                    print(f"\nAssistant: {last_message.content}")
                    print(f"[Intent: {state.current_intent.value}]")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
