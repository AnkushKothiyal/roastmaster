import streamlit as st
from google import genai
import asyncio
import nest_asyncio

# Apply nest_asyncio to allow running asyncio in Streamlit
nest_asyncio.apply()

st.title("Gemini API Test")

api_key = st.sidebar.text_input("Enter your Google AI API Key", type="password")

if st.button("Test Gemini API"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        try:
            with st.spinner("Calling Gemini..."):
                # Configure the client
                genai.configure(api_key=api_key)
                
                # Create a synchronous wrapper for the async API call
                async def call_gemini():
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = await model.generate_content_async("Say hello")
                    return response
                
                # Run the async function in the current event loop
                loop = asyncio.get_event_loop()
                response = loop.run_until_complete(call_gemini())
                
                st.success("Gemini Response:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error(f"Detailed error: {str(e)}")  # Print full error for debugging
