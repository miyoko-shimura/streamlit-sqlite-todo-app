import streamlit as st

# Title of the app
st.title("Simple To-Do App")

# Initialize the session state to store tasks
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Function to add a new task
def add_task():
    task = st.text_input("Enter a task", key="new_task")
    if st.button("Add Task"):
        if task != "":
            st.session_state['tasks'].append(task)
            st.experimental_rerun()  # Refresh the app

# Function to remove a task
def remove_task(index):
    st.session_state['tasks'].pop(index)
    st.experimental_rerun()  # Refresh the app

# Adding a new task
add_task()

# Display the task list
st.write("### Task List")
if len(st.session_state['tasks']) == 0:
    st.write("No tasks available")
else:
    for i, task in enumerate(st.session_state['tasks']):
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f"{i + 1}. {task}")
        if col2.button("Remove", key=f"remove_{i}"):
            remove_task(i)
