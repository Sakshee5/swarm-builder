import streamlit as st
from dotenv import load_dotenv
from configs.agents import *
from swarm import Swarm 

def get_response():
    client = Swarm()

    response = client.run(
        agent=manager_agent,
        messages= st.session_state.messages,
        context_variables=context_variables,
        stream=False,
        debug=False,
    )
    
    return response.messages


load_dotenv()

# Initialize session state variables
if "name" not in st.session_state:
    st.session_state.name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Login page
if st.session_state.name is None:
    st.title("Welcome to Inception - OpenAI Swarm")
    st.caption("Please log in to continue.")

    name_input = st.text_input("Enter your preferred name:")

    # Confirm login button
    if st.button("Log In"):
        if name_input:
            st.session_state.name = name_input
        else:
            st.error("Please enter a name to continue.")

# Main Chat Interface
else:
    with st.sidebar:
        st.write("""## What Do We Offer?
        
Prototyping new ideas often demands significant time just to establish a foundational structure. With this tool, you can efficiently build and test multiple concepts at a basic level, giving you the freedom to explore and iterate at high speed. Validate 10 ideas in the time it would typically take to fully prototype just one!

By providing a robust foundation that you can build on within minutes, we're here to streamline your workflow and accelerate your creative process. 🙂""")

    st.title("💬 Inception - OpenAI Swarm")
    st.caption("🚀 A swarm to build swarms!")
    st.success(f"Welcome, {st.session_state.name}!")

    # Context variables for the session
    context_variables = {"user_name": st.session_state.name}

    # Display chat messages from session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Describe your idea here..."):
        
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(f"**User**: {user_input}")

        # Agent response handling
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    response_messages = get_response()

                for message in response_messages:

                    if message['role'] == 'assistant' and message['content']:
                        st.markdown(f"**{message['role']}**: {message['content']}")
                    st.session_state.messages.append(message)
        
            except Exception as e:
                st.error(f"Error occurred: {str(e)}")
