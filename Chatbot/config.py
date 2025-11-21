"""
Configuration file for Research Assistant
Handles API keys and model settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# ============================================================================
# API KEYS - REPLACE WITH YOUR ACTUAL KEYS
# ============================================================================

# Google Gemini API Key
# Get FREE key at: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyD7KbUXSCXnqcI74qIrfxxFspPYHlbsVwM")

# Serper.dev API Key for web search
# Get FREE key at: https://serper.dev/
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "c7ca6ff7533692a3580ba080ff4afb94d415dddf")

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Gemini model to use
MODEL_NAME = "gemini-2.5-flash"  # Stable, widely supported model

# Temperature (0.0 = deterministic, 1.0 = creative)
TEMPERATURE = 0.5

# Maximum output tokens
MAX_TOKENS = 2048

# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

# Maximum reasoning iterations
MAX_ITERATIONS = 5

# Show agent thinking process
VERBOSE = True

# ============================================================================
# VALIDATION FUNCTION
# ============================================================================

def validate_config():
    """
    Validate that required API keys are properly configured
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    errors = []
    
    # Check Google API Key
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_gemini_api_key_here":
        errors.append("❌ GOOGLE_API_KEY not set. Get it at: https://makersuite.google.com/app/apikey")
    else:
        print("✅ Google Gemini API key found")
    
    # Check Serper API Key
    if not SERPER_API_KEY or SERPER_API_KEY == "your_serper_api_key_here":
        errors.append("❌ SERPER_API_KEY not set. Get it at: https://serper.dev/")
    else:
        print("✅ Serper API key found")
    
    # Print errors if any
    if errors:
        print("\n" + "="*70)
        print("  CONFIGURATION ERRORS")
        print("="*70)
        for error in errors:
            print(f"  {error}")
        print("="*70)
        print("\n📝 SETUP INSTRUCTIONS:")
        print("  1. Get your FREE Gemini API key:")
        print("     → Visit: https://makersuite.google.com/app/apikey")
        print("     → Sign in with Google account")
        print("     → Click 'Create API Key'")
        print("     → Copy the key")
        print("\n  2. Get your FREE Serper API key:")
        print("     → Visit: https://serper.dev/")
        print("     → Sign up (free, no credit card)")
        print("     → Copy API key from dashboard")
        print("\n  3. Add keys to this file (config.py):")
        print("     → Replace 'your_gemini_api_key_here' with actual key")
        print("     → Replace 'your_serper_api_key_here' with actual key")
        print("\n  OR create a .env file with:")
        print("     GOOGLE_API_KEY=your_actual_gemini_key")
        print("     SERPER_API_KEY=your_actual_serper_key")
        print("="*70 + "\n")
        return False
    
    print("✅ All API keys configured successfully!")
    return True


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_llm_config():
    """Get LLM configuration as dictionary"""
    return {
        "model": MODEL_NAME,
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_TOKENS
    }


def get_agent_config():
    """Get agent configuration as dictionary"""
    return {
        "max_iterations": MAX_ITERATIONS,
        "verbose": VERBOSE,
        "handle_parsing_errors": True
    }


# ============================================================================
# TEST CONFIGURATION (RUN THIS FILE DIRECTLY)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  TESTING CONFIGURATION")
    print("="*70 + "\n")
    
    # Validate
    is_valid = validate_config()
    
    if is_valid:
        print("\n🎉 Configuration is ready to use!")
        print(f"\n📊 Settings:")
        print(f"   Model: {MODEL_NAME}")
        print(f"   Temperature: {TEMPERATURE}")
        print(f"   Max Tokens: {MAX_TOKENS}")
        print(f"   Max Iterations: {MAX_ITERATIONS}")
        print(f"   Verbose: {VERBOSE}")
    else:
        print("\n⚠️  Please configure API keys before running the application.")
