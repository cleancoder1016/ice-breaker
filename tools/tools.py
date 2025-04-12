from langchain_community.tools.tavily_search import TavilySearchResults



def get_profile_url_tavily(name: str):
    """Searches for LinkedIn Profile page"""
    search = TavilySearchResults()
    res = search.run(f"{name} Java Developer ")
    return res

if __name__ == "__main__":
    res = get_profile_url_tavily(name="Siva Rama Krishna Prasad")
    print(res)