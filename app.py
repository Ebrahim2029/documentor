import streamlit as st
from rag import Rag
# Streamlit UI
st.title("RAG-based Question Answering System")

st.write("Upload a PDF file, and then ask questions based on its content.")

rag = Rag()

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    rag.feed("uploaded_file.pdf")
    st.success("PDF has been processed and context is ready for question answering.")

# Text input for question
question = st.text_input("Ask a question:")
if st.button("Get Answer"):
    if uploaded_file is None:
        st.warning("Please upload a PDF file first.")
    elif question:
        answer = rag.ask(question)
        st.write("Answer:", answer)

# Clear context button
if st.button("Clear Context"):
    rag.clear()
    st.success("Context has been cleared.")