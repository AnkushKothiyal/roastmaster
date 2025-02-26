import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="RoastMaster 3000",
    page_icon="🔥",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: white;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #2D2D2D;
    }
    .bot-message {
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configure Gemini API
def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Please set your Google API key in the .env file")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_roast(situation, model):
    prompt = f"""
    I need you to roast this situation with clever, witty humor:
    
    "{situation}"
    
    Be creative, funny, and slightly edgy, but avoid being cruel or offensive.
    Keep your response concise and focused on the situation described.
    Start with "🔥 Roast: " and don't include explanations.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating roast: {str(e)}"

# Main app layout
st.title("🔥 RoastMaster 3000")
st.subheader("Describe a situation and let AI roast it!")

# Initialize Gemini model
model = configure_genai()

# Input area
with st.form(key="situation_form"):
    user_input = st.text_area("Describe a situation to roast:", 
                              placeholder="Example: I spent three hours making a fancy dinner and then accidentally dropped it on the floor...")
    submit_button = st.form_submit_button("Get Roasted")

# Process input and generate response
if submit_button and user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get roast from Gemini
    with st.spinner("The RoastMaster is thinking..."):
        roast = get_roast(user_input, model)
    
    # Add bot response to chat
    st.session_state.messages.append({"role": "bot", "content": roast})

# Display chat history
if st.session_state.messages:
    st.subheader("Roast Session")
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div><strong>You:</strong></div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div><strong>RoastMaster:</strong></div>
                <div>{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Instructions
with st.expander("How to use"):
    st.markdown("""
    1. Enter a situation you want roasted in the text box
    2. Click "Get Roasted" to receive a witty, humorous take on your situation
    3. Share multiple situations for multiple roasts!
    
    **Note:** You'll need a Google API key with access to Gemini API. 
    Create a `.env` file in the same directory as this script with:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```
    """)

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini | Created with Streamlit")
