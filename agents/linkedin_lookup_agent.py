import os
from dotenv import load_dotenv
from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from tools.tools import get_profile_url_tavily


load_dotenv()

def linkedin_lookup(name:str) -> str:
    print(f"Entered LinkedIn Lookup with name: {name}")
    llm = ChatOpenAI(
        temperature=0,
        model = "gpt-4o",
    )
    template = """Given the full name {name_of_person} I want you to get me a link to their LinkedIn Profile Page.
                    Your answer should only contain a url"""

    prompt_template = PromptTemplate (
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name = "Crawl google for linkedin profile page",
            func=get_profile_url_tavily,
            description="use when you need to get the linkedin page url",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)


    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = linkedin_lookup(name="Siva Rama Krishna Prasad")
    print(linkedin_url)