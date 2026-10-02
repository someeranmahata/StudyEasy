#TOOLS DEFINING
from rich import print
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from tavily import TavilyClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
def similar_context_from_chromaDB(topic:str)->list:
    f"""search and extract information for the existing database
        that has information about the document {pdf_content}
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        persist_directory="chromaDB",
        embedding_function=embeddings
    )
    results = vector_store.similarity_search(
        f"{topic}",
        k=3
    )
    return results

@tool
def create_vector_db(pdf_path: str, topic:str) -> list:
    f"""Create a ChromaDB vector database from a PDF file.
        if the pdf is not same as previous {pdf_content}"""
        
    pdf_name=pdf_path
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chromaDB"
    )

    return similar_context_from_chromaDB(topic)





'''    

result = search_from_tavily.invoke('about machine learning')
print(type(result), len(result))
for item in result:
    print(len(item))

'''
