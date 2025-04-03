from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == "__main__":
    """
    load_dotenv()
    print("Learning LangChain")
    print(os.environ['COOL_API_KEY'])
    """

    summary_template = """
        given the information{information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(input_variables="information", templates=summary_template)

    llm = ChatOpenAI(tempareture=0, model_name="gpt-3.5-turbo")
    chain = summary_prompt_template | llm

    res = chain.invoke(input={"information": information})