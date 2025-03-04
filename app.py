# streamlit_app.py
import streamlit as st
from crewai import Crew, Process
from agents import query_agent, summarization_agent
from task import retrieval_task, summarization_task
import os
import io
import sys
import time  # Import the time module


@st.cache_resource
def create_crew_agents():
    crew = Crew(
        agents=[
            query_agent,
            summarization_agent
        ],
        tasks=[retrieval_task, summarization_task],
        process=Process.sequential,
        verbose=True
    )
    return crew

crew_instance = create_crew_agents()

def get_response(user_query, conversation_history):
    """Handles the CrewAI interaction with error handling."""
    try:
        result = crew_instance.kickoff(inputs={"user_input": user_query, "conversation_history": "\n".join(conversation_history)})
        return result
    except Exception as e:
        st.error(f"An error occurred during Crew execution: {e}")
        return None  # Return None in case of error


st.title("Legal Chatbot for Indian Law")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What's up?"):


    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        assistant_response = get_response(prompt, [message["content"] for message in st.session_state.messages if message["role"] == "user"])

        if assistant_response:
            # Assuming 'assistant_response' is a CrewOutput object and has a 'text' attribute
            try:
                response_text = assistant_response.text  # Try to access the 'text' attribute
            except AttributeError:
                try:
                    response_text = assistant_response.response #Try to access the 'response' attribute
                except AttributeError:
                    response_text = str(assistant_response) #Fallback: Convert the entire object to a string

            for chunk in response_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.write("The assistant was unable to generate a response.")