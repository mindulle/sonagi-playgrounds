import schedule
import time
import os
import logging
from dotenv import load_dotenv
import sqlite3

# Collectors
from collectors import google_trends, reddit_trends, naver_datalab

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# DB 초기화
DB_PATH = 'db/intelligence.db'
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 테이블 생성 (추후 SQLAlchemy ORM으로 고도화 가능)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trends_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            keyword TEXT,
            score INTEGER,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS naver_keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE,
            pc_msv INTEGER,
            mobile_msv INTEGER,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

def run_all_collectors():
    logger.info("Starting Daily Intelligence Collection...")
    
    # 1. Google Trends (무료, API 키 불필요)
    try:
        google_trends.collect_and_save(DB_PATH)
    except Exception as e:
        logger.error(f"Google Trends Error: {e}")

    # 2. Reddit Tech Trends (무료, Reddit API 필요)
    try:
        reddit_trends.collect_and_save(DB_PATH)
    except Exception as e:
        logger.error(f"Reddit Trends Error: {e}")

    # 3. Naver Datalab/SearchAds (무료, Naver API 필요)
    try:
        naver_datalab.collect_and_save(DB_PATH)
    except Exception as e:
        logger.error(f"Naver Datalab Error: {e}")
        
    logger.info("Collection Cycle Completed!")

if __name__ == "__main__":
    load_dotenv()
    init_db()
    
    # 컨테이너 켜지자마자 1회 즉시 실행
    run_all_collectors()
    
    # 매일 아침 8시에 실행
    schedule.every().day.at("08:00").do(run_all_collectors)
    
    logger.info("Scheduler started. Waiting for jobs...")
    while True:
        schedule.run_pending()
        time.sleep(60)
