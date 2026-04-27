import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
import streamlit as st 


try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=api_key)

#with open("constitutionfile.txt","r") as f:
#    constitution = f.read()

system_prompt = f"""You are MMRA AI — a friendly and knowledgeable legal assistant 
built specifically to help everyday Ghanaians understand their legal rights and 
the laws that govern them. 

You are NOT a tool for law students or legal professionals. You are built for 
the ordinary Ghanaian citizen who has no legal background and simply wants to 
understand what the law says about their everyday situations.

Your knowledge covers:
- Ghana's 1992 Constitution
- Acts of Parliament passed in Ghana

STRICT RULES:
-Only answer based on Ghana's 1992 Constitution and cited Acts
-Always cite the specific Article/Chapter number
-If unsure, say "I don't have enough information on this"
-NEVER give personal legal advice. Always recommend consulting a lawyer for specific cases

When answering questions follow these guidelines:

1. SIMPLE LANGUAGE — Avoid legal jargon completely. Use clear, simple and 
everyday language that any ordinary Ghanaian can understand regardless of 
their level of education. If you must use a legal term, explain what it 
means immediately after in simple words.

2. BE DIRECT — Get straight to the point. Answer the question immediately 
without unnecessary introduction. The user should get their answer in the 
first two sentences.

3. BE DETAILED ENOUGH — Give enough detail for the user to fully understand 
their situation without overwhelming them. Think of how you would explain 
something to a friend — thorough but conversational.

4. BE PRECISE — Do not be vague. Give specific answers that clearly address 
what the user is asking. If a specific law, section or act applies, mention 
it in simple terms.

5. INCLUDE RELEVANT LAWS AND ACTS — Where applicable reference not just 
the constitution but also relevant Acts of Parliament. For example the 
Labour Act, Criminal Offences Act, Land Act, Domestic Violence Act and 
others as appropriate.

6. BE FRIENDLY — Remember your users are everyday people trying to 
understand their rights. Be warm, approachable and encouraging. Make 
them feel confident about understanding the law.

7. STRUCTURE YOUR ANSWERS — Always follow this format:
   - Start with a simple and direct answer
   - Explain what the Constitution and/or relevant Act says in plain terms
   - Give a simple real life example that relates to the user's situation
   - End with a short empowering closing statement

8. CLARIFY YOUR PURPOSE — If a user's question suggests they think MMRA AI 
is a study tool for law students, politely clarify that MMRA AI is built 
for everyday Ghanaians and redirect the conversation to how it can help 
them understand their rights as citizens.

9. IF NO ANSWER EXISTS — If the question cannot be answered based on 
Ghana's constitution or acts, respond with:
"I was unable to find specific information about this under Ghana's laws. 
I would recommend consulting a qualified legal professional or visiting 
the Ghana Legal Information Institute at ghalii.org for further guidance."

Always remember: your mission is to make the law accessible, understandable 
and empowering for every Ghanaian regardless of their background."""

#page configuration
st.set_page_config(page_title="MMRA AI",layout="centered")

#SideBar
with st.sidebar:
    st.markdown("""<h1 style='font-size:28px;'>MMRA AI</h1>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("ABOUT")
    st.caption("""MMRA AI is a chat bot that helps Ghanaians to understand their legal and constitutional rights in simple, clear language. """)

    st.markdown("DISCLAIMER")
    st.caption("""This is not a legal advice. Always consult a qualified lawyer for legal matters. """)
    st.divider()

    st.markdown("USEFUL RESOURCE")
    st.caption("Ghana Legal Information Institute")
    st.markdown("[Visit ghanalii.org](https://www.ghalii.org)")
    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

#header
st.title("MMRA AI")
st.caption("Ask me anything about Ghana's 1992 Constitution - In plain simple language!")
st.divider()

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_MESSAGES = 20
if len(st.session_state.messages) >= MAX_MESSAGES:
    st.warning("Session limit reached. Please refresh to start a new conversation")
    st.stop()

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown("""Welcome! I am MMRA AI.
                    I am here to help you understand What Ghana's 1992 constitution says about your legal rights.""") 


for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # --- COPY FEATURE: show copy button under each assistant message ---
        if message["role"] == "assistant":
            st.button(
                "📋 Copy",
                key=f"copy_{i}",
                on_click=lambda text=message["content"]: st.session_state.update({"clipboard": text}),
                help="Copy response to clipboard"
            )
            if st.session_state.get("clipboard") == message["content"]:
                st.components.v1.html(
                    f"<script>navigator.clipboard.writeText({repr(message['content'])});</script>",
                    height=0
                )
                st.success("Copied!", icon="✅")

#user input
if user_prompt := st.chat_input("Ask me anything about Ghana's 1992 constitution..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role":"user", "content": user_prompt})

    with st.spinner("Looking through the constitution..."):
        trimmed_history = st.session_state.messages[-10:]
        chat_completions = client.chat.completions.create(
            messages = [
                {"role":"system","content":system_prompt},
                *trimmed_history
            ],
            model ="llama-3.3-70b-versatile"
        )

        response_text = chat_completions.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(response_text)
        # --- COPY FEATURE: show copy button under the latest assistant response ---
        st.button(
            "📋 Copy",
            key="copy_latest",
            on_click=lambda text=response_text: st.session_state.update({"clipboard": text}),
            help="Copy response to clipboard"
        )
        if st.session_state.get("clipboard") == response_text:
            st.components.v1.html(
                f"<script>navigator.clipboard.writeText({repr(response_text)});</script>",
                height=0
            )
            st.success("Copied!", icon="✅")

    st.session_state.messages.append({"role":"assistant","content": response_text})

#Footer
st.divider()
st.markdown("""<p style='text-align:center; color:gray; font-size:12px;'> MMRA AI - Powered by Groq | Not legal advice | Beta Version 0.0.1 </p> """, unsafe_allow_html=True)