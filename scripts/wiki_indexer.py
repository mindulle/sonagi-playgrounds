import os
import faiss
import numpy as np
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

WIKI_ROOT = "20_Wiki"
INDEX_PATH = "00_System/_executables/wiki_index.faiss"
METADATA_PATH = "00_System/_executables/wiki_metadata.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"

def chunk_markdown(content):
    """Simple chunking by headers or paragraph limits."""
    chunks = []
    lines = content.split('\n')
    current_chunk = ""
    
    for line in lines:
        if line.startswith('#'):
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
            if len(current_chunk) > 1000: # Max chunk size approx
                chunks.append(current_chunk.strip())
                current_chunk = ""
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return [c for c in chunks if len(c) > 20] # Filter very small chunks

def build_index():
    print(f"--- Building Index with {MODEL_NAME} ---")
    model = SentenceTransformer(MODEL_NAME)
    
    all_chunks = []
    metadata = []
    
    # 1. Collect and Chunk
    files_to_process = []
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                files_to_process.append(os.path.join(root, file))
    
    print(f"Found {len(files_to_process)} files. Chunking...")
    for file_path in tqdm(files_to_process):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = chunk_markdown(content)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append({
                "path": file_path,
                "chunk_idx": i,
                "content": chunk
            })
    
    # 2. Embed
    print(f"Generating embeddings for {len(all_chunks)} chunks...")
    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)
    
    # 3. Save FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    
    print(f"Index built and saved to {INDEX_PATH}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    build_index()
