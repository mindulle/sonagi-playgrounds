import faiss
import pickle
import numpy as np
from collections import defaultdict

# Path Configuration
INDEX_PATH = "00_System/_executables/wiki_index.faiss"
METADATA_PATH = "00_System/_executables/wiki_metadata.pkl"

# Threshold for similarity (Distance in L2 index, lower is more similar)
# Since we use IndexFlatL2, distance 0 is identical. 
# 0.1 to 0.5 is usually very high semantic overlap.
THRESHOLD = 0.3 

def find_semantic_duplicates():
    print("--- Loading Index and Metadata ---")
    try:
        index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, 'rb') as f:
            metadata = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Index or Metadata not found. Please run wiki_indexer.py first.")
        return

    n = index.ntotal
    if n == 0:
        print("Index is empty.")
        return

    print(f"Analyzing {n} chunks for semantic overlap...")
    
    # Reconstruct all vectors from the index
    # Note: IndexFlatL2 allows reconstruction
    vectors = np.zeros((n, index.d), dtype='float32')
    for i in range(n):
        vectors[i] = index.reconstruct(i)

    # Search each vector against the whole index
    # k=2 because the closest match will be the vector itself
    D, I = index.search(vectors, k=2)

    results = []
    seen_pairs = set()

    for i in range(n):
        # I[i][0] is the current vector i
        # I[i][1] is the nearest neighbor
        dist = D[i][1]
        neighbor_idx = I[i][1]

        if dist < THRESHOLD:
            path_a = metadata[i]['path']
            path_b = metadata[neighbor_idx]['path']

            # Ignore if it's the same file
            if path_a == path_b:
                continue

            # Avoid reporting (A, B) and (B, A) twice
            pair = tuple(sorted((i, neighbor_idx)))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                results.append({
                    "dist": float(dist),
                    "file_a": path_a,
                    "file_b": path_b,
                    "content_a": metadata[i]['content'][:100].replace('\n', ' '),
                    "content_b": metadata[neighbor_idx]['content'][:100].replace('\n', ' ')
                })

    # Group by file pairs to report most redundant files
    file_overlap = defaultdict(int)
    for res in results:
        pair = tuple(sorted((res['file_a'], res['file_b'])))
        file_overlap[pair] += 1

    print("\n=== Semantic Redundancy Report ===")
    if not file_overlap:
        print("No significant semantic overlaps found.")
    else:
        print(f"Found {len(results)} highly similar chunk pairs across {len(file_overlap)} file pairs.\n")
        
        # Sort by number of overlapping chunks
        sorted_overlap = sorted(file_overlap.items(), key=lambda x: x[1], reverse=True)
        
        for (f1, f2), count in sorted_overlap:
            print(f"[{count} chunks overlap] ")
            print(f"  A: {f1}")
            print(f"  B: {f2}")
            print("-" * 30)

    print("\nNote: Low distance (0.0 to 0.3) indicates near-identical meaning.")
    print("Consider merging these files or using [[WikiLinks]] to connect them.")

if __name__ == "__main__":
    find_semantic_duplicates()
