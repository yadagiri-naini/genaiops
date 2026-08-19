"""
Interactive test script for Trail Guide Agent.
Allows you to chat with the agent from the terminal.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from .env file
#set os to windows

env_path = Path("C:/Users/yadagiri.naini/sources/aiops/genaiops/.env")#load_dotenv(env_path)



def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""
    print(f"Loading environment variables from .env file...")
    AZURE_AI_PROJECT_ENDPOINT = "https://ai-account-svjmdnobmzv36.services.ai.azure.com/api/projects/ai-project-my-dev-trail-guide"
    print(f"AZURE_AI_PROJECT_ENDPOINT: {AZURE_AI_PROJECT_ENDPOINT}")
    print(f"AGENT_NAME: {os.getenv('AGENT_NAME', 'trail-guide-v1')}")
    # Initialize project client
    project_client = AIProjectClient(
        endpoint=AZURE_AI_PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    )
    
    # Get agent name from environment or use default
    agent_name = os.getenv("AGENT_NAME", "trail-guide")

    openai_client = project_client.get_openai_client()
    
    print(f"\n{'='*60}")
    print(f"Trail Guide Agent - Interactive Chat")
    print(f"Agent: {agent_name}")
    print(f"{'='*60}")
    print("\nType your questions or requests. Type 'exit' or 'quit' to end the session.\n")
    
    # Create a thread for the conversation
    conversation = openai_client.conversations.create()
    print(f"Started conversation (Conversation ID: {conversation.id})\n")
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nEnding session. Goodbye!")
                break
            
            # 1) Add the user message to the conversation as an item
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{
                    "type": "message",
                    "role": "user",
                    "content": user_input
                }]
            )

            # 2) Ask the agent to respond
            response = openai_client.responses.create(
                # NOTE: the sample uses `conversation=...` (not conversation_id)
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
                input="",  # sample keeps this empty because the message is already in the conversation items
            )

            print(f"Agent: {response.output_text}")
                    
    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up thread
        try:
            openai_client.conversations.delete(conversation.id)
            print(f"Conversation thread cleaned up.")
        except:
            pass

if __name__ == "__main__":
    interact_with_agent()