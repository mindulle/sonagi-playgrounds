import os
import sqlite3
import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def collect_and_save(db_path):
    # RSS 피드를 사용하므로 API 키가 필요 없습니다.
    # 단, 차단 우회를 위해 브라우저 형태의 User-Agent를 사용합니다.
    user_agent = os.getenv(
        'REDDIT_USER_AGENT', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    logger.info("Fetching Reddit Tech Trends (Atom/RSS Feed)...")
    
    subreddits = ['macsetups', 'gadgets', 'battlestations']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    total_saved = 0
    headers = {'User-Agent': user_agent}
    
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}.rss"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch r/{sub} RSS: Status {response.status_code}")
                continue
                
            xml_data = response.text
            root = ET.fromstring(xml_data)
            
            # Atom 네임스페이스 매핑
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)
            
            # 최대 5개의 top 트렌드 저장
            for entry in entries[:5]:
                title_elem = entry.find('atom:title', ns)
                if title_elem is not None and title_elem.text:
                    keyword = title_elem.text.strip()
                    score = 100
                    cursor.execute(
                        "INSERT INTO trends_log (source, keyword, score) VALUES (?, ?, ?)",
                        (f'reddit_{sub}', keyword, score)
                    )
                    total_saved += 1
        except Exception as e:
            logger.error(f"Error fetching/parsing r/{sub} RSS: {e}")
            
    conn.commit()
    conn.close()
    logger.info(f"Saved {total_saved} Reddit trends from RSS.")
