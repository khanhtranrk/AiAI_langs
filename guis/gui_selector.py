def create_gui(gui_name: str, agent):
    if gui_name == "simple_console":
        from .simple_console import SimpleConsole
        return SimpleConsole(agent)
    if  gui_name == "textual_chatting":
        from .textual_chatting import TextualChatting
        return TextualChatting(agent)
    else:
        raise ValueError(f"Unknown gui name: {gui_name}")
