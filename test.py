import streamlit as st
import google.generativeai as genai

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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_submitted" not in st.session_state:
    st.session_state.api_key_submitted = False
if "model" not in st.session_state:
    st.session_state.model = None

# Main app title
st.title("🔥 RoastMaster 3000")
st.subheader("Describe a situation and let AI roast it!")

# API key input section
if not st.session_state.api_key_submitted:
    with st.form(key="api_key_form"):
        api_key = st.text_input("Enter your Google Gemini API Key:", 
                                type="password", 
                                help="Get a key at https://aistudio.google.com/app/apikey")
        submit_api_key = st.form_submit_button("Submit API Key")
        
        if submit_api_key and api_key:
            try:
                # Configure Gemini with the provided API key
                genai.configure(api_key=api_key)
                st.session_state.model = genai.GenerativeModel('gemini-pro')
                # Test the API key with a simple generation
                test_response = st.session_state.model.generate_content("Say 'API connection successful'")
                st.session_state.api_key_submitted = True
                st.rerun()
            except Exception as e:
                st.error(f"Error with API key: {str(e)}")

# Main app functionality (only shown after API key is submitted)
if st.session_state.api_key_submitted:
    # Function to get roast from Gemini
    def get_roast(situation):
        prompt = f"""
        I need you to roast this situation with clever, witty humor:
        
        "{situation}"
        
        Be creative, funny, and slightly edgy, but avoid being cruel or offensive.
        Keep your response concise and focused on the situation described.
        Start with "🔥 Roast: " and don't include explanations.
        """
        
        try:
            response = st.session_state.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating roast: {str(e)}"
    
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
            roast = get_roast(user_input)
        
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
    
    # Option to reset API key
    if st.button("Change API Key"):
        st.session_state.api_key_submitted = False
        st.rerun()

# Instructions
with st.expander("How to use"):
    st.markdown("""
    1. Enter your Google Gemini API key (get one from Google AI Studio)
    2. Enter a situation you want roasted in the text box
    3. Click "Get Roasted" to receive a witty, humorous take on your situation
    4. Share multiple situations for multiple roasts!
    
    The RoastMaster will respond with a creative, funny take on your situation.
    """)

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini | Created with Streamlit")
