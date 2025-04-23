from typing import Optional
from langchain.tools import tool
import pandas as pd
import os

TASKS_FILE = "tasks.xlsx"

# Create Excel file if not exists
if not os.path.exists(TASKS_FILE):
    pd.DataFrame(columns=["id", "title", "description", "deadline", "status"]).to_excel(TASKS_FILE, index=False)

# ------------------ Helpers ------------------

def load_tasks():
    return pd.read_excel(TASKS_FILE)

def save_tasks(df):
    df.to_excel(TASKS_FILE, index=False)

# ------------------ Tool Functions ------------------

@tool
def add_task(title: str, deadline: str, description: str = "", status: str = "pending") -> str:
    """Add a new task to the task list.
    
    Args:
        title: The title of the task
        deadline: The deadline in YYYY-MM-DD format
        description: Optional description of the task
        status: Task status (pending, in progress, done)
        
    Returns:
        Confirmation message with the new task ID
    """
    df = load_tasks()
    new_id = 1
    if not df.empty and "id" in df.columns:
        new_id = df["id"].max() + 1
    df.loc[len(df)] = [new_id, title, description, deadline, status]
    save_tasks(df)
    return f"Task '{title}' added with ID {new_id}"

@tool
def remove_task(task_id: int) -> str:
    """Remove a task by ID.
    
    Args:
        task_id: The ID of the task to remove
        
    Returns:
        Confirmation message
    """
    df = load_tasks()
    if task_id not in df["id"].values:
        return f"No task with ID {task_id}"
    df = df[df["id"] != task_id]
    save_tasks(df)
    return f"Task {task_id} removed"

@tool
def update_task(id: int, title: Optional[str] = None, description: Optional[str] = None, 
                deadline: Optional[str] = None, status: Optional[str] = None) -> str:
    """Update fields of a task using ID.
    
    Args:
        id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        deadline: New deadline in YYYY-MM-DD format (optional)
        status: New status (optional)
        
    Returns:
        Confirmation message
    """
    df = load_tasks()
    valid_statuses = ["pending", "in progress", "done"]
    if status and status not in valid_statuses:
        return f"Invalid status: {status}. Must be one of {valid_statuses}"
    
    if id not in df["id"].values:
        return f"No task with ID {id}"
        
    idx = df[df["id"] == id].index[0]
    
    # Create a dictionary of non-None values to update
    update_data = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "status": status
    }
    
    # Filter out None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # Update the dataframe
    for field, value in update_data.items():
        df.at[idx, field] = value
    
    save_tasks(df)
    return f"Task {id} updated"

@tool
def prioritize_tasks() -> str:
    """List tasks sorted by deadline.
    
    Returns:
        A string with tasks ordered by deadline
    """
    df = load_tasks()
    df["deadline"] = pd.to_datetime(df["deadline"], errors='coerce')
    df = df.dropna(subset=["deadline"]).sort_values("deadline")
    tasks = df[["id", "title", "deadline"]].astype(str).values.tolist()
    return "Prioritized tasks:\n" + "\n".join([f"ID: {t[0]}, Title: {t[1]}, Deadline: {t[2]}" for t in tasks])

@tool
def clear_tasks() -> str:
    """Clear all the tasks in the list.
    
    Returns:
        Nothing
    """
    df = load_tasks()
    df = df[0:0]
    save_tasks(df)

@tool
def summarize_tasks() -> str:
    """Summarize the number of tasks per status.
    
    Returns:
        A summary of task counts by status
    """
    df = load_tasks()
    counts = df["status"].value_counts().to_dict()
    return "Task Summary:\n" + "\n".join([f"{k}: {v}" for k, v in counts.items()])

# Define Tools
TOOLS = [add_task, remove_task, update_task, prioritize_tasks, summarize_tasks, clear_tasks]