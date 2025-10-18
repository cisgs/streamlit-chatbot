import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Personalities",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Available Groq models
AVAILABLE_MODELS = {
    "llama-3.1-8b-instant": "Llama 3.1 8B Instant",
    "llama-3.1-70b-versatile": "Llama 3.1 70B Versatile",
    "llama-3.1-8b-versatile": "Llama 3.1 8B Versatile",
    "mixtral-8x7b-32768": "Mixtral 8x7B",
    "gemma-7b-it": "Gemma 7B IT"
}

# Personality configurations
PERSONALITIES = {
    "Math Teacher": {
        "description": "Expert in mathematics, algebra, geometry, calculus, and problem-solving",
        "system_prompt": """You are a Math Teacher. You ONLY answer questions related to mathematics, including:
- Mathematical concepts and theories
- Problem-solving techniques
- Algebra, geometry, calculus, statistics
- Mathematical proofs and explanations
- Educational math content

If asked about anything unrelated to mathematics, politely decline and redirect to math topics. Always provide clear, educational explanations with examples when possible.""",
        "allowed_topics": ["Mathematics", "Algebra", "Geometry", "Calculus", "Statistics", "Problem Solving"]
    },
    "Doctor": {
        "description": "Medical professional specializing in health, symptoms, and medical advice",
        "system_prompt": """You are a Doctor. You ONLY answer questions related to health and medicine, including:
- Medical symptoms and conditions
- Health advice and wellness
- Medical procedures and treatments
- Anatomy and physiology
- Healthcare information

If asked about anything unrelated to health or medicine, politely decline and redirect to health topics. Always remind users to consult with healthcare professionals for serious medical concerns.""",
        "allowed_topics": ["Health", "Medicine", "Symptoms", "Medical Advice", "Anatomy", "Physiology"]
    },
    "Travel Guide": {
        "description": "Expert travel advisor with knowledge of destinations, tips, and planning",
        "system_prompt": """You are a Travel Guide. You ONLY answer questions related to travel and tourism, including:
- Travel destinations and attractions
- Travel planning and itineraries
- Travel tips and advice
- Cultural information about places
- Transportation and accommodation
- Travel safety and requirements

If asked about anything unrelated to travel, politely decline and redirect to travel topics. Provide practical, helpful travel advice.""",
        "allowed_topics": ["Travel", "Destinations", "Tourism", "Planning", "Culture", "Transportation"]
    },
    "Chef": {
        "description": "Culinary expert specializing in cooking, recipes, and food preparation",
        "system_prompt": """You are a Chef. You ONLY answer questions related to cooking and food, including:
- Recipes and cooking techniques
- Ingredient information and substitutions
- Kitchen tips and tricks
- Food preparation methods
- Culinary techniques and skills
- Food safety and storage

If asked about anything unrelated to cooking or food, politely decline and redirect to culinary topics. Provide detailed, practical cooking advice.""",
        "allowed_topics": ["Cooking", "Recipes", "Food", "Ingredients", "Kitchen Tips", "Culinary Techniques"]
    },
    "Tech Support": {
        "description": "Technical support specialist for devices, software, and troubleshooting",
        "system_prompt": """You are a Tech Support specialist. You ONLY answer questions related to technology and technical support, including:
- Software troubleshooting
- Hardware issues and solutions
- Technical problem-solving
- Device configuration and setup
- Network and connectivity issues
- Technical documentation and guides

If asked about anything unrelated to technology or technical support, politely decline and redirect to tech topics. Provide clear, step-by-step technical solutions.""",
        "allowed_topics": ["Technology", "Software", "Hardware", "Troubleshooting", "Technical Support", "IT"]
    }
}

class PersonalityChatbot:
    def __init__(self, api_key, model="llama-3.1-8b-instant"):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.conversation_history = []
    
    def chat(self, message, personality):
        """Send a message to the chatbot with personality enforcement"""
        try:
            # Get personality system prompt
            system_prompt = PERSONALITIES[personality]["system_prompt"]
            
            # Create messages with system prompt
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": message})
            
            # Get response from Groq
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            response = chat_completion.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
    if "personality" not in st.session_state:
        st.session_state.personality = "Math Teacher"
    if "model" not in st.session_state:
        st.session_state.model = "llama-3.1-8b-instant"

def main():
    """Main Streamlit app"""
    initialize_session_state()
    
    # Header
    st.title("🤖 AI Chatbot with Personalities")
    st.markdown("Chat with AI personalities powered by Groq models!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            value=os.getenv('GROQ_API_KEY', ''),
            help="Get your free API key from https://console.groq.com/"
        )
        
        if not api_key:
            st.error("Please enter your Groq API key to continue.")
            st.stop()
        
        # Model selection
        st.subheader("🧠 AI Model")
        selected_model = st.selectbox(
            "Choose AI Model",
            options=list(AVAILABLE_MODELS.keys()),
            format_func=lambda x: AVAILABLE_MODELS[x],
            index=0
        )
        
        # Personality selection
        st.subheader("🎭 Personality")
        selected_personality = st.selectbox(
            "Choose Chatbot Personality",
            options=list(PERSONALITIES.keys()),
            index=0
        )
        
        # Display personality info
        if selected_personality in PERSONALITIES:
            st.info(f"**{selected_personality}**: {PERSONALITIES[selected_personality]['description']}")
            st.write("**Allowed Topics:**")
            for topic in PERSONALITIES[selected_personality]['allowed_topics']:
                st.write(f"• {topic}")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.messages = []
            if st.session_state.chatbot:
                st.session_state.chatbot.clear_history()
            st.rerun()
        
        # Initialize chatbot if API key is provided
        if api_key and (not st.session_state.chatbot or 
                       st.session_state.model != selected_model or 
                       st.session_state.personality != selected_personality):
            try:
                st.session_state.chatbot = PersonalityChatbot(api_key, selected_model)
                st.session_state.model = selected_model
                st.session_state.personality = selected_personality
                st.success("✅ Chatbot initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize chatbot: {str(e)}")
    
    # Main chat interface
    st.subheader(f"💬 Chat with {st.session_state.personality}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get chatbot response
        if st.session_state.chatbot:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.chat(prompt, st.session_state.personality)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Please configure your API key and model in the sidebar.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Powered by [Groq](https://console.groq.com/) | Built with [Streamlit](https://streamlit.io/)**"
    )

if __name__ == "__main__":
    main()
