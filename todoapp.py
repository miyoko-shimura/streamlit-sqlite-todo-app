import streamlit as st
import pandas as pd

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = pd.DataFrame(columns=['Task', 'Status'])

def add_todo():
    if st.session_state.new_todo:
        new_todo = pd.DataFrame({'Task': [st.session_state.new_todo], 'Status': ['Pending']})
        st.session_state.todos = pd.concat([st.session_state.todos, new_todo], ignore_index=True)
        st.session_state.new_todo = ""

def remove_todo(task):
    st.session_state.todos = st.session_state.todos[st.session_state.todos.Task != task]

def toggle_status(task):
    index = st.session_state.todos.index[st.session_state.todos.Task == task].tolist()[0]
    current_status = st.session_state.todos.at[index, 'Status']
    new_status = 'Completed' if current_status == 'Pending' else 'Pending'
    st.session_state.todos.at[index, 'Status'] = new_status

# App title
st.title("📝 Simple To-Do App")

# Input for new todo
st.text_input("Add a new task", key="new_todo", on_change=add_todo)

# Display todos
for index, todo in st.session_state.todos.iterrows():
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.write(f"{'✅' if todo['Status'] == 'Completed' else '⏳'} {todo['Task']}")
    
    with col2:
        st.button(f"{'Undo' if todo['Status'] == 'Completed' else 'Complete'}", 
                  key=f"toggle_{index}", 
                  on_click=toggle_status, 
                  args=(todo['Task'],))
    
    with col3:
        st.button("Remove", key=f"remove_{index}", on_click=remove_todo, args=(todo['Task'],))

# Display dataframe (optional, for debugging)
st.write(st.session_state.todos)