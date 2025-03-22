class SimpleConsole:
    def __init__(self, agent):
        self.agent = agent

    def run(self):
        while True:
            text = input("You: ")
            if text == "exit":
                break
            response = self.agent.invoke(text)
            print("Bot:", response["output"])
