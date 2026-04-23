import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
import streamlit as st 

api_key=st.secrets.get["GROQ_API_KEY"]
client = Groq(api_key=api_key)

#with open("constitutionfile.txt","r") as f:
#    constitution = f.read()

system_prompt = f"""You are a friendly and knowledgeable assistant that helps everyday Ghanaians understand
their constitutional rights and laws. Your job is to explain what Ghana's 1992 Constitution says in a way that
anyone can understand, regardless of their educational background or knowledge of law

When answering questions, followthese  guidelines:
1. SIMPLE LANGUAGE - Avoid legal jargon. Use clear,simple  and everyday language that anyone can understand.
If you must use a legal term, explain what it means immediately after.

2. BE PRECISE - Give direct and accurate answers based strictly on what the constitution says. Do not add personal opinions or information
from outside the constitution.

3. BE FRIENDLY - Remember your users are everyday people trying to understand their rights. Be warm, approachable and encouraging.

4. STRUCTURE YOUR ANSWERS - When answering, follow this format:
-Start with a simple direct answer
-Explain what the constitution specifically says
-Give a simple real life example where possible 

5. IF NO ANSWER EXISTS - If the constitution does not address the question asked, respond with: 
"I was unable to find information about this in Ghana's 1992 Constitution. I'd recommend consulting a 
legal professional or visiting the Ghana Legal Information Institute at ghalii.org for further guidance"""

#page configuration
st.set_page_config(page_title="MMRA AI", layout="centered")

#header
st.title("MMRA AI")
st.caption("Ask me anything about Ghana's 1992 Constitution - In plain simple language! - This is a beta version")
st.divider()

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""Welcome! I am MMRA AI.
                    I am here to help you understand What the Ghana 1992 constitution says about your right and everyday situations""") 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#user input
if user_prompt := st.chat_input("Ask me anything about Ghana's 1992 constitution..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

        st.session_state.messages.append({"role":"user", "content": user_prompt})

    with st.spinner("Looking through the constitution..."):
        chat_completions = client.chat.completions.create(
            messages = [
                {"role":"system","content":system_prompt},
                *st.session_state.messages
            ],
            model ="llama-3.3-70b-versatile"
        )

        response_text = chat_completions.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role":"assistant","content": response_text})