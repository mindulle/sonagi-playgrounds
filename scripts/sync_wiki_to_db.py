import os, yaml, psycopg2, re, glob, time
from psycopg2.extras import execute_values
from datetime import datetime

WIKI_ROOT = "20_Wiki"

def extract_frontmatter(content):
    frontmatter_pattern = re.compile(r'^---(.*?)---', re.DOTALL)
    match = frontmatter_pattern.search(content)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except Exception:
            pass
    return {}

def extract_summary(content):
    lines = content.split('\n')
    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or stripped.startswith('#') or not stripped:
            continue
        return stripped[:300] + ('...' if len(stripped) > 300 else '')
    return ""

def get_links(content):
    link_pattern = re.compile(r'\[\[(.*?)\]\]')
    links = link_pattern.findall(content)
    return [link.split('|')[0].strip() for link in links]

def sync_to_db():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(host=os.environ.get("DB_HOST", "mindullemonitor.tailb95307.ts.net"), port=os.environ.get("DB_PORT", "30543"), dbname=os.environ.get("DB_NAME", "wiki_data"), user=os.environ.get("DB_USER", "wiki_etl_user"), password=os.environ.get("DB_PASSWORD", "EtlWiki_2026_!X"))
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS wiki_pages (
        filename TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        folder TEXT,
        visibility TEXT,
        word_count INTEGER,
        summary TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS wiki_tags (
        page_filename TEXT REFERENCES wiki_pages(filename) ON DELETE CASCADE,
        tag TEXT NOT NULL,
        PRIMARY KEY (page_filename, tag)
    );
    CREATE TABLE IF NOT EXISTS wiki_links (
        source_filename TEXT REFERENCES wiki_pages(filename) ON DELETE CASCADE,
        target_title TEXT NOT NULL,
        PRIMARY KEY (source_filename, target_title)
    );
    GRANT SELECT ON wiki_pages, wiki_tags, wiki_links TO metabase_ro_user;
    """)

    pages_dict = {}
    tags_set = set()
    links_set = set()

    md_files = []
    for root, _, files in os.walk(WIKI_ROOT):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    
    print(f"Parsing {len(md_files)} files...")
    now = datetime.now()
    
    for filepath in md_files:
        filename = os.path.basename(filepath)[:-3]
        if filename in pages_dict:
            continue # Skip duplicates
            
        folder = os.path.relpath(os.path.dirname(filepath), WIKI_ROOT)
        if folder == ".": folder = ""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        meta = extract_frontmatter(content)
        title = meta.get('title', filename) if isinstance(meta.get('title'), str) else filename
        visibility = meta.get('visibility', 'public')
        
        tags = meta.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        
        summary = extract_summary(content)
        word_count = len(content.split())
        
        pages_dict[filename] = (filename, title, folder, visibility, word_count, summary, now)
        
        if tags and isinstance(tags, list):
            for tag in tags:
                if isinstance(tag, str):
                    tags_set.add((filename, tag))
        
        links = get_links(content)
        for target in links:
            links_set.add((filename, target))

    pages_data = list(pages_dict.values())
    tags_data = list(tags_set)
    links_data = list(links_set)

    print(f"Bulk Insert: {len(pages_data)} pages, {len(tags_data)} tags, {len(links_data)} links...")

    pages_query = """
        INSERT INTO wiki_pages (filename, title, folder, visibility, word_count, summary, updated_at)
        VALUES %s
        ON CONFLICT (filename) DO UPDATE SET
            title = EXCLUDED.title,
            folder = EXCLUDED.folder,
            visibility = EXCLUDED.visibility,
            word_count = EXCLUDED.word_count,
            summary = EXCLUDED.summary,
            updated_at = EXCLUDED.updated_at;
    """
    execute_values(cur, pages_query, pages_data, page_size=10000)

    cur.execute("TRUNCATE TABLE wiki_tags, wiki_links;")

    tags_query = "INSERT INTO wiki_tags (page_filename, tag) VALUES %s ON CONFLICT DO NOTHING"
    execute_values(cur, tags_query, tags_data, page_size=10000)

    links_query = "INSERT INTO wiki_links (source_filename, target_title) VALUES %s ON CONFLICT DO NOTHING"
    execute_values(cur, links_query, links_data, page_size=10000)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Complete!")

if __name__ == "__main__":
    sync_to_db()
