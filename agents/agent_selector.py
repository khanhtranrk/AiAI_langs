import os
from .agent import Agent
from tools import command_tools

def create_agent(agent_name: str):
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_root, "identity_prompts", f"{agent_name}.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            identity_prompt = file.read()

        return Agent(
            "Sel",
            "",
            identity_prompt,
            command_tools
        )
    except:
        raise ValueError(f"Unknown agent name: {agent_name}")
