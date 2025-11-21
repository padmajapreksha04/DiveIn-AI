"""
Tool definitions for the Research Agent
"""
from langchain.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from config import SERPER_API_KEY

def create_tools():
    """
    Create and return list of tools for the agent
    
    Returns:
        List of LangChain Tool objects
    """
    tools = []
    
    # Web Search Tool using Serper
    try:
        search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)
        web_search_tool = Tool(
            name="WebSearch",
            func=search.run,
            description="Useful for searching the internet for current information, news, facts, and data. Input should be a search query string."
        )
        tools.append(web_search_tool)
    except Exception as e:
        print(f"⚠️ Warning: Could not create WebSearch tool: {e}")
    
    # Calculator Tool
    def calculate(expression: str) -> str:
        """Simple calculator for mathematical expressions"""
        try:
            # Safe evaluation of mathematical expressions
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    calculator_tool = Tool(
        name="Calculator",
        func=calculate,
        description="Useful for performing mathematical calculations. Input should be a valid mathematical expression like '2+2' or '10*5'."
    )
    tools.append(calculator_tool)
    
    # Text Summarizer Tool
    def summarize(text: str) -> str:
        """Summarize long text"""
        if len(text) <= 200:
            return text
        return text[:200] + "..."
    
    summarizer_tool = Tool(
        name="Summarizer",
        func=summarize,
        description="Useful for summarizing long text. Input should be the text you want to summarize."
    )
    tools.append(summarizer_tool)
    
    return tools
