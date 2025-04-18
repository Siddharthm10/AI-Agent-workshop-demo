# test_tools.py

from tools import *
from datetime import datetime

def test_add():
    task = Task(
        id=999,
        title="Test Task",
        description="This is a test",
        deadline="2025-04-30",
        status="pending"
    )
    print(add_task(task))

def test_update():
    update = UpdateTask(
        id=999,
        description="Updated description",
        status="in progress"
    )
    print(update_task(update))

def test_remove():
    print(remove_task(999))

def test_prioritize():
    print(prioritize_tasks())

def test_summary():
    print(summarize_tasks())

if __name__ == "__main__":
    test_add()
    test_update()
    test_prioritize()
    test_summary()
    test_remove()
