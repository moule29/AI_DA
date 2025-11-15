import streamlit as st
import google.generativeai as genai

st.title("Gemini Chatbot")

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load model (choose Gemini 1.5 Flash or Pro)
MODEL_ID = "gemini-flash-latest"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history for Gemini
    chat_history = [
        {"role": m["role"], "parts": [m["content"]]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        model = genai.GenerativeModel(MODEL_ID)
        response = model.generate_content(chat_history, stream=True)

        output = ""
        for chunk in response:
            if chunk.text:
                output += chunk.text
                st.write(chunk.text)

    st.session_state.messages.append({"role": "model", "content": output})

