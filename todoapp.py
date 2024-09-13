import streamlit as st
import pandas as pd
import sqlite3

# Ensure the database is created in the correct directory
import os
st.write("Current working directory:", os.getcwd())

# Function to create a connection to the SQLite database
def get_connection():
    try:
        conn = sqlite3.connect('todos.db')
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# Create table if it doesn't exist
def create_table():
    conn = get_connection()
    if conn is None:
        return
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            category TEXT,
            priority TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call create_table() at the start of the app
create_table()

# Function to add a new task to SQLite
def add_todo_to_db(task, category, priority):
    conn = get_connection()
    if conn is None:
        return
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
    if conn is None:
        return []
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM todos')
        todos = c.fetchall()
        conn.close()
        return todos
    except Exception as e:
        st.error(f"Error retrieving tasks from the database: {e}")
        return []

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

# Retrieve all todos from the database
todos = get_todos_from_db()
todos_df = pd.DataFrame(todos, columns=['ID', 'Task', 'Category', 'Priority', 'Status'])

# Display todos
st.write(todos_df)

# Debugging: Optional to see table structure and errors
if st.checkbox("Show Dataframe"):
    st.write(todos_df)
