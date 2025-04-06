import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)



load_dotenv()

def lookup(name:str) -> str:
    return "https://www.linkedin.com/in/siva-rama-krishna-prasad-changala-a3115a253/"