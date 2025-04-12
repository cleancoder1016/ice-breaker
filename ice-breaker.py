from dotenv import load_dotenv
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from agents.linkedin_lookup_agent import linkedin_lookup
from third_parties.linkendin import scrape_linkedin_profile

def ice_break_with(name: str) -> str:

    print("Entered Ice Breaker")

    linkedin_username = linkedin_lookup(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username,
        mock=False
    )
   

    summary_template = """
        given the linkedin information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    #llm = ChatOllama(model='mistral')
    chain = summary_prompt_template | llm | StrOutputParser()
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/irrelevant-for-mock-mode/",
        mock=True
    )
    res = chain.invoke(input={"information": linkedin_data})
    print(res)

if __name__ == "__main__":

    load_dotenv()
    
    #print(os.environ['COOL_API_KEY'])
    
    ice_break_with(name="Siva Rama Krishna Prasad")
