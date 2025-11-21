"""
Research Agent Implementation using Google Gemini (Native SDK)
"""
import google.generativeai as genai
from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE

class ResearchAgent:
    """Autonomous Research Agent powered by Google Gemini"""
    
    def __init__(self, tools):
        """
        Initialize the Research Agent
        
        Args:
            tools: List of LangChain tools (WebSearch, Calculator, etc.)
        """
        print("🚀 Initializing Research Assistant...")
        
        try:
            # Configure Google Generative AI
            print(f"   → Configuring Google AI...")
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # Clean up model name - remove any "models/" prefix if present
            clean_model_name = MODEL_NAME.replace("models/", "")
            
            # List available models to verify
            print(f"   → Checking available models...")
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            print(f"   → Available models: {', '.join([m.split('/')[-1] for m in available_models[:3]])}...")
            
            # Use gemini-pro if the requested model isn't available
            if not any(clean_model_name in model for model in available_models):
                print(f"   ⚠️ {clean_model_name} not found, using gemini-pro instead")
                clean_model_name = "gemini-pro"
            
            # Initialize Gemini model
            print(f"   → Loading {clean_model_name}...")
            self.model = genai.GenerativeModel(
                model_name=clean_model_name,
                generation_config={
                    "temperature": TEMPERATURE,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            print("   ✅ Model initialized successfully")
            
            # Store tools
            self.tools = tools
            self.tool_dict = {tool.name: tool for tool in tools}
            print(f"   ✅ Loaded {len(tools)} tools: {', '.join([t.name for t in tools])}")
            
            print("\n✅ Research Assistant fully initialized!\n")
            
        except Exception as e:
            print(f"\n❌ Failed to initialize agent: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def query(self, question: str) -> str:
        """
        Process a user query and return the response
        
        Args:
            question: User's input question
            
        Returns:
            Agent's response as a string
        """
        try:
            # Check if we should use web search
            search_keywords = ['search', 'find', 'what is', 'who is', 'when', 'where', 'latest', 'current', 'recent', 'news', 'today']
            should_search = any(keyword in question.lower() for keyword in search_keywords)
            
            # Check if we should use calculator
            calc_keywords = ['calculate', 'compute', 'math', '+', '-', '*', '/', 'sum', 'multiply', 'divide']
            should_calculate = any(keyword in question.lower() for keyword in calc_keywords)
            
            context = ""
            
            # Use WebSearch tool if needed
            if should_search and 'WebSearch' in self.tool_dict:
                print("\n🔍 Searching the web...")
                try:
                    search_result = self.tool_dict['WebSearch'].func(question)
                    context += f"\n\n**Web Search Results:**\n{search_result}\n"
                    print("✅ Search completed")
                except Exception as e:
                    print(f"⚠️ Search failed: {e}")
            
            # Use Calculator tool if needed
            if should_calculate and 'Calculator' in self.tool_dict:
                print("\n🔢 Calculating...")
                try:
                    # Extract mathematical expression from question
                    import re
                    math_pattern = r'[\d\+\-\*\/\.\(\)\s]+'
                    matches = re.findall(math_pattern, question)
                    if matches:
                        expression = max(matches, key=len).strip()
                        calc_result = self.tool_dict['Calculator'].func(expression)
                        context += f"\n\n**Calculation Result:**\n{calc_result}\n"
                        print("✅ Calculation completed")
                except Exception as e:
                    print(f"⚠️ Calculation failed: {e}")
            
            # Create prompt for the LLM
            prompt = f"""You are a helpful AI research assistant. Answer questions clearly and concisely.

Question: {question}

{context if context else "Please answer based on your knowledge."}

Provide a clear, helpful answer:"""
            
            # Get response from Gemini
            print("\n💭 Thinking...")
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"❌ Error processing query: {str(e)}"
