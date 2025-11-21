"""
Check available Google Gemini models with your API key
"""
import google.generativeai as genai
from config import GOOGLE_API_KEY

print("🔍 Checking available models with your API key...\n")

try:
    # Configure API
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # List all available models
    print("=" * 70)
    print("AVAILABLE MODELS:")
    print("=" * 70)
    
    models = genai.list_models()
    content_gen_models = []
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            content_gen_models.append(model.name)
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100] if model.description else 'N/A'}...")
    
    print("\n" + "=" * 70)
    print(f"TOTAL: {len(content_gen_models)} models support content generation")
    print("=" * 70)
    
    if content_gen_models:
        print(f"\n✅ Use one of these model names in your config.py:")
        for model_name in content_gen_models:
            # Show both full and short names
            short_name = model_name.split('/')[-1]
            print(f"   - '{short_name}'  (or '{model_name}')")
    else:
        print("\n❌ No models found! Check your API key.")
        print("   Visit: https://makersuite.google.com/app/apikey")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid API key")
    print("2. API key doesn't have access to Gemini models")
    print("3. Network/firewall blocking the request")
    print("\n👉 Get a valid key at: https://makersuite.google.com/app/apikey")
