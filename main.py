"""
Main entry point for the Research Assistant
"""
import sys
from config import validate_config
from agent import ResearchAgent
from tools import create_tools
from utils import display_banner, display_tips, get_user_input, display_response

def main():
    """Main application loop"""
    
    # Display welcome banner
    display_banner()
    
    # Validate configuration
    print("\n🔧 Validating configuration...\n")
    if not validate_config():
        print("\n❌ Configuration validation failed. Please check your API keys in config.py\n")
        sys.exit(1)
    
    print("✅ All API keys configured successfully!\n")
    
    try:
        # Create tools FIRST
        print("🔧 Creating research tools...")
        tools = create_tools()
        print(f"✅ Created {len(tools)} tools: {', '.join([t.name for t in tools])}\n")
        
        # Initialize agent with tools
        agent = ResearchAgent(tools=tools)
        
        # Display usage tips
        display_tips()
        
        # Main interaction loop
        while True:
            # Get user input
            user_input = get_user_input()
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using Research Assistant! Goodbye!\n")
                break
            
            if user_input.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                display_banner()
                display_tips()
                continue
            
            # Skip empty inputs
            if not user_input.strip():
                continue
            
            # Process query
            print("\n🤖 Assistant: Processing your question...\n")
            print("=" * 70)
            response = agent.query(user_input)
            print("=" * 70)
            
            # Display response
            display_response(response)
            print()
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!\n")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
