import os
import time
import hmac
import hashlib
import base64
import sqlite3
import logging
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.searchad.naver.com"

def get_signature(timestamp, method, uri, secret_key):
    message = f"{timestamp}.{method}.{uri}"
    hash_obj = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    return base64.b64encode(hash_obj.digest()).decode()

def get_headers(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = get_signature(timestamp, method, uri, secret_key)
    return {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Timestamp': timestamp,
        'X-API-KEY': api_key,
        'X-Customer': str(customer_id),
        'X-Signature': signature
    }

def clean_search_count(val):
    if not val:
        return 0
    val_str = str(val).strip()
    if '<' in val_str:
        return 0
    try:
        return int(val_str.replace(',', ''))
    except ValueError:
        return 0

def fetch_keyword_msv(keyword, api_key, secret_key, customer_id):
    method = "GET"
    uri = f"/keywordstool?hintKeywords={keyword}&showDetail=1"
    
    try:
        headers = get_headers(method, uri, api_key, secret_key, customer_id)
        response = requests.get(BASE_URL + uri, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.warning(f"Naver API Error: Status {response.status_code} for keyword '{keyword}'")
            return None
            
        data = response.json()
        keyword_list = data.get("keywordList", [])
        
        for kw in keyword_list:
            if kw.get("relKeyword") == keyword:
                pc_count = clean_search_count(kw.get("monthlyPcQcCnt"))
                mobile_count = clean_search_count(kw.get("monthlyMobileQcCnt"))
                return pc_count, mobile_count
                
        return None
    except Exception as e:
        logger.error(f"Error fetching Naver MSV for '{keyword}': {e}")
        return None

def collect_and_save(db_path):
    api_key = os.getenv('NAVER_API_KEY')
    secret_key = os.getenv('NAVER_SECRET_KEY')
    customer_id = os.getenv('NAVER_CUSTOMER_ID')
    
    if not api_key or not secret_key or not customer_id:
        logger.warning("Naver Search Ads API credentials missing. Skipping Naver MSV collection.")
        return
        
    logger.info("Starting Naver Search Ads (MSV) collection...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT keyword 
            FROM trends_log 
            WHERE keyword NOT IN (SELECT keyword FROM naver_keywords)
            LIMIT 50
        """)
        keywords = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        cursor.execute("SELECT DISTINCT keyword FROM trends_log LIMIT 50")
        keywords = [row[0] for row in cursor.fetchall()]
        
    if not keywords:
        logger.info("No new keywords found for Naver MSV lookup.")
        conn.close()
        return
        
    logger.info(f"Found {len(keywords)} keywords to query Naver MSV.")
    
    total_saved = 0
    for kw in keywords:
        time.sleep(0.1)
        res = fetch_keyword_msv(kw, api_key, secret_key, customer_id)
        if res is not None:
            pc_msv, mobile_msv = res
            cursor.execute("""
                INSERT OR REPLACE INTO naver_keywords (keyword, pc_msv, mobile_msv)
                VALUES (?, ?, ?)
            """, (kw, pc_msv, mobile_msv))
            total_saved += 1
            logger.info(f"Saved MSV for '{kw}': PC={pc_msv}, Mobile={mobile_msv}")
            
    conn.commit()
    conn.close()
    logger.info(f"Completed Naver MSV Collection. Saved {total_saved} keywords.")
