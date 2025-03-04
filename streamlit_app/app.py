import streamlit as st
import requests
import os

# FastAPI Backend URL

UPLOAD_SINGLE_URL = "http://127.0.0.1:8000/files/upload/"
UPLOAD_MULTIPLE_URL = "http://127.0.0.1:8000/files/upload-multiple/"
QUERY_API_URL = "http://localhost:8000/query/ask"


ALLOWED_EXTENSIONS = ["json", "pdf", "txt", "jpg", "jpeg", "png", "docx", "csv", "xls", "xlsx"]


st.set_page_config(page_title="Ultimate RAG", layout="wide",  page_icon="🤖")

st.title("🤖 Ultimate RAG")

st.sidebar.title("🔝 Ultimate RAG")


# Initialize session state for selections & history
if "embedding_model" not in st.session_state:
    st.session_state["embedding_model"] = "huggingface"
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = "chroma"
if "generator" not in st.session_state:
    st.session_state["generator"] = "gemini"
if "query_history" not in st.session_state:
    st.session_state["query_history"] = []  # Stores past queries & responses


# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
st.session_state["embedding_model"] = st.sidebar.selectbox("Select Embedding Model", ["huggingface", "cohere", "openai"])
st.session_state["vector_store"] = st.sidebar.selectbox("Select Vector Store", ["chroma", "faiss", "qdrant"])
st.session_state["generator"] = st.sidebar.selectbox("Select Generator", ["gemini", "groq", "openai"])

st.sidebar.write(f"🛠️ **Embedding:** {st.session_state['embedding_model']}")
st.sidebar.write(f"📚 **Vector Store:** {st.session_state['vector_store']}")
st.sidebar.write(f"🤖 **Generator:** {st.session_state['generator']}")

# Tabs for different functionalities
tab1, tab2 = st.tabs(["🔍 Ask Questions", "📂 Upload Documents"])

# ✅ **Tab 1: Ask Questions & Retrieve Answers**
with tab1:
    st.header("🔍 Ask Question")

    question = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        response = requests.post(
            QUERY_API_URL,
            json={  # ✅ Include additional parameters
                "query": question,
                "retriever_name": st.session_state.get("vector_store", "default_retriever"),
                "generator_name": st.session_state.get("generator", "default_generator"),
                "embedding_name": st.session_state.get("embedding_model", "default_embedding"),
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            answer = response.json()["response"]
            st.write(f"**AI Response:** {answer}")
        else:
            st.error("❌ Error retrieving answer.")



# ✅ **Tab 2: Upload & Embed Documents**
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


