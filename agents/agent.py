from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from pydantic import SecretStr
from configs import settings

class Agent:
    def __init__(self, name, description, identity_prompt, tools=[], memory=None):
        self.name = name
        self.description = description
        self.identity_prompt = identity_prompt
        self.tools = tools
        self.memory = memory
        self._create_executor()

    def invoke(self, input: str) -> dict:
        resp = self.executor.invoke({"input": input})
        self.memory_persist() # Persist memory after each invocation
        return resp

    def memory_persist(self):
        if self.memory is not None:
            self.memory.vector_store.persist()

    # Private methods

    def _get_memory(self):
        if self.memory is None:
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

        return self.memory.memory

    def _get_promnt(self):
        return ChatPromptTemplate.from_messages([
            ("system", self.identity_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

    def _get_llm(self):
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            api_key=SecretStr(settings.gemini_api_key),
            temperature=0.7
        )

    def _create_executor(self):
        agent = create_tool_calling_agent(
            llm=self._get_llm(),
            tools=self.tools,
            prompt=self._get_promnt(),
        )

        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self._get_memory(),
            verbose=True,
            max_iterations=5
        )
