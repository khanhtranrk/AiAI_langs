import os
import shortuuid
import time
from .agent import Agent
from .memory import Memory

def create_agent(agent_name: str):
    # Load the identity prompt for the agent
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "identity_prompts", f"{agent_name}.txt")
    with open(file_path, "r", encoding="utf-8") as file:
        identity_prompt = file.read()

    # Create memory
    memory = Memory(collection_name=f"CONV_{agent_name}_{int(time.time())}_{shortuuid.random(length=8)}")

    print(f"Created agent {agent_name} with memory {memory.collection_name}")

    return Agent(agent_name, "", identity_prompt, [], memory)
