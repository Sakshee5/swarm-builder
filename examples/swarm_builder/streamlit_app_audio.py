import streamlit as st
from dotenv import load_dotenv
from configs.agents import *
from swarm import Swarm
import openai
from gtts import gTTS
from io import BytesIO
import os
from audio_recorder_streamlit import audio_recorder  # New import

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to convert text to audio
def transcribe_text_to_audio(text):
    tts = gTTS(text, lang='en')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# Function to transcribe audio to text using the updated OpenAI API
def transcribe_audio_to_text(audio_bytes):
    try:
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "audio.wav"  # Give a dummy filename for API compatibility
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return response  # Directly returns the transcribed text
    except Exception as e:
        st.error(f"An error occurred during transcription: {e}")
        return None

# Function to get a response from the Swarm manager agent
def get_response():
    client = Swarm()
    response = client.run(
        agent=manager_agent,
        messages=st.session_state.messages,
        context_variables=context_variables,
        stream=False,
        debug=False,
    )
    return response.messages

# Initialize session state variables
if "name" not in st.session_state:
    st.session_state.name = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "recording" not in st.session_state:
    st.session_state.recording = False
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None  # Track captured audio data

# Login page
if st.session_state.name is None:
    st.title("Welcome to Inception - OpenAI Swarm")
    st.caption("Please log in to continue.")
    name_input = st.text_input("Enter your preferred name:")

    if st.button("Log In"):
        if name_input:
            st.session_state.name = name_input
        else:
            st.error("Please enter a name to continue.")

# Main Chat Interface
else:
    with st.sidebar:
        st.write("""## What Do We Offer?
        
Prototyping new ideas often demands significant time just to establish a foundational structure. With this tool, you can efficiently build and test multiple concepts at a basic level, giving you the freedom to explore and iterate at high speed. 
Validate 10 ideas in the time it would typically take to fully prototype just one!

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

    # Recording buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎙️ Start Recording"):
            st.session_state.recording = True
            st.session_state.audio_data = None  # Reset audio data at start
    with col2:
        if st.button("🛑 Stop Recording"):
            st.session_state.recording = False

    # Capture audio only after recording is started
    if st.session_state.recording:
        st.write("Recording... Click 'Stop Recording' to finish.")
        st.session_state.audio_data = audio_recorder()  # Record audio once

    # Process and display transcription only when recording stops
    if st.session_state.audio_data and not st.session_state.recording:
        st.write("Processing audio...")

        # Transcribe audio to text
        user_input = transcribe_audio_to_text(st.session_state.audio_data)
        st.session_state.audio_data = None  # Clear audio data after processing

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(f"User: {user_input}")

            # Get response from the Swarm manager agent
            with st.chat_message("assistant"):
                try:
                    with st.spinner("Thinking..."):
                        response_messages = get_response()
                        for message in response_messages:
                            response_text = message["content"]
                            st.markdown(f"{message['role']}: {response_text}")
                            st.session_state.messages.append(message)

                            # Convert assistant response to audio and play it
                            response_audio_bytes = transcribe_text_to_audio(response_text)
                            st.audio(response_audio_bytes, format="audio/mp3")
        
                except Exception as e:
                    st.error(f"Error occurred: {str(e)}")