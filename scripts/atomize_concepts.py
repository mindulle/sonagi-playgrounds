import os
import re
import shutil

WIKI_ROOT = "/home/mindulle/projects/llm-wiki/20_Wiki"

def normalize_name(name):
    # Lowercase and remove all non-alphanumeric (including Korean)
    return re.sub(r"[^a-z0-9ㄱ-ㅎㅏ-ㅣ가-힣]", "", name.lower())

def consolidate_chunk(limit=10):
    pages = {}
    if not os.path.exists(WIKI_ROOT):
        print(f"Error: {WIKI_ROOT} not found.")
        return

    for root, dirs, files in os.walk(WIKI_ROOT):
        # Skip large reference folders or system folders
        if "Develop/References" in root or "00_System" in root:
            continue
            
        for file in files:
            if file.endswith(".md"):
                name = file[:-3]
                if name.lower() == "index":
                    continue
                path = os.path.join(root, file)
                norm = normalize_name(name)
                if not norm:
                    continue
                if norm in pages:
                    pages[norm].append(path)
                else:
                    pages[norm] = [path]
    
    duplicates = {k: v for k, v in pages.items() if len(v) > 1}
    print(f"--- Found {len(duplicates)} duplicate sets. Processing chunk of {limit} ---")
    
    total_merged = 0
    processed_sets = 0
    
    # Sort keys for deterministic behavior across runs
    sorted_keys = sorted(duplicates.keys())
    
    for norm in sorted_keys:
        if processed_sets >= limit:
            break
            
        paths = duplicates[norm]
        
        # Primary selection heuristic:
        # 1. Prefer files in a "Concepts" (plural) folder
        # 2. Prefer files NOT in _concepts (singular) or _commons (legacy)
        # 3. Prefer shorter path depth
        # 4. Prefer larger file size
        
        def score(p):
            s = 0
            if "/Concepts/" in p: s -= 100
            if "/_concepts/" in p or "/_commons/" in p: s += 50
            s += len(p.split(os.sep))
            try:
                s -= os.path.getsize(p) / 1024 # Minus size in KB
            except:
                pass
            return s
            
        paths.sort(key=score)
        
        primary = paths[0]
        others = paths[1:]
        
        print(f"Set [{norm}]: Primary={primary}")
        
        try:
            with open(primary, 'r', encoding='utf-8') as f:
                primary_content = f.read()
                primary_content_no_fm = re.sub(r'^---.*?---\n', '', primary_content, flags=re.DOTALL).strip()
            
            for secondary in others:
                print(f"  Merging {secondary} -> {primary}")
                with open(secondary, 'r', encoding='utf-8') as f:
                    secondary_content = f.read()
                
                secondary_content_no_fm = re.sub(r'^---.*?---\n', '', secondary_content, flags=re.DOTALL).strip()
                
                # Check if content is substantially different
                if secondary_content_no_fm and secondary_content_no_fm not in primary_content_no_fm:
                    with open(primary, 'a', encoding='utf-8') as f:
                        f.write(f"\n\n---\n## 상세 내용 (Merged from {secondary})\n")
                        f.write(secondary_content_no_fm)
                else:
                    print(f"    (Content is identical or already included, skipping append)")
                
                os.remove(secondary)
                total_merged += 1
        except Exception as e:
            print(f"  Error processing set {norm}: {e}")
        
        processed_sets += 1
            
    print(f"\nTotal merged in this chunk: {total_merged}")

if __name__ == "__main__":
    consolidate_chunk(10)
