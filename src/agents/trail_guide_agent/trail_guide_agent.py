import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Load environment variables from .env file

AZURE_AI_PROJECT_ENDPOINT = "https://ai-account-svjmdnobmzv36.services.ai.azure.com/api/projects/ai-project-my-dev-trail-guide"
MODEL_NAME = "GPT-5.1"
AGENT_NAME = "trail-guide"
# Read instructions from prompt file
prompt_file = Path(__file__).parent / 'prompts' / 'v2_instructions.txt'
with open(prompt_file, 'r') as f:
    instructions = f.read().strip()
print(f"Instructions loaded from {prompt_file}: {instructions[:100]}...")  # Print first 100 chars
print(f"print endpoint: {AZURE_AI_PROJECT_ENDPOINT}")
print(f"print model: {MODEL_NAME}")
project_client = AIProjectClient(
    endpoint=AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_NAME,  # Use Global Standard model
        instructions=instructions,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")