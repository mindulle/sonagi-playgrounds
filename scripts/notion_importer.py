import csv
import os
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename).replace(" ", "_").strip()

def import_notion_csv(csv_path, limit=200):
    print(f"--- Importing Notion CSV: {csv_path} (Limit: {limit}) ---")
    if not os.path.exists(csv_path):
        print("Error: CSV file not found.")
        return

    dest_dir = "20_Wiki/_resources"
    concept_dir = "20_Wiki/_concepts"
    os.makedirs(dest_dir, exist_ok=True)
    
    # Get existing concepts for auto-linking
    existing_concepts = []
    if os.path.exists(concept_dir):
        existing_concepts = [f.replace(".md", "") for f in os.listdir(concept_dir) if f.endswith(".md")]

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                
                name = row.get('Name', 'Untitled').strip()
                if not name: continue
                
                tags = [t.strip() for t in row.get('Tags', '').split(',') if t.strip()]
                url = row.get('URL', '')
                area = row.get('Area/Resource', '')
                
                # Simple auto-linking logic
                links = []
                for concept in existing_concepts:
                    if concept.lower() in name.lower():
                        links.append(f"[[{concept}]]")
                
                safe_name = sanitize_filename(name)
                file_path = os.path.join(dest_dir, f"{safe_name}.md")
                
                content = f"""---
title: "{name}"
tags: {tags}
url: "{url}"
area: "{area}"
source: Notion Import
created: 2026-05-11
---

# {name}

## 요약
노션에서 마이그레이션된 리소스입니다.

## 원문 링크
- [바로가기]({url})

## 관련 개념 (Auto-linked)
{", ".join(links) if links else "발견된 관련 개념 없음"}

## 관련 영역
- {area}
"""
                with open(file_path, 'w', encoding='utf-8') as wf:
                    wf.write(content)
                
                count += 1
            
            print(f"Successfully imported {count} entries into {dest_dir}")
            
            # Log the action
            with open("00_System/log.md", 'a', encoding='utf-8') as log_f:
                log_f.write(f"| 2026-05-11 | IMPORT | Notion Data | ✅ Success | Imported {count} resources with auto-linking |\n")

    except Exception as e:
        print(f"Error during import: {e}")

if __name__ == "__main__":
    csv_path = "10_Sources/web/ExportBlock/Notes [PT] aa80d5301b504cf186ea176dd02ecec4.csv"
    import_notion_csv(csv_path)
