"""
AI Research Assistant - Web Interface
Built by: Data Science Graduate Student @ Pace University
"""
import streamlit as st
import google.generativeai as genai
from tools import create_tools
import os
import re

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="DiveIn AI - Research Companion",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD API KEYS FROM SECRETS
# ============================================================================
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
except Exception as e:
    st.error("⚠️ API keys not configured. Please set up secrets.")
    st.info("Add GOOGLE_API_KEY and SERPER_API_KEY to .streamlit/secrets.toml")
    st.stop()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'agent_initialized' not in st.session_state:
    st.session_state.agent_initialized = False
if 'tools' not in st.session_state:
    st.session_state.tools = None
if 'tool_dict' not in st.session_state:
    st.session_state.tool_dict = {}
if 'model' not in st.session_state:
    st.session_state.model = None

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    model_name = st.selectbox(
        "Select Model",
        [
            "gemini-1.5-pro-preview-0514",
            "gemini-1.5-flash-002",
            "gemini-1.5-pro-002",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ],
        index=0,
        help="Choose the AI model"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower = focused, Higher = creative"
    )
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📚 About")
    st.markdown("""
    **AI Research Assistant**
    
    Capabilities:
    - 🔍 Web search
    - 🔢 Calculations
    - 💡 AI responses
    - 📊 Research
    
    **Tech Stack:**
    - Google Gemini AI
    - Serper.dev API
    - Streamlit
    - LangChain
    """)
    
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Developer")
    st.markdown("""
    **Built by:**  
    Padmaja Preksha
    
    **Education:**  
    MS in Data Science  
    Pace University, NY
    """)

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown('<div class="main-header">🔬 DiveIn AI - Research Companion</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Built to Discover something New</div>', unsafe_allow_html=True)

# ============================================================================
# AGENT INITIALIZATION
# ============================================================================
if not st.session_state.agent_initialized:
    with st.spinner("🚀 Initializing AI Assistant..."):
        try:
            # Configure Google AI
            genai.configure(api_key=GOOGLE_API_KEY)
            
            # First, detect available models
            st.info("🔍 Detecting available models with your API key...")
            available_models = []
            
            try:
                all_models = genai.list_models()
                for model in all_models:
                    if 'generateContent' in model.supported_generation_methods:
                        model_name = model.name.split('/')[-1]
                        available_models.append(model_name)
                
                if available_models:
                    st.success(f"✅ Found {len(available_models)} available models")
                    st.info(f"Available: {', '.join(available_models[:5])}")
                else:
                    st.error("❌ No models found. Please check your API key.")
                    st.stop()
            except Exception as e:
                st.error(f"❌ Could not list models: {e}")
                # Fallback to common model names
                available_models = [
                    "gemini-1.5-flash-latest",
                    "gemini-1.5-pro-latest", 
                    "gemini-pro"
                ]
            
            # Try to create model
            model_created = False
            last_error = None
            
            for try_model in available_models:
                try:
                    st.info(f"⏳ Trying model: {try_model}")
                    
                    test_model = genai.GenerativeModel(
                        model_name=try_model,
                        generation_config={
                            "temperature": temperature,
                            "top_p": 0.95,
                            "top_k": 40,
                            "max_output_tokens": 8192,
                        }
                    )
                    
                    # Test with simple generation
                    test_response = test_model.generate_content("Say hi")
                    
                    # If we got here, model works!
                    st.session_state.model = test_model
                    st.success(f"✅ Successfully initialized: {try_model}")
                    model_created = True
                    break
                    
                except Exception as e:
                    last_error = str(e)
                    st.warning(f"⚠️ {try_model} failed: {str(e)[:100]}")
                    continue
            
            if not model_created:
                st.error("❌ Could not initialize any model")
                st.error(f"Last error: {last_error}")
                st.info("""
                **Possible solutions:**
                1. Check your Google API key is valid
                2. Visit: https://makersuite.google.com/app/apikey
                3. Generate a new API key
                4. Make sure Gemini API is enabled for your account
                """)
                st.stop()
            
            # Create tools
            os.environ['SERPER_API_KEY'] = SERPER_API_KEY
            st.session_state.tools = create_tools()
            st.session_state.tool_dict = {
                tool.name: tool for tool in st.session_state.tools
            }
            
            st.session_state.agent_initialized = True
            st.success("🎉 AI Assistant ready!")
            
        except Exception as e:
            st.error(f"❌ Initialization error: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

# ============================================================================
# WELCOME MESSAGE
# ============================================================================
if len(st.session_state.chat_history) == 0:
    with st.chat_message("assistant"):
        st.markdown("""
👋 **Welcome to AI Research Assistant!**

I can help you with:
- 🔍 **Web searches** - Current events, news, any topic
- 🔢 **Calculations** - Math problems
- 💡 **General questions** - AI-powered answers
- 📚 **Research** - Deep dives into subjects

**Try asking:**
- "What are the latest AI developments?"
- "Calculate 15% of 2500"
- "Tell me about machine learning"
- "Search for climate change news"
        """)

# ============================================================================
# CHAT HISTORY DISPLAY
# ============================================================================
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================================================
# CHAT INPUT AND PROCESSING
# ============================================================================
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process query
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Determine if tools are needed
                search_keywords = [
                    'search', 'find', 'what is', 'who is', 'when',
                    'where', 'latest', 'current', 'recent', 'news',
                    'today', 'tell me about'
                ]
                should_search = any(
                    keyword in prompt.lower() 
                    for keyword in search_keywords
                )
                
                calc_keywords = [
                    'calculate', 'compute', 'math', '+', '-', '*',
                    '/', 'sum', 'multiply', 'divide', '%'
                ]
                should_calculate = any(
                    keyword in prompt.lower() 
                    for keyword in calc_keywords
                )
                
                context = ""
                
                # Web Search
                if should_search and 'WebSearch' in st.session_state.tool_dict:
                    with st.status("🔍 Searching the web...", expanded=True):
                        try:
                            search_result = st.session_state.tool_dict['WebSearch'].func(prompt)
                            context = context + "\n\nWeb Search Results:\n" + str(search_result) + "\n"
                            st.write("✅ Search completed")
                        except Exception as e:
                            st.write(f"⚠️ Search error: {str(e)}")
                
                # Calculator
                if should_calculate and 'Calculator' in st.session_state.tool_dict:
                    with st.status("🔢 Calculating...", expanded=True):
                        try:
                            math_pattern = r'[\d\+\-\*\/\.\(\)\s%]+'
                            matches = re.findall(math_pattern, prompt)
                            if matches:
                                expression = max(matches, key=len).strip()
                                calc_result = st.session_state.tool_dict['Calculator'].func(expression)
                                context = context + "\n\nCalculation:\n" + str(calc_result) + "\n"
                                st.write("✅ Calculation completed")
                        except Exception as e:
                            st.write(f"⚠️ Calculation error: {str(e)}")
                
                # Build prompt
                if context:
                    full_prompt = (
                        "You are a helpful AI research assistant. "
                        "Provide clear, accurate, and well-structured answers.\n\n"
                        "Question: " + prompt + "\n\n" +
                        context + "\n\n"
                        "Provide a clear, helpful answer:"
                    )
                else:
                    full_prompt = (
                        "You are a helpful AI research assistant. "
                        "Provide clear, accurate, and well-structured answers.\n\n"
                        "Question: " + prompt + "\n\n"
                        "Please answer based on your knowledge. "
                        "Be concise but comprehensive.\n\n"
                        "Provide a clear, helpful answer:"
                    )

                # Generate response
                response = st.session_state.model.generate_content(full_prompt)
                response_text = response.text
                
                # Display response
                st.markdown(response_text)
                
                # Save to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": error_msg
                })

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🎓 <strong>DiveIn AI</strong> | Built with Intellegence and Innovation</p>
        <p>Designed by Padmaja Preksha, Pace University</p>
    </div>
""", unsafe_allow_html=True)
