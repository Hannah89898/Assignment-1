"""
Home.py - Legal Document Q&A Application
"""
import streamlit as st
from utilities.chroma_db import query_chromadb_collection, add_document_chunk_to_chroma_collection
from utilities.ai_inference import gpt5_mini_inference
from utilities.documents import process_pdf
from utilities.api_key import render_sidebar

COLLECTION_NAME = "legal_case_collection"

# API key setup
api_key, update_button = render_sidebar()
if update_button:
    st.session_state.openai_api_key = api_key
api_key = st.session_state.get("openai_api_key")

# Header
st.title("⚖️ Legal Document Q&A")
st.info("Upload a legal document, then ask questions about it.")

# File upload and processing
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
        with st.spinner("Processing..."):
            nodes = process_pdf(uploaded_file)
            for i, node in enumerate(nodes):
                add_document_chunk_to_chroma_collection(COLLECTION_NAME, node.text, document_id=f"{uploaded_file.name}_chunk_{i}")
            st.session_state.processed_file = uploaded_file.name
            st.session_state.num_chunks = len(nodes)
        st.success(f"✅ Processed into {st.session_state.num_chunks} chunks")
    else:
        st.success(f"✅ {uploaded_file.name} loaded ({st.session_state.num_chunks} chunks)")

# Query section
if api_key and uploaded_file:
    st.markdown("---")
    query = st.text_input("Ask a question:", placeholder="What is this case about?")
    
    if st.button("Search"):
        if query:
            with st.spinner("Searching..."):
                results = query_chromadb_collection(COLLECTION_NAME, query, n_results=3)
            
            if results:
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                history = "\n".join(st.session_state.chat_history[-3:])
                context = "\n\n".join(results)
                prompt = f"{history}\n\nQuestion: {query}\n\nContext:\n{context}"
                
                try:
                    answer = gpt5_mini_inference(
                        "You are a legal assistant. Answer based on the provided context.",
                        prompt,
                        api_key
                    )
                    st.session_state.chat_history.append(f"Q: {query}\nA: {answer}")
                    st.markdown("### Answer")
                    st.write(answer)
                    
                    with st.expander("View source chunks"):
                        for i, chunk in enumerate(results, 1):
                            st.text_area(f"Chunk {i}", chunk, height=100, disabled=True)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("No relevant chunks found.")
        else:
            st.warning("Please enter a question")
elif not api_key:
    st.warning("Enter your API key in the sidebar and click 'Update API Key'")
elif not uploaded_file:
    st.info("Upload a PDF to begin")