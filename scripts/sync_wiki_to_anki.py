import os
import json
import urllib.request
import re
import yaml

# 환경변수로 재정의 가능. 기본값은 Tailscale 내부망 headless-anki NodePort.
# 로컬 실행 시: ANKI_CONNECT_URL=http://172.20.208.1:8765 python sync_wiki_to_anki.py
# 서버 실행 시: ANKI_CONNECT_URL=http://100.82.121.40:30747 python sync_wiki_to_anki.py
ANKI_CONNECT_URL = os.environ.get("ANKI_CONNECT_URL", "http://100.82.121.40:30747")

# 환경변수로 재정의 가능. 기본값은 로컬 상대경로.
# 서버 실행 시: WIKI_ROOT=/home/ubuntu/llm-wiki/20_Wiki python sync_wiki_to_anki.py
_default_wiki_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../20_Wiki")
WIKI_ROOT = os.environ.get("WIKI_ROOT", _default_wiki_root)

def anki_request(action, **params):
    payload = {"action": action, "version": 6, "params": params}
    req = urllib.request.Request(ANKI_CONNECT_URL, json.dumps(payload).encode('utf-8'))
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            if res.get('error'):
                print(f"AnkiConnect Error [{action}]: {res['error']}")
            return res.get('result')
    except Exception as e:
        print(f"AnkiConnect Connection Error [{action}]: {e}")
        return None

def extract_frontmatter(content):
    match = re.search(r'^---(.*?)---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except:
            pass
    return {}

def extract_cards_from_content(content, default_deck, default_tags):
    cards = []
    
    # 1. 파일 전체 요약을 카드로 만드는 로직 (위키 타이틀 중심)
    # 첫 번째 H1이나 파일 제목을 프론트로, 그 아래 Summary를 백으로.
    summary_match = re.split(r'\n## ', re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL))
    if summary_match:
        summary = summary_match[0].strip()
        summary = re.sub(r'^# .*(\n|$)', '', summary).strip()
        if len(summary) >= 10:
            # 기본 문서 단위 카드 (Plugin의 기본 동작과 무관하지만 위키 특성상 유지)
            # 여기서는 문서 전체 요약 카드는 파일명 자체를 Front로 함.
            pass # 생략하거나 필요시 추가. 이번 수정에서는 플러그인 문법에 집중하기 위해 아래 inline 파싱을 추가함.

    # 2. Obsidian Flashcards 플러그인 문법 파싱 (:: 및 :::)
    # Front :: Back 형태
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # 정방향 카드 (::)
        if ' :: ' in line and not ' ::: ' in line:
            parts = line.split(' :: ', 1)
            if len(parts) == 2:
                cards.append({
                    "deckName": default_deck,
                    "modelName": "Basic",
                    "fields": {"Front": parts[0].strip(), "Back": parts[1].strip()},
                    "tags": default_tags
                })
        # 역방향/양방향 카드 (:::) -> Basic (and reversed card) 모델 필요 시 처리, 여기선 기본 카드로 2개 생성
        elif ' ::: ' in line:
            parts = line.split(' ::: ', 1)
            if len(parts) == 2:
                front, back = parts[0].strip(), parts[1].strip()
                cards.append({
                    "deckName": default_deck,
                    "modelName": "Basic",
                    "fields": {"Front": front, "Back": back},
                    "tags": default_tags
                })
                cards.append({
                    "deckName": default_deck,
                    "modelName": "Basic",
                    "fields": {"Front": back, "Back": front}, # Reversed
                    "tags": default_tags
                })
    return cards

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = extract_frontmatter(content)
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
        
    is_flashcard_file = False
    for t in tags:
        if 'anki' in str(t).lower() or 'card' in str(t).lower():
            is_flashcard_file = True
            
    if not is_flashcard_file:
        return []
    
    rel_dir = os.path.dirname(os.path.relpath(filepath, WIKI_ROOT))
    if rel_dir and rel_dir != ".":
        deck_name = rel_dir.replace(os.sep, "::")
    else:
        deck_name = "Default"
    final_tags = [t.replace(" ", "_") for t in tags] + ["wiki-auto-sync"]
    
    # Extract cards
    extracted = extract_cards_from_content(content, deck_name, final_tags)
    
    # 문서 자체를 하나의 카드로 취급 (문서 요약)
    summary_match = re.split(r'\n## ', re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL))
    if summary_match:
        summary = summary_match[0].strip()
        summary = re.sub(r'^# .*(\n|$)', '', summary).strip()
        title = meta.get("title", os.path.basename(filepath).replace(".md", ""))
        if len(summary) >= 10 and not any(c['fields']['Front'] == title for c in extracted):
             extracted.append({
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {"Front": title, "Back": summary.replace('\n', '<br>')},
                "tags": final_tags
            })
             
    return extracted

def main():
    print("Starting Wiki to Anki Sync (Plugin-Compatible Mode)...")
    decks = anki_request("deckNames")
    if decks is None:
        print("Failed to connect to AnkiConnect. Is Anki running?")
        return

    all_cards = []
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                cards = process_file(os.path.join(root, file))
                all_cards.extend(cards)

    print(f"Found {len(all_cards)} cards to sync.")

    decks_to_create = set(c["deckName"] for c in all_cards)
    for d in decks_to_create:
        if d not in decks:
            anki_request("createDeck", deck=d)

    success_count = 0
    for card in all_cards:
        # Check by Front field exactly
        front_query = card["fields"]["Front"].replace('"', '\\"')
        find_query = f'"deck:{card["deckName"]}" "Front:{front_query}"'
        existing = anki_request("findNotes", query=find_query)
        
        if existing:
            note_id = existing[0]
            anki_request("updateNoteFields", note={"id": note_id, "fields": card["fields"]})
            anki_request("updateNoteTags", note=note_id, tags=" ".join(card["tags"]))
        else:
            res = anki_request("addNote", note=card)
            if res:
                success_count += 1
                
    anki_request("sync")
    print(f"Sync complete! {success_count} new cards added.")

if __name__ == "__main__":
    main()
