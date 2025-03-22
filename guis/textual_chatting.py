from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog

from rich.markdown import Markdown
from rich.text import Text

import asyncio

class TextualChatting(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 1;
        grid-columns: 1fr;
        grid-rows: 1fr auto;
    }

    RichLog {
        overflow-y: auto;
        overflow-x: hidden;
        padding: 3;

        scrollbar-color: green green;
        scrollbar-gutter: stable;
        scrollbar-size: 0 0;
    }

    Input {
        border: blank;
    }
    """

    def __init__(self, agent) -> None:
        self.agent = agent
        super().__init__()

    def compose(self) -> ComposeResult:
        yield RichLog(id="chat_log", wrap=True)
        yield Input(placeholder="Type your message here...", id="chat_input")

    def on_mount(self) -> None:
        self.query_one("#chat_input", Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        chat_log = self.query_one("#chat_log", RichLog)
        chat_input = self.query_one("#chat_input", Input)

        chat_input.clear()

        prompt_text = Text()
        prompt_text.append("You: ", style="bold green")
        prompt_text.append(event.value, style="green")
        chat_log.write(prompt_text)
        chat_log.write("\n")

        async def get_response():
            return await asyncio.to_thread(self.agent.invoke, event.value)

        response = await get_response()

        chat_log.write(Markdown(response['output']))
        chat_log.write("\n")

        chat_input.focus()
