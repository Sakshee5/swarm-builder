import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from configs.agents import *
from swarm.repl import streamlit_loop


if "name" not in st.session_state:
    st.session_state.name = None

# Login page
if st.session_state.name is None:

    st.title("Welcome to Inception - OpenAI Swarm")
    st.caption("Please log in to continue.")
    
    name_input = st.text_input("Enter your preferred name:")

    # Confirm login button
    if st.button("Log In"):
        if name_input:
            st.session_state.name = name_input
            st.success(f"Welcome, {st.session_state.name}!")
        else:
            st.error("Please enter a name to continue.")

else:

    with st.sidebar:
        # swarm_type = st.selectbox(label='Choose swarm type..', options=['OpenAI Swarm', 'CrewAI', 'MetaGPT', 'AutoGPT'])
        st.write("""## What Do We Offer?

Prototyping new ideas often demands significant time just to establish a foundational structure. With this tool, you can efficiently build and test multiple concepts at a basic level, giving you the freedom to explore and iterate at high speed. Validate 10 ideas in the time it would typically take to fully prototype just one!

By providing a robust foundation that you can build on within minutes, we're here to streamline your workflow and accelerate your creative process. 🙂""")

    st.title("💬 Inception - OpenAI Swarm")
    st.caption("🚀 A swarm to build swarms!")

    context_variables = {'user_name': st.session_state.name}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Describe your idea here.."):
        while True:
            with st.chat_message("user"):
                st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                reply = streamlit_loop(st.session_state.messages, manager_agent, context_variables=context_variables, debug=True)
                
                if reply:
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
