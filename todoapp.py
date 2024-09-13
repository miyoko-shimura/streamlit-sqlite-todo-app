import streamlit as st
import pandas as pd
import sqlite3

# Function to create a connection to the SQLite database
def get_connection():
    conn = sqlite3.connect('todos.db')
    return conn

# Function to add a new task to SQLite
def add_todo_to_db(task, category, priority):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO todos (task, category, priority, status)
        VALUES (?, ?, ?, 'Pending')
    ''', (task, category, priority))
    conn.commit()
    conn.close()

# Function to retrieve all tasks from SQLite
def get_todos_from_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM todos')
    todos = c.fetchall()
    conn.close()
    return todos

# Function to remove a task from SQLite
def remove_todo_from_db(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Function to toggle task status in SQLite
def toggle_task_status(task_id, current_status):
    new_status = 'Completed' if current_status == 'Pending' else 'Pending'
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE todos SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    conn.close()

# App title
st.title("📝 To-Do List Using Streamlit and SQLite")

# Input for new todo
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    new_task = st.text_input("Add a new task", key="new_todo")
with col2:
    category = st.selectbox("Category", ['Work', 'Personal', 'Shopping', 'Other'], key="category")
with col3:
    priority = st.selectbox("Priority", ['High', 'Medium', 'Low'], key="priority")

if st.button("Add Task"):
    if new_task:
        add_todo_to_db(new_task, category, priority)

# Filter options
st.sidebar.header("Filters")
filter_category = st.sidebar.multiselect("Filter by Category", ['Work', 'Personal', 'Shopping', 'Other'])
filter_priority = st.sidebar.multiselect("Filter by Priority", ['High', 'Medium', 'Low'])
filter_status = st.sidebar.multiselect("Filter by Status", ['Pending', 'Completed'])

# Retrieve all todos from the database
todos = get_todos_from_db()
todos_df = pd.DataFrame(todos, columns=['ID', 'Task', 'Category', 'Priority', 'Status'])

# Apply filters
if filter_category:
    todos_df = todos_df[todos_df['Category'].isin(filter_category)]
if filter_priority:
    todos_df = todos_df[todos_df['Priority'].isin(filter_priority)]
if filter_status:
    todos_df = todos_df[todos_df['Status'].isin(filter_status)]

# Display todos
for index, todo in todos_df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    
    with col1:
        st.write(f"{'✅' if todo['Status'] == 'Completed' else '⏳'} {todo['Task']}")
    
    with col2:
        st.write(f"🏷️ {todo['Category']}")
    
    with col3:
        priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        priority = todo['Priority']
        if priority in priority_color:
            st.write(f"{priority_color[priority]} {priority}")
        else:
            st.write(f"Unknown Priority: {priority}")
    
    with col4:
        st.button(f"{'Undo' if todo['Status'] == 'Completed' else 'Done'}",  # Changed "Complete" to "Done"
                  key=f"toggle_{index}", 
                  on_click=toggle_task_status, 
                  args=(todo['ID'], todo['Status']))
    
    with col5:
        st.button("Remove", key=f"remove_{index}", on_click=remove_todo_from_db, args=(todo['ID'],))

# Display dataframe (optional, for debugging)
if st.checkbox("Show Dataframe"):
    st.write(todos_df)
