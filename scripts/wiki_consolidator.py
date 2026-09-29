import os
import re

WIKI_ROOT = "20_Wiki"

def consolidate():
    pages = {}
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                name_lower = file[:-3].lower()
                if name_lower == "index":
                    continue
                path = os.path.join(root, file)
                if name_lower in pages:
                    pages[name_lower].append(path)
                else:
                    pages[name_lower] = [path]
    
    duplicates = {k: v for k, v in pages.items() if len(v) > 1}
    print(f"--- Consolidating {len(duplicates)} duplicate sets ---")
    
    total_merged = 0
    for name, paths in duplicates.items():
        # Heuristic to pick the "Primary" file:
        # 1. Prefer path not in _concepts or _commons
        # 2. Prefer shorter path depth
        # 3. Prefer larger file size
        
        paths.sort(key=lambda p: (
            1 if "_concepts" in p or "_commons" in p else 0,
            len(p.split(os.sep)),
            -os.path.getsize(p)
        ))
        
        primary = paths[0]
        others = paths[1:]
        
        for secondary in others:
            print(f"  Merging {secondary} into {primary}")
            
            with open(secondary, 'r', encoding='utf-8') as f:
                secondary_content = f.read()
            
            # Remove YAML frontmatter
            secondary_content = re.sub(r'^---.*?---\n', '', secondary_content, flags=re.DOTALL)
            
            with open(primary, 'a', encoding='utf-8') as f:
                f.write(f"\n\n---\n## 상세 내용 (Merged from {secondary})\n")
                f.write(secondary_content)
            
            os.remove(secondary)
            total_merged += 1
            
    print(f"\nTotal merged: {total_merged}")

if __name__ == "__main__":
    consolidate()
