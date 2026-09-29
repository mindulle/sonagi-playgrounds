#!/usr/bin/env python3
import os
import json
import time
import mimetypes
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import boto3
import requests
from botocore.client import Config
from botocore.exceptions import ClientError

# --- 설정 (Configuration) ---
TARGET_TAG = "deploy"
EAGLE_LIBRARY_PATH = os.environ.get("EAGLE_LIBRARY_PATH", "/data/eagle.library/images")
STATE_FILE = "bridge_state.json"

# Discord 알림 설정 (웹훅 URL)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")

# Minio 정보
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "https://cdn.sonagi.space")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME", "assets")

if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY:
    raise ValueError("MINIO_ACCESS_KEY and MINIO_SECRET_KEY environment variables must be set.")

ROUTING_MAP = {
    "academic": "academic",
    "business": "business",
    "projects": "projects",
    "design": "design"
}
DEFAULT_CATEGORY = "resources"

# --- S3 클라이언트 셋업 ---
s3_client = boto3.client('s3',
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

def ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError as e:
        status_code = e.response.get('ResponseMetadata', {}).get('HTTPStatusCode')
        if status_code == 404:
            print(f"[Minio] '{BUCKET_NAME}' 버킷이 없습니다. 새로 생성합니다...", flush=True)
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            
            # 퍼블릭 읽기 권한(Policy) 부여
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
                    }
                ]
            }
            s3_client.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(policy))
            print(f"[Minio] '{BUCKET_NAME}' 버킷 퍼블릭 권한 설정 완료.", flush=True)
        else:
            print(f"[Minio] 버킷 체크 에러: {e}", flush=True)

# --- 로컬 상태 (중복 방지) ---
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

processed_assets = load_state()
state_lock = threading.Lock()

# --- 실제 S3 업로드 로직 ---
def real_minio_upload(local_file, cdn_path):
    print(f"   [Minio S3 Uploading] '{local_file.name}' 👉 s3://{BUCKET_NAME}/{cdn_path}", flush=True)
    
    # 파일 확장자에 따른 Content-Type 자동 유추
    content_type, _ = mimetypes.guess_type(str(local_file))
    if content_type is None:
        content_type = 'application/octet-stream'

    s3_client.upload_file(
        str(local_file), 
        BUCKET_NAME, 
        cdn_path,
        ExtraArgs={'ContentType': content_type}
    )
    # Minio는 버킷 이름이 URL 경로에 포함됩니다
    return f"{MINIO_ENDPOINT}/{BUCKET_NAME}/{cdn_path}"

# --- 디스코드 알림 로직 ---
def send_discord_notification(asset_id, category, final_url):
    if not DISCORD_WEBHOOK_URL:
        print("   [Discord] 웹훅 URL이 설정되지 않아 알림을 건너뜁니다.", flush=True)
        return
        
    payload = {
        "content": None,
        "embeds": [
            {
                "title": "✅ 새로운 에셋 CDN 배포 완료",
                "description": f"Eagle Gallery에서 승인된 에셋이 Minio CDN으로 배포되었습니다.",
                "color": 5814783,
                "fields": [
                    {"name": "분류 (Category)", "value": f"`{category}`", "inline": True},
                    {"name": "에셋 ID", "value": f"`{asset_id}`", "inline": True},
                    {"name": "CDN URL", "value": f"{final_url}"}
                ],
                "image": {"url": final_url} # 디스코드에서 이미지가 바로 보이도록 설정
            }
        ]
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        print("   [Discord] 알림 발송 완료!", flush=True)
    except Exception as e:
        print(f"   [Discord Error] 알림 발송 실패: {e}", flush=True)

# --- 폴더 감지 로직 ---
class EagleEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith("metadata.json"):
            self.process_metadata(event.src_path)

    def process_metadata(self, json_path):
        try:
            time.sleep(0.2)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tags = data.get("tags", [])
            asset_id = data.get("id")
            
            with state_lock:
                if asset_id in processed_assets or TARGET_TAG not in tags:
                    return
                processed_assets[asset_id] = "PENDING"
                
            asset_name = data.get("name")
            asset_ext = data.get("ext")
            
            parent_dir = Path(json_path).parent
            image_file = parent_dir / f"{asset_name}.{asset_ext}"
            
            # 이미지 파일이 실제로 존재하는지 확인
            if not image_file.exists():
                print(f"[Error] Image file not found: {image_file}", flush=True)
                with state_lock:
                    processed_assets.pop(asset_id, None)
                return
            
            category = DEFAULT_CATEGORY
            for tag in tags:
                if tag in ROUTING_MAP:
                    category = ROUTING_MAP[tag]
                    break
                    
            cdn_path = f"{category}/{asset_id}.{asset_ext}"
            
            print("\n[🎯 TARGET DETECTED]", flush=True)
            print(f"- Asset ID: {asset_id} (Tags: {tags})", flush=True)
            
            # 실제 업로드 수행
            final_url = real_minio_upload(image_file, cdn_path)
            
            print(f"- ✅ Upload Complete! URL: {final_url}", flush=True)
            
            # 디스코드 알림 발송
            send_discord_notification(asset_id, category, final_url)
            
            with state_lock:
                processed_assets[asset_id] = final_url
                save_state(processed_assets)
                
        except json.JSONDecodeError as e:
            print(f"[Warning] JSON decode error (file might still be writing): {e}", flush=True)
        except Exception as e:
            print(f"[Error] reading {json_path}: {e}", flush=True)

if __name__ == "__main__":
    ensure_bucket_exists()
    
    path = EAGLE_LIBRARY_PATH
    event_handler = EagleEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    print(f"👀 Watching '{path}' for '{TARGET_TAG}' tags...", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
