import streamlit as st
import pandas as pd
import sqlite3
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the database is created in the correct directory
st.write("Current working directory:", os.getcwd())

# Function to create a connection to the SQLite database
def get_connection():
    try:
        conn = sqlite3.connect('todos.db', check_same_thread=False)
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        st.error(f"Failed to connect to the database: {e}")
        return None

# Create table if it doesn't exist
def create_table():
    conn = get_connection()
    if conn is None:
        return
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        logger.info("Table 'todos' created successfully or already exists.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        st.error(f"Error creating table: {e}")
    finally:
        conn.close()

# Function to add a new task to SQLite
def add_todo_to_db(task, category, priority):
    conn = get_connection()
    if conn is None:
        return
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO todos (task, category, priority, status)
            VALUES (?, ?, ?, 'Pending')
        ''', (task, category, priority))
        conn.commit()
        st.success("Task added successfully!")
        logger.info(f"Task added: {task}")
    except Exception as e:
        logger.error(f"Error adding task to the database: {e}")
        st.error(f"Error adding task to the database: {e}")
    finally:
        conn.close()

# Function to retrieve all tasks from SQLite
def get_todos_from_db():
    conn = get_connection()
    if conn is None:
        return []
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM todos')
        todos = c.fetchall()
        logger.info(f"Retrieved {len(todos)} tasks from the database.")
        return todos
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            logger.error("Table 'todos' does not exist. Attempting to create it.")
            create_table()
            return []
        else:
            logger.error(f"Error retrieving tasks from the database: {e}")
            st.error(f"Error retrieving tasks from the database: {e}")
            return []
    except Exception as e:
        logger.error(f"Unexpected error retrieving tasks from the database: {e}")
        st.error(f"Unexpected error retrieving tasks from the database: {e}")
        return []
    finally:
        conn.close()

# Call create_table() at the start of the app
create_table()

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
    else:
        st.warning("Please enter a task before adding.")

# Retrieve all todos from the database
todos = get_todos_from_db()
todos_df = pd.DataFrame(todos, columns=['ID', 'Task', 'Category', 'Priority', 'Status'])

# Display todos
if not todos_df.empty:
    st.write(todos_df)
else:
    st.info("No tasks found. Add a task to get started!")

# Debugging: Optional to see table structure and errors
if st.checkbox("Show Dataframe"):
    st.write(todos_df)

# Add this at the end of your script to see any unhandled exceptions
st.exception = Exception
