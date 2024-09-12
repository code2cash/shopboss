import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def get_tasks():
    # In a real application, this data would come from a database
    return pd.DataFrame({
        "Task": [
            "Send weekly newsletter",
            "Update Facebook ad campaign",
            "Analyze SEO performance",
            "Create content for blog post",
            "Review PPC keywords"
        ],
        "Due Date": [
            datetime.now() + timedelta(days=i) for i in range(1, 6)
        ],
        "Status": ["Pending", "In Progress", "Pending", "In Progress", "Pending"]
    })

def render_task_management():
    st.title("Task Management")

    tasks = get_tasks()

    # Display tasks
    st.subheader("Upcoming Tasks")
    st.dataframe(tasks)

    # Add new task
    st.subheader("Add New Task")
    new_task = st.text_input("Task Description")
    new_due_date = st.date_input("Due Date")
    new_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

    if st.button("Add Task"):
        # In a real application, this would add the task to a database
        st.success(f"Task '{new_task}' added successfully!")

    # Update task status
    st.subheader("Update Task Status")
    task_to_update = st.selectbox("Select Task", tasks["Task"])
    new_status = st.selectbox("New Status", ["Pending", "In Progress", "Completed"])

    if st.button("Update Status"):
        # In a real application, this would update the task status in the database
        st.success(f"Status for task '{task_to_update}' updated to {new_status}")

    # Add some explanatory text
    st.markdown("""
    Use this task management system to keep track of your marketing activities:
    - View upcoming tasks and their current status
    - Add new tasks with descriptions, due dates, and initial status
    - Update the status of existing tasks as you make progress

    Keeping your tasks organized will help you stay on top of your marketing efforts and ensure nothing falls through the cracks.
    """)
