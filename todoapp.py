import streamlit as st
import sqlite3
import os

# Display current working directory
st.write("Current working directory:", os.getcwd())

# Function to create a connection to the SQLite database
def get_connection():
    try:
        conn = sqlite3.connect('todos.db', check_same_thread=False)
        st.success("Successfully connected to the database!")
        return conn
    except Exception as e:
        st.error(f"Failed to connect to the database: {e}")
        return None

# Function to create table
def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        ''')
        conn.commit()
        st.success("Table 'todos' created successfully!")
    except Exception as e:
        st.error(f"Error creating table: {e}")

# Function to add a task
def add_task(conn, task):
    try:
        c = conn.cursor()
        c.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        st.success(f"Task '{task}' added successfully!")
    except Exception as e:
        st.error(f"Error adding task: {e}")

# Function to get all tasks
def get_tasks(conn):
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM todos')
        tasks = c.fetchall()
        return tasks
    except Exception as e:
        st.error(f"Error retrieving tasks: {e}")
        return []

# Main app
st.title("Minimal SQLite To-Do App")

# Create connection
conn = get_connection()

if conn is not None:
    # Create table
    create_table(conn)

    # Add task
    new_task = st.text_input("Enter a new task")
    if st.button("Add Task") and new_task:
        add_task(conn, new_task)

    # Display tasks
    tasks = get_tasks(conn)
    if tasks:
        st.write("Tasks:")
        for task in tasks:
            st.write(f"- {task[1]}")
    else:
        st.write("No tasks found.")

    # Close connection
    conn.close()
