import os
import argparse
import datetime

def push_artifact(title, content, category="_resources/_inbox"):
    today = datetime.date.today().isoformat()
    
    # Clean title for filename
    filename = title.replace(" ", "_").replace("/", "-") + ".md"
    
    # Path construction
    base_dir = "20_Wiki"
    dest_dir = os.path.join(base_dir, category)
    dest_path = os.path.join(dest_dir, filename)
    
    # Create directory
    os.makedirs(dest_dir, exist_ok=True)
    
    # Frontmatter
    frontmatter = f"""---
title: {title}
tags: [agent-artifact, {category.replace('/', '-')}]
created: {today}
updated: {today}
---

# {title}

{content}
"""
    
    # Write to Wiki
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        
    print(f"Artifact pushed to: {dest_path}")
    return dest_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push agent artifact to Wiki")
    parser.add_argument("--title", required=True, help="Artifact title")
    parser.add_argument("--content", required=True, help="Artifact content")
    parser.add_argument("--category", default="_resources/_inbox", help="Wiki category path")
    
    args = parser.parse_args()
    
    push_artifact(args.title, args.content, args.category)
