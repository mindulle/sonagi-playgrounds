import sys
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder

INDEX_PATH = "00_System/_executables/wiki_index.faiss"
METADATA_PATH = "00_System/_executables/wiki_metadata.pkl"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

def search(query, top_k=10):
    # 1. Load Resources
    embed_model = SentenceTransformer(EMBED_MODEL_NAME)
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, 'rb') as f:
        metadata = pickle.dump = pickle.load(f)
    
    # 2. Vector Search (Initial Retrieval)
    query_vector = embed_model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vector.astype('float32'), top_k)
    
    initial_results = [metadata[idx] for idx in indices[0] if idx != -1]
    
    # 3. Reranking
    print(f"\n--- Reranking results for: '{query}' ---")
    rerank_model = CrossEncoder(RERANK_MODEL_NAME)
    
    # Prepare pairs for reranking: (query, chunk_content)
    pairs = [(query, res['content']) for res in initial_results]
    scores = rerank_model.predict(pairs)
    
    # Sort by rerank scores
    for i, res in enumerate(initial_results):
        res['rerank_score'] = float(scores[i])
    
    final_results = sorted(initial_results, key=lambda x: x['rerank_score'], reverse=True)
    
    # 4. Output
    for i, res in enumerate(final_results[:5]): # Show top 5
        print(f"\n[{i+1}] Score: {res['rerank_score']:.4f} | Path: {res['path']}")
        print(f"--- Content Snippet ---")
        print(res['content'][:300] + "...")
        print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wiki_retriever.py \"your query\"")
    else:
        search(sys.argv[1])
