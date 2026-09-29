import os
import json
import datetime
import glob

# Category Mapping for roadmap.sh topics
CATEGORY_MAP = {
    # AI / Data Science -> Computing
    "ai-agents": "Computing",
    "ai-engineer": "Computing",
    "ai-data-scientist": "Computing",
    "ai-product-builder": "Computing",
    "ai-red-teaming": "Computing",
    "machine-learning": "Computing",
    "mlops": "Computing",
    "data-engineer": "Computing",
    "data-analyst": "Computing",
    "prompt-engineering": "Computing",
    
    # Core CS & Infra -> Computing
    "computer-science": "Computing",
    "datastructures-and-algorithms": "Computing",
    "system-design": "Computing",
    "software-architect": "Computing",
    "software-design-architecture": "Computing",
    "devops": "Computing",
    "devops-beginner": "Computing",
    "devsecops": "Computing",
    "cyber-security": "Computing",
    "linux": "Computing",
    "docker": "Computing",
    "kubernetes": "Computing",
    "aws": "Computing",
    "cloudflare": "Computing",
    "terraform": "Computing",
    "git-github": "Computing",
    "git-github-beginner": "Computing",
    "sql": "Computing",
    "postgresql-dba": "Computing",
    "mongodb": "Computing",
    "redis": "Computing",
    "elasticsearch": "Computing",
    "api-design": "Computing",
    "graphql": "Computing",
    "shell-bash": "Computing",
    
    # Programming Languages & Frameworks -> Develop
    "javascript": "Develop",
    "typescript": "Develop",
    "python": "Develop",
    "java": "Develop",
    "golang": "Develop",
    "rust": "Develop",
    "cpp": "Develop",
    "php": "Develop",
    "ruby": "Develop",
    "kotlin": "Develop",
    "scala": "Develop",
    "nodejs": "Develop",
    "react": "Develop",
    "react-native": "Develop",
    "angular": "Develop",
    "vue": "Develop",
    "nextjs": "Develop",
    "django": "Develop",
    "laravel": "Develop",
    "spring-boot": "Develop",
    "ruby-on-rails": "Develop",
    "flutter": "Develop",
    "android": "Develop",
    "ios": "Develop",
    "swift-ui": "Develop",
    "aspnet-core": "Develop",
    "css": "Develop",
    "html": "Develop",
    "frontend": "Develop",
    "frontend-beginner": "Develop",
    "backend": "Develop",
    "backend-beginner": "Develop",
    "full-stack": "Develop",
    
    # Design -> Design
    "design-system": "Design",
    "ux-design": "Design",
    
    # Business -> Business
    "product-manager": "Business",
    "engineering-manager": "Business",
    "bi-analyst": "Business",
    
    # Writing -> Writing
    "technical-writer": "Writing",
    
    # Others
    "wordpress": "Develop",
    "leetcode": "Computing",
    "vibe-coding": "Computing",
    "claude-code": "Computing",
    "openclaw": "Computing"
}

NOISE_PATTERNS = [
    "roadmap.sh", "detailed version", "Related Roadmaps", 
    "Have a look at", "Visit the following", "Related Tracks",
    "Find the detailed", "relevant tracks", "Check out the",
    "Subscribe to", "Follow us", "Contribute to"
]

def ingest_roadmap(topic, category=None):
    if not category:
        category = CATEGORY_MAP.get(topic, "Computing")
    
    print(f"--- Ingesting: {topic} -> {category} ---")
    
    source_base = f"10_Sources/roadmaps/{topic}"
    wiki_dest = f"20_Wiki/{category}/{topic}.md"
    log_path = "00_System/log.md"
    
    if not os.path.exists(source_base):
        print(f"Error: Source {source_base} not found.")
        return False

    # 1. Read nodes from JSON
    json_path = os.path.join(source_base, f"{topic}.json")
    nodes_to_atomize = []
    title = topic.replace("-", " ").capitalize()
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                nodes = data.get('nodes', [])
                if not nodes and 'json' in data:
                    nodes = data['json'].get('nodes', [])
                
                for node in nodes:
                    name = node.get('name')
                    if not name and 'data' in node:
                        name = node['data'].get('label')
                    
                    if not name or name.strip() == "" or node.get('type') in ['section', 'vertical', 'horizontal', 'roadmap']:
                        continue
                    
                    if any(p.lower() in name.lower() for p in NOISE_PATTERNS):
                        continue
                    
                    nodes_to_atomize.append({
                        "name": name,
                        "description": node.get('description', '')
                    })
            except Exception as e:
                print(f"Error parsing {json_path}: {e}")
                return False

    # 2. Generate Main Topic Document with WikiLinks
    today = datetime.date.today().isoformat()
    concept_links = "\n".join([f"- [[{n['name']}]]" for n in nodes_to_atomize])
    
    content = f"""---
title: {title}
tags: [roadmap, {topic}]
created: {today}
updated: {today}
source: {source_base}
---

# {title}

## 요약
{topic}에 관한 로드맵 지식입니다. 각 세부 개념은 개별 문서로 관리됩니다.

## 주요 개념 (Atomic Notes)
{concept_links}

## 관련 로드맵
- [[ai-agents]]
- [[ai-engineer]]
- [[python]]
- [[javascript]]
"""

    # 3. Write to Wiki
    os.makedirs(os.path.dirname(wiki_dest), exist_ok=True)
    with open(wiki_dest, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 4. Log
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"| {today} | INGEST | [[{topic}]] | ✅ Success | Categorized as {category} ({len(nodes_to_atomize)} nodes) |\n")
    
    return True

def batch_ingest():
    source_dir = "10_Sources/roadmaps"
    topics = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    success_count = 0
    for topic in topics:
        if ingest_roadmap(topic):
            success_count += 1
    
    print(f"\nBatch Ingestion Complete: {success_count}/{len(topics)} topics processed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 wiki_maintainer.py [topic-name|--batch]")
    elif sys.argv[1] == "--batch":
        batch_ingest()
    else:
        ingest_roadmap(sys.argv[1])
