
import streamlit as st
from google import genai
import asyncio
import os

st.title("Gemini API Test")

api_key = st.sidebar.text_input("Enter your Google AI API Key", type="password")

if st.button("Test Gemini API"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        try:
            with st.spinner("Calling Gemini..."):
                # Set the API key as an environment variable to avoid any auth issues
                os.environ["GOOGLE_API_KEY"] = api_key
                
                # Initialize the client
                client = genai.Client(api_key=api_key)
                
                
                # Create a new event loop and set it as the current one for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Now use the synchronous API which will work with the newly set event loop
                response = client.models.generate_content( model="gemini-2.0-flash",contents="Say hello")
                
                st.success("Gemini Response:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error(f"Detailed error: {str(e)}")  # Print full error for debugging
