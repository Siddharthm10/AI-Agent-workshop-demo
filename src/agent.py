import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from tools import TOOLS
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from prompts import AGENT_SYSTEM_PROMPT
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import random
import string


# Load env vars
load_dotenv()

def generate_tool_call_id(length=9):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Prompt setup
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(AGENT_SYSTEM_PROMPT),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# LLM setup using langchain-huggingface with custom wrapper
llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        endpoint_url=os.getenv("HF_ENDPOINT_URL"),
        huggingfacehub_api_token=os.getenv("HF_API_TOKEN"),
        task="chat-completion",
        temperature=0.2,
        max_new_tokens=1024
    )
)

# Create agent with ID validation
agent = create_tool_calling_agent(llm, TOOLS, prompt)

# Agent executor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=TOOLS, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=3 
)

# Function to run query
def run_agent(query: str):
    try:
        # Run the agent
        output = agent_executor.invoke({"input": query})
        return output
    except Exception as e:
        print(f"Error in agent execution: {str(e)}")
        # Return a graceful error message
        return {
            "output": f"I encountered an error processing your request. Please try rephrasing or simplifying your query. Technical details: {str(e)}",
            "intermediate_steps": []
        }
