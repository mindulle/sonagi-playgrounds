import os
import re

def update_index():
    index_path = "00_System/index.md"
    wiki_root = "20_Wiki"
    
    topics = []
    
    # Walk Wiki to find files with the roadmap tag
    for root, dirs, files in os.walk(wiki_root):
        if "_concepts" in root or "_commons" in root or "_people" in root or "Archives" in root:
            continue
            
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # Read the first few lines to check for tags
                        content = f.read(500)
                        
                        # Simple check for roadmap tag in frontmatter
                        if "tags: [" in content and "roadmap" in content:
                            topic = file[:-3]
                            # Try to extract a specific source if it exists, otherwise use a placeholder
                            source_match = re.search(r"source:\s*(.+)", content)
                            source_path = source_match.group(1).strip() if source_match else "Wiki Source"
                            topics.append((topic, source_path))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    pass
    
    # Remove duplicates (if a topic exists in multiple categories)
    unique_topics = {}
    for topic, source in topics:
        if topic not in unique_topics:
            unique_topics[topic] = source
    
    sorted_topics = sorted(unique_topics.items())
    
    table_header = "| Topic | Status | Source | Wiki Link |\n| :--- | :--- | :--- | :--- |\n"
    table_rows = ""
    for topic, source_path in sorted_topics:
        wiki_link = f"[[{topic}]]"
        source_display = f"[Source]({source_path})" if source_path.startswith("10_Sources") else source_path
        table_rows += f"| {topic} | ✅ Ready | {source_display} | {wiki_link} |\n"
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_table = table_header + table_rows
    # Replace the existing table
    pattern = r"\| Topic \| Status \| Source \| Wiki Link \|\n\| :--- \| :--- \| :--- \| :--- \|\n(.*?)((?=\n\n)|(?=\Z))"
    updated_content = re.sub(pattern, new_table, content, flags=re.DOTALL)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"Updated {index_path} with {len(sorted_topics)} unique roadmap topics based on tags.")

if __name__ == "__main__":
    update_index()
