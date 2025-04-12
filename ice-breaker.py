from dotenv import load_dotenv
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from agents.linkedin_lookup_agent import linkedin_lookup
from third_parties.linkendin import scrape_linkedin_profile
from output_parsers import summary_parser

def ice_break_with(name: str) -> str:

    print("Entered Ice Breaker")

    linkedin_username = linkedin_lookup(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_username,
        mock=True
    )
   

    summary_template = """
        given the linkedin information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them

        Use information from linkedin profile 
        \n{formatted_information}
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                             partial_variables={"formatted_information": summary_parser.get_format_instructions()}, 
                                             template=summary_template)

    llm = ChatOpenAI(temperature=0, model="gpt-4o")
    #llm = ChatOllama(model='mistral')
    #chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser
    
    res = chain.invoke(input={"information": linkedin_data})
    print(res)

if __name__ == "__main__":

    load_dotenv()
    
    #print(os.environ['COOL_API_KEY'])
    
    ice_break_with(name="Siva Rama Krishna Prasad")
