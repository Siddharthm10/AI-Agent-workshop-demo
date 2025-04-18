from typing import List, Optional
from pydantic import BaseModel, Field
import pandas as pd
from datetime import datetime
import os

TASKS_FILE = "tasks.xlsx"

# Create Excel file if not exists
if not os.path.exists(TASKS_FILE):
    pd.DataFrame(columns=["id", "title", "description", "deadline", "status"]).to_excel(TASKS_FILE, index=False)

# ------------------ Schemas ------------------

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    deadline: str = Field(..., example="2025-04-20")
    status: Optional[str] = "pending"

class UpdateTask(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None

# ------------------ Helpers ------------------

def load_tasks():
    return pd.read_excel(TASKS_FILE)

def save_tasks(df):
    df.to_excel(TASKS_FILE, index=False)

# ------------------ Tool Functions ------------------

def add_task(title: str, deadline: str, description: str = "", status: str = "pending", id: int = None) -> str:
    print("[TOOL CALL] add_task")
    df = load_tasks()
    new_id = id if id is not None else (df["id"].max() + 1 if not df.empty else 1)
    df.loc[len(df)] = [new_id, title, description, deadline, status]
    save_tasks(df)
    return f"Task '{title}' added with ID {new_id}"

def remove_task(task_id: int) -> str:
    df = load_tasks()
    if task_id not in df["id"].values:
        return f"No task with ID {task_id}"
    df = df[df["id"] != task_id]
    save_tasks(df)
    return f"Task {task_id} removed"

def update_task(update: UpdateTask) -> str:
    df = load_tasks()
    if update.id not in df["id"].values:
        return f"No task with ID {update.id}"
    idx = df[df["id"] == update.id].index[0]
    for field, value in update.dict(exclude_none=True).items():
        if field != "id":
            df.at[idx, field] = value
    save_tasks(df)
    return f"Task {update.id} updated"

def prioritize_tasks() -> List[str]:
    df = load_tasks()
    df["deadline"] = pd.to_datetime(df["deadline"], errors='coerce')
    df = df.dropna(subset=["deadline"]).sort_values("deadline")
    return df[["id", "title", "deadline"]].astype(str).values.tolist()

def summarize_tasks() -> str:
    df = load_tasks()
    counts = df["status"].value_counts().to_dict()
    return "Task Summary:\n" + "\n".join([f"{k}: {v}" for k, v in counts.items()])
