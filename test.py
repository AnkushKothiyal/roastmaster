import streamlit as st
from google import genai

st.title("Gemini API Test")

api_key = st.sidebar.text_input("Enter your Google AI API Key", type="password")

if st.button("Test Gemini API"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        try:
            with st.spinner("Calling Gemini..."):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents="Say hello"
                )
                st.success("Gemini Response:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error(f"Detailed error: {str(e)}") # Print full error for debugging
