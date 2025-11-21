"""
Tool definitions for the Research Agent
Compatible with LangChain latest versions
"""
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import os

def create_tools():
    """
    Create and return list of tools for the agent
    
    Returns:
        List of Tool objects
    """
    tools = []
    
    # Web Search Tool using Serper
    try:
        serper_key = os.environ.get('SERPER_API_KEY')
        if serper_key:
            search = GoogleSerperAPIWrapper(serper_api_key=serper_key)
            web_search_tool = Tool(
                name="WebSearch",
                func=search.run,
                description="Search the internet for current information, news, facts, and data. Input should be a search query string."
            )
            tools.append(web_search_tool)
    except Exception as e:
        print(f"Warning: Could not create WebSearch tool: {e}")
    
    # Calculator Tool
    def calculate(expression: str) -> str:
        """Simple calculator for mathematical expressions"""
        try:
            # Safe evaluation
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    calculator_tool = Tool(
        name="Calculator",
        func=calculate,
        description="Perform mathematical calculations. Input should be a valid mathematical expression like '2+2' or '10*5'."
    )
    tools.append(calculator_tool)
    
    # Summarizer Tool
    def summarize(text: str) -> str:
        """Summarize long text"""
        if len(text) <= 200:
            return text
        return text[:200] + "..."
    
    summarizer_tool = Tool(
        name="Summarizer",
        func=summarize,
        description="Summarize long text. Input should be the text you want to summarize."
    )
    tools.append(summarizer_tool)
    
    return tools
