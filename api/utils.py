import os
import pdfplumber
import chromadb
import logging
from sentence_transformers import SentenceTransformer
from django.core.files.storage import default_storage
from api.models import Document
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache the SentenceTransformer model
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def process_document(document_id):
    start_time = time.time()
    logger.info("Starting document processing for ID: %s", document_id)

    document = Document.objects.get(id=document_id)
    file_path = default_storage.path(document.file.name)
    
    # Extract text from PDF using pdfplumber
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text() or ""
                text += f"\n[Page {page_num}] {page_text}"
        logger.info("PDF parsing completed in %.2f seconds", time.time() - start_time)
    except Exception as e:
        logger.error("PDF parsing failed: %s", str(e))
        raise

    # Chunk the text (smaller chunks for faster processing)
    chunk_size = 500
    max_chunks = 50  # Limit to 50 chunks to cap processing time
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)][:max_chunks]
    chunk_metadata = [{"file_name": document.file_name, "page": i + 1} for i in range(len(chunks))]
    
    # Generate embeddings
    embedding_start = time.time()
    embeddings = MODEL.encode(chunks, convert_to_tensor=False)
    logger.info("Embedding generation completed in %.2f seconds", time.time() - embedding_start)
    
    # Store in ChromaDB
    client = chromadb.HttpClient(host='localhost', port=8000)
    collection = client.get_or_create_collection(name="knowledge_base")
    
    # Check if collection has documents and delete if not empty
    chromadb_start = time.time()
    if collection.count() > 0:
        existing_ids = collection.get()['ids']
        collection.delete(ids=existing_ids)
        logger.info("Cleared existing ChromaDB data")
    
    # Add new embeddings
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=chunk_metadata,
        ids=[f"{document.file_name}_page_{i+1}" for i in range(len(chunks))]
    )
    logger.info("ChromaDB storage completed in %.2f seconds", time.time() - chromadb_start)
    
    total_time = time.time() - start_time
    logger.info("Document processing completed in %.2f seconds", total_time)
    if total_time > 30:
        logger.warning("Processing took longer than 30 seconds")

def query_knowledge_base(question):
    question_embedding = MODEL.encode([question], convert_to_tensor=False).tolist()
    
    client = chromadb.HttpClient(host='localhost', port=8000)
    collection = client.get_collection(name="knowledge_base")
    
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )
    
    return [
        {"text": doc, "metadata": meta}
        for doc, meta in zip(results['documents'][0], results['metadatas'][0])
    ]