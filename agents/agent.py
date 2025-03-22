from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from configs import settings

class Agent:
    def __init__(self, name, description, identity_prompt, tools = []):
        self.name = name
        self.description = description
        self.identity_prompt = identity_prompt
        self.tools = tools

        self._create_executor()

    def _create_executor(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.identity_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])


        llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            api_key=settings.gemini_api_key,
            temperature=0.7
        )

        agent = create_tool_calling_agent(
            llm=llm,
            tools=self.tools,
            prompt=prompt,
        )

        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True,
            max_iterations=5
        )

    def invoke(self, input: str) -> dict:
        return self.executor.invoke({"input": input})
