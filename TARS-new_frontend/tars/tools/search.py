import json
import string
import re

from langchain_community.tools import DuckDuckGoSearchRun
from bs4 import BeautifulSoup
from crewai_tools import tool


def remove_html(content):
    oline = content
    soup = BeautifulSoup(oline, "html.parser")
    for data in soup(["style", "script"]):
        data.decompose()
    tmp = " ".join(soup.stripped_strings)
    tmp = "".join(filter(lambda x: x in set(string.printable), tmp))
    tmp = re.sub(" +", " ", tmp)
    return tmp


# Initialize DuckDuckGo search tool
search_tool = DuckDuckGoSearchRun()


@tool("SearchEngine")
def search_engine(query: str) -> str:
    """
    Search-Engine tool for browsing the web and getting urls, titles, and website snippets using DuckDuckGo

    Parameters:
    - query (str): Query that will be sent to the search engine

    Returns:
    - str: The search result from the query containing relevant information and snippets
    """
    try:
        # Get raw results from DuckDuckGo
        results = search_tool.run(query)
        
        # Format the results in a readable way
        formatted_results = ""
        for line in results.split("\n"):
            if line.strip():
                formatted_results += f"SNIPPET: {remove_html(line)}\n\n"
        
        return formatted_results.strip()
    except Exception as e:
        return f"Search failed: {str(e)}"
