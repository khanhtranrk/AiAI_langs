from langchain.tools import Tool
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import subprocess
import requests
from bs4 import BeautifulSoup
from configs import settings

# Initialize ChromaDB
embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=settings.gemini_api_key
)

# Set up ChromaDB with the Gemini embedding function
vectorstore = Chroma(
    collection_name="my_collection",
    embedding_function=embedding_function,
    persist_directory="./chroma_db"
)

# Tool: Query ChromaDB for relevant Linux commands
def search_chromadb(query: str) -> str:
    results = vectorstore.similarity_search(query, k=1)
    return results[0].page_content if results else ""

search_tool = Tool(
    name="Chromadb_search",
    func=search_chromadb,
    description="Search for Linux command knowledge in ChromaDB."
)

# Tool: Search the web for Linux commands
def web_search(query: str) -> str:
    search_url = f"https://www.google.com/search?q={query}+linux+command"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    snippets = [s.get_text() for s in soup.find_all("span")]
    return "\n".join(snippets[:5]) if snippets else "No relevant results."

web_search_tool = Tool(
    name="web_Search",
    func=web_search,
    description="Search the web for Linux command information."
)

# Tool: Execute Linux command safely
def execute_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=5)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

execute_tool = Tool(
    name="execute_linux_command",
    func=execute_command,
    description="Execute a given Linux command safely and return the output."
)

# List of tools available for the agent
command_tools = [search_tool, web_search_tool, execute_tool]
