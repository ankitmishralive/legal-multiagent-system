

# task.py
from crewai import Task
from agents import query_agent, summarization_agent
from tools import legal_retrieval_tool

retrieval_task = Task(
    description=(
        # "Based on the user query: '{user_input}', retrieve the most relevant sections from the legal documents to accurately answer the query.  Focus on extracting the specific information requested and provide context where necessary."
   "Based on the user query: '{user_input}', retrieve the most relevant sections from Indian legal statutes (e.g., CPC, CrPC, Contract Act) and procedural guidelines that accurately answer the query. Extract complete steps, conditions, and exceptions where applicable"
    
    ),
    expected_output=(
        "Relevant sections from the legal documents that directly address the user's query.  The sections should be complete and include any necessary context."
    ),
    tools=[legal_retrieval_tool],  # Use the LegalRetrievalTool
    agent=query_agent
)

summarization_task = Task(
    description=(
        # "Based on the retrieved legal information, convert the complex legal concepts into plain, easy-to-understand language while preserving accuracy.  Provide clear and concise explanations, avoiding legal jargon.  The goal is to make the information accessible to a layperson.  **The response should be formatted as a helpful chatbot message, ending with a question to encourage the user to ask for more details.**"
  
  "Based on the retrieved legal information, provide a clear, structured summary of the procedural steps, statutory requirements, and case law in plain language. Ensure completeness by listing all steps in sequence, highlighting any exceptions, and avoiding unnecessary legal jargon"
  
    ),
    expected_output=(
        "A clear and concise summary of the legal information, written in plain language and formatted as a chatbot response.  The summary should accurately reflect the meaning of the original text, be easily understood by a non-lawyer, and **end with a question prompting the user to ask for more information.**"
    ),
    agent=summarization_agent
)