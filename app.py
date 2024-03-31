# run command with no redirect: streamlit run app.py 
import streamlit as st
import wiki
import textwrap
import os

# Function to mimic response from an AI (placeholder)
def get_answer(question: str):
    answer = wiki.ask(st.session_state.get('document_path'), question, st.session_state.get('selected_topic'))['result'].strip()
    wrapped_lines = textwrap.wrap(answer, width=80)
    return '\n'.join(wrapped_lines)

# Define the main chat function
def main_chat():
    st.title("Chat with WikiWise")
    st.write(f"Topic: {st.session_state.get('selected_topic', '')}")
    st.write(f"Wiki URL: {st.session_state.get('wiki_url', '')}")

    # Wrap the chat input in a form and use the form's submit button
    with st.form(key="chat_form"):
        question = st.text_input("Ask a question:", placeholder="Type your message here...")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and question:
        # Simulate sending a message and receiving a response
        st.session_state.chat_history.append(f"You: {question}")

        answer = get_answer(question)
        st.session_state.chat_history.append(f"AI: {answer}")
        
    # Button to go back to the home screen
    if st.button("Back to Home"):
        st.session_state.update({'display_main_chat': False, 'selected_topic': '', 'chat_history': []})
        os.remove(st.session_state.get('document_path'))
        st.rerun()
        
    # Display chat history
    for message in st.session_state.get('chat_history', []):
        st.text(message)


# Define the topic entry screen
def topic_entry():
    st.title("Welcome to the WikiWise")
    
    topic = st.text_input("Please enter a topic to get started:", key="topic", placeholder="Monkeys, The War of 1812, The Simpsons, etc...")
    
    if st.button("Submit"):
        if len(topic) > 0:
            url = wiki.get_url(topic).replace(' ', '_')
            if 'en.wikipedia.org' not in url:
                st.error("No Wikipedia page found for the topic. Please try again and make sure you spell it right.")
                return
            
            path = wiki.save_url_as_pdf(url, topic)
            
            
            st.session_state.update({'display_main_chat': True, 'selected_topic': topic, 'chat_history': [], 'wiki_url': url, 'document_path': path})
            st.rerun()
        else:
            st.error("Please enter a topic to continue.")
        
    return
    
    
# Initialize session state keys if they don't exist
if 'display_main_chat' not in st.session_state:
    st.session_state.display_main_chat = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Control flow to display the appropriate screen based on the state
if st.session_state.get('display_main_chat'):
    main_chat()
else:
    topic_entry()
