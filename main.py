from agents import create_agent
from guis import create_gui
import argparse

def main():
    parser = argparse.ArgumentParser(description="AiAI - langs (experiment)")
    parser.add_argument("agent_name", type=str, help="Agent name")
    parser.add_argument("gui_name", type=str, nargs="?", help="GUI name", default="textual_chatting", choices=["simple_console", "textual_chatting"])
    args = parser.parse_args()

    agent = create_agent(args.agent_name)
    gui = create_gui(args.gui_name, agent)
    gui.run()

if __name__ == "__main__":
    main()
