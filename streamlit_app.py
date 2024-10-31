import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_completion_openai(messages):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )

    reply = response.choices[0].message.content

    return reply

st.sidebar("""## What Do We Offer?

Prototyping new ideas often demands significant time just to establish a foundational structure. With this tool, you can efficiently build and test multiple concepts at a basic level, giving you the freedom to explore and iterate at high speed. Validate 10 ideas in the time it would typically take to fully prototype just one!

By providing a robust foundation that you can build on within minutes, we're here to streamline your workflow and accelerate your creative process. 🙂
""")

st.title("💬 Inception - OpenAI Swarm")
st.caption("🚀 A swarm to build swarms!")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        reply = get_completion_openai(st.session_state.messages)

        st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})