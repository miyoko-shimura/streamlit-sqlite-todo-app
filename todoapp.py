import streamlit as st
import pandas as pd

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = pd.DataFrame(columns=['Task', 'Category', 'Priority', 'Status'])

# Categories and Priorities
categories = ['仕事', '個人', '買い物', 'その他']
priorities = ['高', '中', '低']

def add_todo():
    if st.session_state.new_todo:
        new_todo = pd.DataFrame({
            'Task': [st.session_state.new_todo],
            'Category': [st.session_state.category],
            'Priority': [st.session_state.priority],
            'Status': ['未完了']
        })
        st.session_state.todos = pd.concat([st.session_state.todos, new_todo], ignore_index=True)
        st.session_state.new_todo = ""

def remove_todo(task):
    st.session_state.todos = st.session_state.todos[st.session_state.todos.Task != task]

def toggle_status(task):
    index = st.session_state.todos.index[st.session_state.todos.Task == task].tolist()[0]
    current_status = st.session_state.todos.at[index, 'Status']
    new_status = '完了' if current_status == '未完了' else '未完了'
    st.session_state.todos.at[index, 'Status'] = new_status

# App title
st.title("📝 カテゴリー別・優先度別 TO DOリスト")

# Input for new todo
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.text_input("新しいタスクを追加", key="new_todo")
with col2:
    st.selectbox("カテゴリー", categories, key="category")
with col3:
    st.selectbox("優先度", priorities, key="priority")

st.button("タスクを追加", on_click=add_todo)

# Filter options
st.sidebar.header("フィルター")
filter_category = st.sidebar.multiselect("カテゴリーで絞り込み", categories)
filter_priority = st.sidebar.multiselect("優先度で絞り込み", priorities)
filter_status = st.sidebar.multiselect("状態で絞り込み", ['未完了', '完了'])

# Apply filters
filtered_todos = st.session_state.todos
if filter_category:
    filtered_todos = filtered_todos[filtered_todos['Category'].isin(filter_category)]
if filter_priority:
    filtered_todos = filtered_todos[filtered_todos['Priority'].isin(filter_priority)]
if filter_status:
    filtered_todos = filtered_todos[filtered_todos['Status'].isin(filter_status)]

# Display todos
for index, todo in filtered_todos.iterrows():
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    
    with col1:
        st.write(f"{'✅' if todo['Status'] == '完了' else '⏳'} {todo['Task']}")
    
    with col2:
        st.write(f"🏷️ {todo['Category']}")
    
    with col3:
        priority_color = {'高': '🔴', '中': '🟡', '低': '🟢'}
        st.write(f"{priority_color[todo['Priority']]} {todo['Priority']}")
    
    with col4:
        st.button(f"{'元に戻す' if todo['Status'] == '完了' else '完了'}", 
                  key=f"toggle_{index}", 
                  on_click=toggle_status, 
                  args=(todo['Task'],))
    
    with col5:
        st.button("削除", key=f"remove_{index}", on_click=remove_todo, args=(todo['Task'],))

# Display dataframe (optional, for debugging)
if st.checkbox("データフレームを表示"):
    st.write(st.session_state.todos)