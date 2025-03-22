from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr
from configs import settings

class Memory:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self._get_embedding_function(),
            persist_directory="./storage/memories"
        )
        self.memory = VectorStoreRetrieverMemory(retriever=self.vector_store.as_retriever())

    def _get_embedding_function(self):
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=SecretStr(settings.gemini_api_key)
        )
