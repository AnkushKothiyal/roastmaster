"""
Roast Generator - A Gemini-powered app that creates funny roasts
Author: Ankush kothiyal
"""
import streamlit as st
import google.generativeai as genai


model = genai.GenerativeModel("gemini-2.0-flash")

# Page config
st.set_page_config(page_title="Roast Master", page_icon="🔥")

api_key = st.sidebar.text_input("Enter your Google AI API Key", type="password")
# genai.configure(api_key='AIzaSyCq1VdjVJNCgaIia16nUquJnsVW0QiOdsA')

# Title and description
st.title("🔥 Roast Master")
st.write("Enter a situation and get a funny roast from our AI Roast Master!")
situation = st.text_area("Describe your situation:", placeholder="I was eating an ice cream on my way to the office, and it fell down.")

# Create button first, then check conditions
# generate_button = st.button("Generate Roast 🔥")

prompt = f"""
                You are a Roast Master who can produce some of the best roast. You'll be given a situation often a negative one and your job is to create a concise roast for the person.
                Keep in mind the following qualities of a good roast:

                1. Sharp Wit and Humor: This is the most fundamental quality. The roast needs to be genuinely funny. The humor should be clever, demonstrating wit rather than just being silly or crude without a point. The jokes should evoke laughter or at least a chuckle through their ingenuity and comedic timing (even on paper).

                2. Specificity and Personalization: A good roast is not generic. It targets the specific individual being roasted. The jokes should be rooted in their known traits, quirks, habits, accomplishments, and perhaps even well-known failures or stories.  Generic jokes fall flat in a roast because they lack that personal punch. Reading a good roast should make you feel like "Yes, that's exactly something they do/are like!"

                3. Originality and Unpredictability: Clichés and expected jokes are the enemies of a good roast. The best roasts surprise you. They take a familiar trait of the roastee and twist it in an unexpected or novel way. Reading a roast line that makes you think "I never thought of it that way before!" is a sign of originality.

                4. Conciseness and Impact: Roast lines are often short, punchy, and to the point. Every word should ideally contribute to the humor. Reading thegood roast line should feel efficient and impactful, delivering the joke quickly and effectively without unnecessary rambling.

                5. Play on the grammar - If there is a misspelled word or the grammar is incorrect, you may include that in your roast too.

                For example, if the situation is: 'I had an interview but at the last moment they cancelled it.'
                Then some examples of a good roast could be:
                1. They must have seen your resume and realized they already had enough clowns for the office.
                2. They said they found someone 'more qualified,' but I suspect it was a squirrel in a tiny suit who could juggle staplers.

                Note - Don't include anything else in the response like 'Here is the roast' or 'Roast:' or anything else. Just respond with the roast line.

                Keeping the above context in mind,
                here is a situation, roast it with a funny line.

                situation {situation}
                """


genai.configure(api_key=api_key)

if st.button("Generate Roast 🔥"):
    if not api_key:
        st.warning("Please enter your API key.")
    else:
        try:
            with st.spinner("Cooking your roast :smiling_imp:"):
                response = model.generate_content(prompt)
                st.success("Gemini Response:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.error(f"Detailed error: {str(e)}") 


# Footer
st.markdown("---")
st.markdown("Created by Ankush Kothiyal | Powered by Google's Gemini AI")
