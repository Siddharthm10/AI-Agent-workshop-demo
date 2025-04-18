import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from tools import add_task, remove_task, update_task, prioritize_tasks, summarize_tasks, Task, UpdateTask
from pydantic import BaseModel
from langchain.agents import create_tool_calling_agent

from langchain_core.messages import HumanMessage

from langchain.memory import ConversationBufferMemory
from prompts import AGENT_SYSTEM_PROMPT

# Load env vars
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

class RemoveSchema(BaseModel):
    task_id: int


# Define Tools
TOOLS = [
    StructuredTool.from_function(
        func=add_task,
        name="add_task",
        description="Add a new task to the task list",
        args_schema=Task        
    ),
    StructuredTool.from_function(
        func=remove_task,
        name="remove_task",
        description="Remove a task by ID",
        args_schema=RemoveSchema
    ),
    StructuredTool.from_function(
        func=update_task,
        name="update_task",
        description="Update fields of a task using ID",
        args_schema=UpdateTask
    ),
    StructuredTool.from_function(
        func=prioritize_tasks,
        name="prioritize_tasks",
        description="List tasks sorted by deadline"
    ),
    StructuredTool.from_function(
        func=summarize_tasks,
        name="summarize_tasks",
        description="Summarize the number of tasks per status"
    ),
]

# Prompt setup
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(AGENT_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")

])

# LLM
llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.2,
    api_key=groq_api_key
)

# Memory
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history", output_key="output")

# Agent + Executor
agent = create_tool_calling_agent(llm, TOOLS, prompt)
agent_executor = AgentExecutor(agent=agent, tools=TOOLS, memory=memory, return_intermediate_steps=True, verbose=True, handle_parsing_errors=True, output_key='output')

# Function to run query
def run_agent(query: str):
    output = agent_executor.invoke({"input": query})
    
    # Log intermediate tool calls
    print("\n--- INTERMEDIATE STEPS ---")
    for step in output.get("intermediate_steps", []):
        print(step)
    
    print("\n--- FINAL OUTPUT ---")
    print(output["output"])
    return output

