#GOING TO BUILD ALL THE AGENTS HERE USING TOOLS FROM Tools.py file

from dotenv import load_dotenv
from Tools import *
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from rich import print
from langchain_core.prompts import ChatPromptTemplate
from prompts import get_prompt
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

response = model.invoke('hey')

web_research_agent = create_agent(
    model=model,
    tools=[
        search_from_tavily,
        search_from_url
    ],
    system_prompt=get_prompt('web_research_agent')
)


pdf_research_agent = create_agent(
    model=model,
    tools=[
        similar_context_from_chromaDB,
        create_vector_db
    ],
    system_prompt=get_prompt('pdf_research_agent')
)

#AGENT -> TOOLS
@tool
def web_research_agent_tool(question: str) -> str:
    """Use this agent for web research and URL-based questions."""

    response = web_research_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    return response["messages"][-1].content


@tool
def pdf_research_agent_tool(question: str) -> str:
    """Use this agent for questions about information contained in the PDF."""

    response = pdf_research_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    return response["messages"][-1].content

checkpointer = InMemorySaver()

main_agent = create_agent(
    model=model,

    tools=[
        web_research_agent_tool,
        pdf_research_agent_tool
    ],

    system_prompt=get_prompt('main_agent'),
    checkpointer=checkpointer
)

'''
1. Testing agents
response = pdf_research_agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the main concept explained in this PDF? 'book2.pdf' "
        }
    ]
})

print(response)
print("="*80)
print(response['messages'][-1].content)

2.
print(response)
print("-"*100)
print(response['messages'][-1].content)

3. Context storing check using Checkpointer

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

response = main_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what's your name? if you don't have any then from now onwards you're name is pogo"
            }
        ]
    },
    config
)
print(response["messages"][-1].content)
print(config)


response = main_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What's your name"
            }
        ]
    },
    config
)

print(response["messages"][-1].content)
print(config)

'''