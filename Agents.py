#GOING TO BUILD ALL THE AGENTS HERE USING TOOLS FROM Tools.py file

from dotenv import load_dotenv
from Tools import search_from_tavily, search_from_url
from langchain.agents import create_agent
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings, ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from rich import print
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen3.8-27B:novita'
)
model = ChatHuggingFace(llm = llm)

response = model.invoke('hey')


agent_for_web_scraping = create_agent(
    model=model,
    tools=[search_from_tavily, search_from_url],
    system_prompt= '''
        You are assistant that helps with searching tavily or any url,
        when you don't have data about that particular topic.
    '''
)
parser = StrOutputParser()
chat = HumanMessage(content=input('user:'))

response = agent_for_web_scraping.invoke({
    'messages':chat
})

print(response)