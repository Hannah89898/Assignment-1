"""
documents.py - Process PDF and chunk using LlamaIndex
"""
import PyPDF2
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core import Document

def process_pdf(pdf_file):
    """
    Process a PDF file and return chunks using LlamaIndex SentenceWindowNodeParser
    
    Args:
        pdf_file: File path (string) or file object
    
    Returns:
        List of nodes (chunks) from LlamaIndex
    """
    # Read PDF
    if isinstance(pdf_file, str):
        # If it's a file path
        with open(pdf_file, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    else:
        # If it's a file object (from Streamlit uploader)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    
    # Create LlamaIndex Document
    document = Document(text=text)
    
    # Initialize SentenceWindowNodeParser
    parser = SentenceWindowNodeParser.from_defaults(
        window_size=5,  # sentences on each side
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )
    
    # Parse into nodes (chunks)
    nodes = parser.get_nodes_from_documents([document])
    
    return nodes