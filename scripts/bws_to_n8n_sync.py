import os
import json
import subprocess
import requests
import sys

# === Configuration ===
BWS_ACCESS_TOKEN = os.environ.get("BWS_ACCESS_TOKEN")
N8N_API_KEY = os.environ.get("N8N_API_KEY")
N8N_URL = os.environ.get("N8N_URL", "http://100.113.113.72") 

SYNC_MAP = [
    {
        "bws_id": "9fd904ce-ef58-4859-b384-b308009a0dde", 
        "n8n_name": "Notion API - BWS Synced",
        "n8n_type": "notionApi",
        "data_mapping": {
            "apiKey": "VALUE" 
        }
    }
]

def get_bws_secret(secret_id):
    if not BWS_ACCESS_TOKEN:
        raise ValueError("BWS_ACCESS_TOKEN environment variable is not set.")
    
    cmd = ["bws", "secret", "get", secret_id, "-o", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        secret_data = json.loads(result.stdout)
        return secret_data.get("value")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching secret {secret_id} from BWS: {e.stderr}")
        return None

def get_n8n_credentials():
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Accept": "application/json"
    }
    url = f"{N8N_URL.rstrip('/')}/api/v1/credentials"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('data', [])

def create_or_update_n8n_credential(cred_id, name, cred_type, data):
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "type": cred_type,
        "data": data
    }
    
    if cred_id:
        url = f"{N8N_URL.rstrip('/')}/api/v1/credentials/{cred_id}"
        response = requests.put(url, headers=headers, json=payload)
        action = "Updated"
    else:
        url = f"{N8N_URL.rstrip('/')}/api/v1/credentials"
        response = requests.post(url, headers=headers, json=payload)
        action = "Created"
        
    response.raise_for_status()
    print(f"Successfully {action} credential: {name}")

def run_sync():
    if not N8N_API_KEY:
        print("ERROR: N8N_API_KEY environment variable is not set.")
        sys.exit(1)

    print("Fetching existing n8n credentials...")
    try:
        existing_creds = get_n8n_credentials()
    except Exception as e:
        print(f"Failed to connect to n8n API: {e}")
        sys.exit(1)

    cred_map = {cred['name']: cred['id'] for cred in existing_creds}
    success_count = 0

    for item in SYNC_MAP:
        print(f"\nProcessing sync for: {item['n8n_name']}")
        
        secret_value = get_bws_secret(item["bws_id"])
        if not secret_value:
            print(f"Skipping {item['n8n_name']} due to BWS fetch failure.")
            continue
            
        mapped_data = {}
        for k, v in item["data_mapping"].items():
            if v == "VALUE":
                mapped_data[k] = secret_value
            else:
                mapped_data[k] = v
                
        existing_id = cred_map.get(item["n8n_name"])
        
        try:
            create_or_update_n8n_credential(
                existing_id, 
                item["n8n_name"], 
                item["n8n_type"], 
                mapped_data
            )
            success_count += 1
        except Exception as e:
            print(f"Failed to sync {item['n8n_name']} to n8n: {e}")

    if success_count == len(SYNC_MAP):
        print("\nAll credentials synced successfully.")
    else:
        print(f"\nSynced {success_count} out of {len(SYNC_MAP)} credentials.")
        sys.exit(1)

if __name__ == "__main__":
    run_sync()