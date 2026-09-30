#TOOLS DEFINING
from rich import print
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from tavily import TavilyClient
import os

load_dotenv()

tavily_client = TavilyClient(os.getenv('TAVILY_API_KEY'))


@tool
def search_from_url(url:str)-> str:
    """Load information of url passed in the function"""
    loader = WebBaseLoader(url)
    data = loader.load()
    
    return ''.join(data[0].page_content.split('\n\n'))

@tool
def search_from_tavily(topic:str)-> str:
    """searching from tavily"""
    research = tavily_client.search(
        query=topic,
        search_depth='basic',
        max_results=3
    )
    # research: dict->type, dict['result']->dict type {'url', 'title', 'content', 'score', 'raw_content', 'id'}

    return research
'''    
loader = WebBaseLoader('https://english.onlinekhabar.com')
ld = loader.load()
print(len(ld), type(ld), ''.join(ld[0].page_content.split('\n\n')))    
print('-'*50)
r2 = search_from_tavily.invoke('latest news on nepal')
print(r2)
'''
# r2 = search_from_tavily.invoke('latest news on nepal')
# for item in r2['results']:
    
#     search_dict = WebBaseLoader(item['url'])
#     search_loader = search_dict.load()
    
#     print(len(search_loader), type(search_loader))


print(search_from_url.invoke('https://english.onlinekhabar.com'))