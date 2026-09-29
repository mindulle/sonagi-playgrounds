import os
import re

WIKI_ROOT = "20_Wiki"

def get_all_valid_pages():
    pages = {} # Lowercase target -> Actual Filename
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                name = file[:-3]
                pages[name.lower()] = name
                pages[name.lower().replace("-", " ")] = name
                pages[name.lower().replace(" ", "-")] = name
    return pages

def heal_links():
    valid_pages_map = get_all_valid_pages()
    no_space_map = {k.replace(" ", "").replace("-", ""): v for k, v in valid_pages_map.items()}
    
    total_healed = 0
    total_unlinked = 0
    
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    
    print("--- Healing Broken Links ---")
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            links = link_pattern.findall(content)
            
            changed = False
            for link in links:
                parts = link.split('|')
                target = parts[0].strip()
                label = parts[1].strip() if len(parts) > 1 else None
                
                target_lower = target.lower()
                
                found = False
                actual_name = None
                
                # 1. Direct match (case mismatch)
                if target_lower in valid_pages_map:
                    actual_name = valid_pages_map[target_lower]
                    if target != actual_name:
                        found = True
                
                # 2. Fuzzy match
                if not found:
                    fuzzy_targets = [
                        re.sub(r'\s+', ' ', target_lower),
                        re.sub(r'[\\/:?"<>|]', "", target_lower).strip(),
                        target_lower.replace("/", ""),
                        target_lower.replace(" & ", "  "),
                        target_lower.replace(" / ", "  "),
                        target_lower.strip("?").strip("."),
                        re.sub(r'\s+(roadmap|track)$', '', target_lower),
                        target_lower.rstrip('s')
                    ]
                    for ft in fuzzy_targets:
                        if ft in valid_pages_map:
                            actual_name = valid_pages_map[ft]
                            found = True
                            break
                    
                    if not found:
                        no_space_ft = target_lower.replace(" ", "").replace("-", "")
                        if no_space_ft in no_space_map:
                            actual_name = no_space_map[no_space_ft]
                            found = True
                
                # Apply healing
                if found and actual_name:
                    if label:
                        replacement = f"[[{actual_name}|{label}]]"
                    else:
                        replacement = f"[[{actual_name}|{target}]]"
                    
                    old_link = f"[[{link}]]"
                    new_content = new_content.replace(old_link, replacement)
                    changed = True
                    total_healed += 1
                else:
                    # 3. Noise removal
                    noise_patterns = [
                        "other resources", "detailed version", "interactive version",
                        "more roadmaps at", "roadmap.sh", "relevant tracks", "visit the following"
                    ]
                    if any(p in target_lower for p in noise_patterns) or len(target) > 50:
                        old_link = f"[[{link}]]"
                        new_content = new_content.replace(old_link, target)
                        changed = True
                        total_unlinked += 1

            if changed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Healed/Cleaned links in {file_path}")

    print(f"\nTotal links healed: {total_healed}")
    print(f"Total noise unlinked: {total_unlinked}")

if __name__ == "__main__":
    heal_links()
