

# crew.py
import os
from crewai import Crew,  Process
from agents import query_agent, summarization_agent
from task import retrieval_task, summarization_task

# Define the crew with updated agents and tasks
crew = Crew(
    agents=[
        query_agent,
        summarization_agent
    ],
    tasks=[retrieval_task, summarization_task],
    process=Process.sequential,  # Tasks will execute in sequence: retrieval -> summarization

        verbose=True  # 
)

# Starting the task execution process with enhanced feedback
# if __name__ == "__main__":
#     user_query = input("Enter your legal query: ")
#     result = crew.kickoff(inputs={"user_input": user_query})
#     print("\n\nHere's the Answer:")
#     print(result)



if __name__ == "__main__":
    print("Welcome to the Legal Chatbot! Ask me anything about Indian law.")

    conversation_history = []  # Store the conversation history

    while True:
        user_query = input("You: ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        # Append the user query to the conversation history
        conversation_history.append(f"You: {user_query}")

        # Run the crew and get the response
        result = crew.kickoff(inputs={"user_input": user_query, "conversation_history": "\n".join(conversation_history)})

        # Append the agent's response to the conversation history
        conversation_history.append(f"Chatbot: {result}")

        print("\nChatbot:", result)
        print("\n")