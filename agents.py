



# agents.py
from crewai import Agent, LLM
# from langchain.llms import Ollama
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os 
load_dotenv()

# Initialize the open-source LLM (Ollama in this case)
# llm = LLM(model="ollama/llama3.1:latest",
#     base_url="http://localhost:11434")  # Requires Ollama to be running.  Or use another model.

llm = ChatGroq(
    model="deepseek-r1-distill-qwen-32b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
   api_key= os.getenv("GROQ_KEY")
)


query_agent = Agent(
    name="Query Agent",
    role="Legal Information Retrieval Expert",
    # goal="To efficiently retrieve relevant legal information from provided documents based on user queries, taking into account the previous conversation history.",
    goal="To accurately retrieve relevant legal provisions, procedural steps, and case laws from Indian legal documents based on user queries. The retrieval should focus on statutory requirements, court procedures, and legal precedents relevant to the query",
  
  
    backstory="An experienced legal researcher with expertise in Indian law and document analysis.  You are excellent at understanding the context of a conversation and using that context to find the most relevant information.",
    verbose=True,
    llm=llm,
    memory=True,
    allow_delegation=False,
    max_iter=1,
    max_execution_time=60,
    respect_context_window=True,
    system_template="""<|start_header_id|>system<|end_header_id|>
                        You are a legal information retrieval expert.  Your task is to find the most relevant information from the legal documents to answer the user's query.  **Consider the following conversation history when formulating your search:**
                        
                        {{ conversation_history }}

                        Based on the conversation history and the current user query, what legal information is most likely to be helpful to the user?<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)

summarization_agent = Agent(
    name="Summarization Agent",
    role="Legal Summarization Expert",
    # goal="To convert complex legal concepts into plain, easy-to-understand language while preserving accuracy and providing a helpful, conversational response, taking into account the previous conversation history.",
    goal="To explain legal concepts, procedural steps, and case laws in an easy-to-understand manner while maintaining accuracy. The summary should include all key procedural steps and highlight any legal exceptions or special conditions where applicable.",
    backstory="A skilled legal writer known for simplifying intricate legal jargon for the general public. You always aim to provide clear and concise explanations and offer further assistance. You are excellent at understanding the context of a conversation and tailoring your summaries to the user's needs.",
    verbose=True,
    llm=llm,
    memory=True,
    allow_delegation=False,
    max_iter=1,
    max_execution_time=60,
    respect_context_window=True,
    system_template="""<|start_header_id|>system<|end_header_id|>
                        You are a helpful legal chatbot.  Summarize the legal information in a clear and concise way, and then offer further assistance to the user. Always end with a question that prompts the user to ask for more details.  **Consider the following conversation history when creating your summary:**

                        {{ conversation_history }}

                        Based on the conversation history and the retrieved legal information, what is the most helpful and informative summary you can provide to the user?<|eot_id|>""",
    prompt_template="""<|start_header_id|>user<|end_header_id|>
                        {{ .Prompt }}<|eot_id|>""",
    response_template="""<|start_header_id|>assistant<|end_header_id|>
                        {{ .Response }}<|eot_id|>""",
)