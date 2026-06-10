import streamlit as st
import requests

# Configure the page styling
st.set_page_config(page_title="Local PDF AI Companion", page_icon="📄", layout="centered")

st.title("📄 Chat with Your Local PDF")
st.write("Upload any document to process it securely on your machine using Qdrant & Llama 3.")

# Define backend API URLs
UPLOAD_URL = "http://127.0.0.1:8000/upload-pdf"
CHAT_URL = "http://127.0.0.1:8000/chat"

# Sidebar for file upload mechanics
with st.sidebar:
    st.header("📥 Document Ingestion")
    uploaded_file = st.file_uploader("Drag and drop your PDF here", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("🚀 Process & Index PDF", use_container_width=True):
            with st.spinner("Parsing document layers & calculating vectors..."):
                try:
                    # Package the file to send over HTTP to your FastAPI backend
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(UPLOAD_URL, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("status") == "success":
                            st.success(f"✅ {result.get('message')}")
                        else:
                            st.error(f"❌ Error: {result.get('message')}")
                    else:
                        st.error(f"❌ Server connection failed (Status: {response.status_code})")
                except Exception as e:
                    st.error(f"🔌 Could not connect to backend server: {e}")

# Initialize user interface chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat elements
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input Field Area
if user_query := st.chat_input("Ask something about your document..."):
    # Render user query bubble
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Query backend API pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching local vector database points..."):
            try:
                payload = {"question": user_query}
                response = requests.post(CHAT_URL, json=payload)
                
                if response.status_code == 200:
                    ai_response = response.json().get("response", "No answer generated.")
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error("⚠️ Failed to parse response text from local LLM engine.")
            except Exception as e:
                st.error(f"🔌 Connection drop error: {e}")
