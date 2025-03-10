# app.py

import streamlit as st
import requests
import os

import json
from pathlib import Path



# FastAPI Backend URL
API_BASE_URL = "http://127.0.0.1:8000"
# End points
UPLOAD_SINGLE_URL = f"{API_BASE_URL}/files/upload/"
UPLOAD_MULTIPLE_URL = f"{API_BASE_URL}/files/upload-multiple/"
QUERY_API_URL = f"{API_BASE_URL}/query/ask"


ALLOWED_EXTENSIONS = ["json", "pdf", "txt", "jpg", "jpeg", "png", "docx", "csv", "xls", "xlsx"]


st.set_page_config(page_title="Ultimate RAG", layout="wide",  page_icon="🤖")

st.title("🤖 Career Advisory Service")

st.sidebar.title(" 🎓 Career Advisory AI")

st.sidebar.markdown("**🔝 AI-powered job mentoring**\n\nHelping you find the best career paths! 🚀")


# Tabs for different functionalities
tab1, tab2 = st.tabs(["🔍 Ask Questions", "📂 Upload Documents"])

# Tab 1: Ask Questions & Retrieve Answers
with tab1:
    st.header("🔍 Ask Question")

    question = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        response = requests.post(
            QUERY_API_URL,
            json={  
                "query": question
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            answer = response.json()["response"]
            context = response.json()["retrieved_context"]

            st.write(f"**AI Response:** {answer} \n\n\n")

            st.markdown("---")  # Adds a horizontal line


            with st.expander("Please click here to view context"):
                st.write(context)
        else:
            st.error("❌ Error retrieving answer.")



# Tab 2: Upload & Embed Documents
with tab2:

    st.header("📂 Upload Documents") 
    # File uploader (supports multiple files)
    uploaded_files = st.file_uploader("Choose file(s)", accept_multiple_files=True, type=ALLOWED_EXTENSIONS)

    if uploaded_files:
        if len(uploaded_files) == 1:
            # Single file upload
            file = uploaded_files[0]
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(UPLOAD_SINGLE_URL, files=files)
        else:
            # Multiple file upload
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            response = requests.post(UPLOAD_MULTIPLE_URL, files=files)

        # Handle API response
        if response.status_code == 200:
            st.success("File(s) uploaded successfully!")
            st.json(response.json())  # Display response
        else:
            st.error(f"Upload failed: {response.json()['detail']}")


