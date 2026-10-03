from dotenv import load_dotenv

load_dotenv()

from Tools import *
from Agents import *
from langchain_core.prompts import ChatPromptTemplate
from prompts import get_prompt

prompt = ChatPromptTemplate([
    ('system', 'summarize the text given and'),
    ('user', '{topic}')
    
])

chain = prompt | main_agent

config = {
    "configurable": {
        "thread_id": "user_1"
    }
}

while True:
    user_input = input("user: ")

    if user_input.lower() in ["quit", "exit"]:
        break

    response = chain.invoke(
        {"topic":user_input},
        config
    )

    print("="*60)
    print(response)
    print(response['messages'][-1].content)
    
