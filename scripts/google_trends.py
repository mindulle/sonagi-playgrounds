import sqlite3
import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def clean_traffic(val):
    if not val:
        return 0
    val_str = str(val).replace('+', '').replace(',', '').strip()
    try:
        return int(val_str)
    except ValueError:
        return 0

def collect_and_save(db_path):
    logger.info("Fetching Google Trends (KR - Public RSS Feed)...")
    url = "https://trends.google.com/trending/rss?geo=KR"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.warning(f"Failed to fetch Google Trends RSS: Status {response.status_code}")
            return
            
        xml_data = response.text
        root = ET.fromstring(xml_data)
        
        ns = {'ht': 'https://trends.google.com/trending/rss'}
        items = root.findall('.//item')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        total_saved = 0
        for item in items:
            title_elem = item.find('title')
            traffic_elem = item.find('ht:approx_traffic', ns)
            
            if title_elem is not None and title_elem.text:
                keyword = title_elem.text.strip()
                traffic_text = traffic_elem.text if traffic_elem is not None else "0"
                score = clean_traffic(traffic_text)
                
                cursor.execute(
                    "INSERT INTO trends_log (source, keyword, score) VALUES (?, ?, ?)",
                    ('google_trends_kr', keyword, score)
                )
                total_saved += 1
                
        conn.commit()
        conn.close()
        logger.info(f"Saved {total_saved} Google Trends keywords from RSS.")
    except Exception as e:
        logger.error(f"Error fetching/parsing Google Trends RSS: {e}")
