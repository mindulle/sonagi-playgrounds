import os
import re
import yaml

WIKI_ROOT = "20_Wiki"
PERSONAL_DIR = "_personal"

def get_all_valid_pages():
    pages = {}
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                name = file[:-3]
                pages[name.lower()] = name # Store original name
    return pages

def check_visibility():
    """Checks for visibility metadata and enforces rules for _personal directory."""
    print("\n--- Scanning for Visibility & Privacy Rules ---")
    missing_visibility = []
    incorrect_visibility = []
    private_count = 0
    public_count = 0
    
    frontmatter_pattern = re.compile(r'^---(.*?)---', re.DOTALL)
    
    for root, dirs, files in os.walk(WIKI_ROOT):
        is_personal_folder = PERSONAL_DIR in root
        for file in files:
            if not file.endswith(".md"):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = frontmatter_pattern.search(content)
                
                visibility = None
                if match:
                    try:
                        data = yaml.safe_load(match.group(1))
                        if data and 'visibility' in data:
                            visibility = data['visibility']
                    except Exception:
                        pass
                
                # Rule 1: Files in _personal/ must be private
                if is_personal_folder:
                    if visibility != 'private':
                        incorrect_visibility.append((file_path, "Must be 'private' (inside _personal/)"))
                    private_count += 1
                elif visibility == 'private':
                    private_count += 1
                elif visibility == 'public':
                    public_count += 1
                else:
                    missing_visibility.append(file_path)
                    public_count += 1 # Default to public for now
    
    print(f"Private pages: {private_count}")
    print(f"Public pages: {public_count}")
    print(f"Pages missing 'visibility' tag: {len(missing_visibility)}")
    
    if incorrect_visibility:
        print("\nIncorrect Visibility Flags:")
        for path, reason in incorrect_visibility:
            print(f"  - {path}: {reason}")
            
    if missing_visibility:
        print("\nSample Pages Missing Visibility (First 5):")
        for path in missing_visibility[:5]:
            print(f"  - {path}")

def check_links():
    valid_pages_map = get_all_valid_pages()
    broken_links = []
    total_links = 0
    
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    print("\n--- Scanning for Broken Links (Case Insensitive) ---")
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                links = link_pattern.findall(content)
                for link in links:
                    total_links += 1
                    target = link.split('|')[0].strip()
                    if target.lower() not in valid_pages_map:
                        broken_links.append((file_path, target))
    
    print(f"Total links scanned: {total_links}")
    print(f"Broken links found: {len(broken_links)}")
    
    if broken_links:
        print("\nTop 10 Broken Links:")
        for source, target in broken_links[:10]:
            print(f"  - In {source}: [[{target}]]")

def check_duplicates():
    print("\n--- Scanning for Potential Duplicates (Case Insensitive) ---")
    pages = {}
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                name_lower = file[:-3].lower()
                if name_lower in pages:
                    pages[name_lower].append(os.path.join(root, file))
                else:
                    pages[name_lower] = [os.path.join(root, file)]
    
    duplicates = {k: v for k, v in pages.items() if len(v) > 1}
    print(f"Potential duplicate sets found: {len(duplicates)}")
    for name, paths in list(duplicates.items())[:5]:
        print(f"  - '{name}': {paths}")

def check_orphans():
    print("\n--- Scanning for Orphan Pages (Unlinked) ---")
    valid_pages_map = get_all_valid_pages()
    linked_pages = set()
    
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    # First pass: find all targets of all links
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                links = link_pattern.findall(content)
                for link in links:
                    target = link.split('|')[0].strip().lower()
                    linked_pages.add(target)
                    linked_pages.add(target.replace("-", " "))
                    linked_pages.add(target.replace(" ", "-"))
    
    orphans = []
    for page_lower, original_name in valid_pages_map.items():
        if page_lower not in linked_pages:
            orphans.append(original_name)
    
    print(f"Total orphan pages found: {len(orphans)}")
    if orphans:
        print("\nFirst 20 Orphan Pages:")
        for orphan in sorted(orphans)[:20]:
            print(f"  - {orphan}")

if __name__ == "__main__":
    check_visibility()
    check_links()
    check_duplicates()
    check_orphans()
