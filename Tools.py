#TOOLS DEFINING
from rich import print
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from tavily import TavilyClient
import os

load_dotenv()

tavily_client = TavilyClient(os.getenv('TAVILY_API_KEY'))
pdf_content = None

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

'''    
loader = WebBaseLoader('https://english.onlinekhabar.com')
ld = loader.load()
print(len(ld), type(ld), ''.join(ld[0].page_content.split('\n\n')))    

r2 = search_from_tavily.invoke('latest news on nepal')
for item in r2['results']:
    
    search_dict = WebBaseLoader(item['url'])
    search_loader = search_dict.load()
    
    print(len(search_loader), type(search_loader))
    
_, result = search_from_tavily.invoke('about machine learning')
print(type(result), len(result))
for item in result:
    print(len(item))

'''
