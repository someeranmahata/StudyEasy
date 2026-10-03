#GOING TO BUILD ALL THE AGENTS HERE USING TOOLS FROM Tools.py file

from dotenv import load_dotenv
from Tools import *
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from rich import print
from langchain_core.prompts import ChatPromptTemplate


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

# print(response)
# print("-"*100)
# print(response['messages'][-1].content)

agent_context_search = create_agent(
    model=model,
    tools=[
        similar_context_from_chromaDB,
        create_vector_db
    ],
    system_prompt="""
        You are an AI assistant that answers questions using information from a PDF
        stored in ChromaDB.

        First determine whether the existing ChromaDB can provide information relevant
        to the user's question.

        Use similar_context_from_chromaDB when the vector database already exists.

        Use create_vector_db only when the PDF needs to be indexed into ChromaDB.

        After obtaining the relevant information, answer the user's question clearly
        and concisely.

        Do not invent information that is not present in the retrieved context.
        """
)
response = agent_context_search.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the main concept explained in this PDF? 'itc_book.pdf' "
        }
    ]
})

print(response)
