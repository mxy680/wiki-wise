# Import necessary modules
import streamlit as st
import wiki
import textwrap


# Function to mimic response from an AI (placeholder)
def get_answer(question: str):
    # Retrieve answer from Wiki module based on the question and selected topic
    answer = wiki.ask(question, st.session_state.get('wiki_url'))['result'].strip()
    
    # Wrap the answer into lines of 80 characters for better display
    wrapped_lines = textwrap.wrap(answer, width=80)
    return '\n'.join(wrapped_lines)

# Define the main chat function
def main_chat():
    # Set up the title and display selected topic and Wiki URL
    st.title("Chat with WikiWise")
    st.write(f"Topic: {st.session_state.get('selected_topic')}")
    st.write(f"Wiki URL: {st.session_state.get('wiki_url')}")

    # Create a form for user input
    with st.form(key="chat_form"):
        question = st.text_input("Ask a question:", placeholder="Type your message here...")
        submit_button = st.form_submit_button(label="Send")

    if submit_button and question:
        # Append user's question to the chat history
        st.session_state.chat_history.append(f"You: {question}")

        # Get the AI's response to the user's question and append it to the chat history
        answer = get_answer(question)
        st.session_state.chat_history.append(f"AI: {answer}")
        
    # Button to return to the home screen
    if st.button("Back to Home"):
        # Reset session state and rerun the app to display the topic entry screen
        st.session_state.update({'display_main_chat': False, 'selected_topic': '', 'chat_history': []})
        st.rerun()
        
    # Display chat history
    for message in st.session_state.get('chat_history', []):
        st.text(message)


# Define the topic entry screen
def topic_entry():
    st.title("Welcome to the WikiWise")
    
    # Text input for the user to enter a topic
    topic = st.text_input("Please enter a topic to get started:", key="topic", placeholder="Monkeys, The War of 1812, The Simpsons, etc...")
    
    if st.button("Submit"):
        if len(topic) > 0:
            # Get the Wikipedia URL for the entered topic
            url = wiki.get_url(topic).replace(' ', '_')
            
            # Check if a valid Wikipedia page is found
            if 'en.wikipedia.org' not in url:
                st.error("No Wikipedia page found for the topic. Please try again and make sure you spell it right.")
                return
            
            # Save the Wikipedia page as a PDF and set session state variables
            path = wiki.save_url_as_pdf(url)
            st.session_state.update({'display_main_chat': True, 'selected_topic': topic, 'chat_history': [], 'wiki_url': url})
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
