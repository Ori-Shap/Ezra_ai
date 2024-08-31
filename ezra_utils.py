import os
from openai import OpenAI
import ai21
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from ai21.models.chat import ChatMessage
import streamlit as st

AI21_KEY = "0AgGyLuj3v4ei7XbIPGZ17HLPzRRSwt5"
LOGO_PATH = "png-transparent-construction-robot-illustration-fotor-bg-remover-2024083110409.png"


def generate_context(selected_files: list[str], docs_path: str) -> list[str]:
    docs = []
    for file in selected_files:
        with open(os.path.join(docs_path, file), "r") as f:
            content = f.read()
            docs.append(content)

    context = ""
    for i in range(1, len(docs)+1):
        context = context + f"Document number {i}:\n {docs[i-1]}\n\n"
    return context


def set_title():
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)

    st.title("Ezra")
    st.markdown("### Here to help")


def main():
    set_title()
    api_key = st.text_input("Insert API Key", type="password")
    if not api_key:
        st.info("Please add your API key to continue.", icon="🗝️")
    else:
        q_and_a_app(api_key=api_key)


def q_and_a_app(api_key):
    # Create an OpenAI client.
    # client = OpenAI(api_key=OAI_KEY)
    client_ai21 = ai21.AI21Client(api_key=api_key)

    # Show title and description.
    # Check if the file exists before attempting to load it
    docs_path = "docs"

    # Initialize session state to store selected files if it doesn't exist
    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []
    if 'messages_history' not in st.session_state:
        st.session_state.messages_history = []
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Get a list of all .md files in the 'docs' folder
    md_files = [f for f in os.listdir(docs_path) if (f.endswith(".md") or f.endswith(".txt"))]

    # Display checkboxes for each .md file

    with st.expander("הי לפני שמתחילים תוכל לבחור נושא או כמה בבקשה?"):
        selected_files = []
        for md_file in md_files:
            if st.checkbox(md_file):
                selected_files.append(md_file)

    context = generate_context(selected_files=selected_files,
                               docs_path=docs_path)

    for idx, message in enumerate(st.session_state.messages_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if selected_files:
        # User input
        if prompt := st.chat_input("איך אפשר לעזור?"):
            new_message = ChatMessage(role="user",
                                      content=f"""\
        Here is a set of documents regarding Israel's construction\
        regulations {context} \n\n---\n\n reply to the following user input in hebrew, :{prompt}, \
        if the user input is not about the documents provided, \
        gently remind the user to ask a question related to the documents provided.""")
            
            
            st.session_state.messages.append(new_message)

            st.session_state.messages_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            # print(st.session_state.messages)
            # Get bot response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("תמתין רגע בבקשה, אני בודק את המידע"):
                    response = client_ai21.chat.completions.create(messages=st.session_state.messages,
                                                                model="jamba-1.5-large",
                                                                stream=False)
                st.session_state.messages.append(ChatMessage(role="assistant",
                                                             content=response.choices[0].message.content))
                st.session_state.messages.remove(new_message)
                st.session_state.messages.append(ChatMessage(role="user", content=prompt))
                st.session_state.messages_history.append({"role": "assistant", "content": response.choices[0].message.content})
                message_placeholder.markdown(response.choices[0].message.content)
                print(st.session_state.messages)

        # # Generate an answer using the OpenAI API.
        # stream = vlient.chat.completions.create(
        #     model="gpt-40",
        #     messages=messages,
        #     stream=True,
        # )

        # Stream the response to the app using `st.write_stream`.
        # st.write_stream(stream)
