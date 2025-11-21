"""
Utility functions for display and user interaction
"""
import sys
from datetime import datetime

def display_banner():
    """Display the application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║      🔬 RESEARCH / KNOWLEDGE WORKER ASSISTANT                        ║
║                                                                      ║
║              Powered by Gemini AI                                   ║
║              + Serper.dev Web Search                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def display_tips():
    """Display usage tips"""
    tips = """
======================================================================
  INTERACTIVE RESEARCH ASSISTANT
======================================================================

💡 Tips:
   - Ask any question and I'll research for you
   - Type 'exit' or 'quit' to end
   - Type 'clear' to clear screen

======================================================================
"""
    print(tips)

def get_user_input():
    """
    Get input from user with proper formatting
    
    Returns:
        str: User's input
    """
    try:
        user_input = input("\n🙋 You: ")
        return user_input
    except EOFError:
        return "exit"
    except KeyboardInterrupt:
        print("\n")
        return "exit"

def display_response(response):
    """
    Display the agent's response with formatting
    
    Args:
        response: The response text to display
    """
    print(f"\n🤖 Assistant:\n")
    print(response)
    print("\n" + "="*70)

def log_interaction(user_input, response):
    """
    Log interaction to file (optional)
    
    Args:
        user_input: User's question
        response: Agent's response
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("interaction_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"User: {user_input}\n")
            f.write(f"Assistant: {response}\n")
    except Exception as e:
        # Silently fail if logging doesn't work
        pass

def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
