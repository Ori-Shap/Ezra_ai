import os
import anthropic
import streamlit as st

LOGO_PATH = "png-transparent-construction-robot-illustration-fotor-bg-remover-2024083110409.png"

def generate_context(selected_files: list[str], docs_path: str) -> str:
    docs = []
    for file in selected_files:
        with open(os.path.join(docs_path, file), "r") as f:
            content = f.read()
            docs.append(content)

    context = ""
    for i, doc in enumerate(docs, 1):
        context += f"Document number {i}:\n {doc}\n\n"
    return context

def set_title():
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)

    st.title("Ezra")
    st.markdown("### Here to help")

def main():
    set_title()
    api_key = st.text_input("Insert Anthropic API Key", type="password")
    if not api_key:
        st.info("Please add your Anthropic API key to continue.", icon="🗝️")
    else:
        q_and_a_app(api_key=api_key)

def q_and_a_app(api_key):
    client = anthropic.Anthropic(api_key=api_key)

    docs_path = "docs"

    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []
    if 'messages_history' not in st.session_state:
        st.session_state.messages_history = []

    md_files = [f for f in os.listdir(docs_path) if f.endswith((".md", ".txt"))]

    with st.expander("הי לפני שמתחילים תוכל לבחור נושא או כמה בבקשה?"):
        selected_files = [md_file for md_file in md_files if st.checkbox(md_file)]

    context = generate_context(selected_files=selected_files, docs_path=docs_path)

    for message in st.session_state.messages_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if selected_files:
        if prompt := st.chat_input("איך אפשר לעזור?"):
            st.session_state.messages_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("תמתין רגע בבקשה, אני בודק את המידע"):
                    messages = [
                        {
                            "role": "user",
                            "content": f"""You are an assistant who helps with questions about Israel's construction regulations. 
                            Here are the relevant documents: 

                            {context}

                            Reply to the following user input in Hebrew. If the input is not about the documents provided, 
                            gently remind the user to ask a question related to the documents: {prompt}"""
                        }
                    ]
                    
                    response = client.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=1000,
                        messages=messages
                    )
                
                assistant_response = response.content[0].text
                st.session_state.messages_history.append({"role": "assistant", "content": assistant_response})
                message_placeholder.markdown(assistant_response)