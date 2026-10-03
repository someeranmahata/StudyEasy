#TOOLS DEFINING
from rich import print
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from tavily import TavilyClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling.loader import DoclingLoader
import os

load_dotenv()

tavily_client = TavilyClient(os.getenv('TAVILY_API_KEY'))
pdf_content = None
pdf_name = None

@tool
def search_from_url(url:str)-> str:
    """Load and extract information from a webpage when the url/link is given."""
    loader = WebBaseLoader(url)
    data = loader.load()
    
    text = "\n".join(doc.page_content for doc in data)

    return text[:10000]


@tool
def search_from_tavily(topic:str)-> str:
    """searching from tavily if any information is not present in the database."""
    research = tavily_client.search(
        query=topic,
        search_depth='basic',
        max_results=3
    )
    # research: dict->type, dict['result']->dict type {'url', 'title', 'content', 'score', 'raw_content', 'id'}

    results = []

    for item in research["results"]:
        results.append(
            f"Title: {item['title']}\n"
            f"URL: {item['url']}\n"
            f"Content: {item['content']}"
        )

    return "\n\n".join(results)


@tool
def similar_context_from_chromaDB(topic: str) -> str:
    """Search the existing ChromaDB for information relevant to the topic."""

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory="chromaDB",
        embedding_function=embeddings
    )

    results = vector_store.similarity_search(topic, k=3)

    if not results:
        return "No relevant information was found in ChromaDB."

    context = "\n\n".join(
        f"Document {i+1}:\n{doc.page_content}"
        for i, doc in enumerate(results)
    )

    return context


@tool
def create_vector_db(pdf_path: str) -> str:
    """Create a ChromaDB from the provided PDF when its content is not already available."""
    
    loader = PyPDFLoader("book2.pdf")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chromaDB"
    )

    return "Vector database created successfully from the PDF."



'''  
1.vector db check: 
create_vector_db.invoke('book2.pdf')
result = similar_context_from_chromaDB.invoke('questions of chapter 1')

print(result)

2.search web check:
result = search_from_tavily.invoke('about machine learning')
print(type(result), len(result))
for item in result:
    print(len(item))

'''
