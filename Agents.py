#GOING TO BUILD ALL THE AGENTS HERE USING TOOLS FROM Tools.py file

from dotenv import load_dotenv
from Tools import search_from_tavily, search_from_url
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from rich import print

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

response = model.invoke('hey')

agent_for_web_scraping = create_agent(
    model=model,
    tools=[
        search_from_tavily,
        search_from_url
    ],
    system_prompt="""
    You are a web research assistant.

    Tool selection rules:

    1. If the user provides a specific URL and asks
       for information from that URL, use search_from_url.

    2. If the user asks for information about a topic
       without providing a specific URL, use search_from_tavily.

    3. Do not call search_from_tavily when a specific URL
       has already been provided unless additional web research
       is explicitly required.

    4. Keep the amount of retrieved information concise.
    """
)
parser = StrOutputParser()
chat = HumanMessage(content=input('user:'))

response = agent_for_web_scraping.invoke({
    'messages':chat
})
print(response)
print("-"*100)
print(response['messages'][-1].content)