import streamlit as st
import pandas as pd
import datetime
from datetime import datetime as dt

# Initialize session state for storing data
if 'notes_df' not in st.session_state:
    st.session_state.notes_df = pd.DataFrame(columns=['Title', 'Description', 'Category', 'Deadline', 'Reward', 'Created', 'Completed'])

# App title
st.title("Personal Productivity Notepad")

# Sidebar for category selection and new note
st.sidebar.header("Add New Note")
categories = ["Future Goals", "Daily Goals", "Startup Ideas", "Money Management", "Research Topics"]
title = st.sidebar.text_input("Title")
description = st.sidebar.text_area("Description")
category = st.sidebar.selectbox("Category", categories)
deadline = st.sidebar.date_input("Deadline", min_value=dt.today())
reward = st.sidebar.text_input("Reward (Optional)")
add_button = st.sidebar.button("Add Note")

# Function to add a new note
def add_note(title, description, category, deadline, reward):
    new_note = pd.DataFrame({
        'Title': [title],
        'Description': [description],
        'Category': [category],
        'Deadline': [deadline],
        'Reward': [reward],
        'Created': [dt.now()],
        'Completed': [False]
    })
    st.session_state.notes_df = pd.concat([st.session_state.notes_df, new_note], ignore_index=True)

# Add note when button is clicked
if add_button and title and description:
    add_note(title, description, category, deadline, reward)
    st.sidebar.success("Note added successfully!")

# Display notes by category
st.header("Your Notes")
for cat in categories:
    st.subheader(cat)
    cat_notes = st.session_state.notes_df[st.session_state.notes_df['Category'] == cat]
    
    if not cat_notes.empty:
        for idx, row in cat_notes.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{row['Title']}** (Created: {row['Created'].strftime('%Y-%m-%d %H:%M')})")
                st.write(f"Description: {row['Description']}")
                st.write(f"Deadline: {row['Deadline']}")
                if row['Reward']:
                    st.write(f"Reward: {row['Reward']}")
            with col2:
                completed = st.checkbox("Completed", value=row['Completed'], key=f"check_{idx}")
                if completed != row['Completed']:
                    st.session_state.notes_df.at[idx, 'Completed'] = completed
                if st.button("Delete", key=f"delete_{idx}"):
                    st.session_state.notes_df = st.session_state.notes_df.drop(idx).reset_index(drop=True)
                    st.experimental_rerun()
    else:
        st.write("No notes in this category.")

# Display summary
st.header("Summary")
st.write(f"Total Notes: {len(st.session_state.notes_df)}")
st.write(f"Completed Notes: {len(st.session_state.notes_df[st.session_state.notes_df['Completed']])}")
st.write(f"Pending Notes: {len(st.session_state.notes_df[~st.session_state.notes_df['Completed']])}")

# Download data as CSV
if not st.session_state.notes_df.empty:
    csv = st.session_state.notes_df.to_csv(index=False)
    st.download_button(
        label="Download Notes as CSV",
        data=csv,
        file_name="notes.csv",
        mime="text/csv"
    )