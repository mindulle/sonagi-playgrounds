import os
import json
import time
import subprocess
import requests
import shutil
from pathlib import Path

# Paths
WORKSPACE_ROOT = Path("/mnt/c/Users/hoofo/Documents/projects/llm-wiki")
COMFY_WORKSPACE = Path("/home/mindulle/comfyui-workspace")
COMFY_RUN_SCRIPT = COMFY_WORKSPACE / "run.sh"
COMFY_OUTPUT_DIR = COMFY_WORKSPACE / "output"

QUEUE_DIR = WORKSPACE_ROOT / "20_Wiki/Design/_queue"
DONE_DIR = QUEUE_DIR / "done"
FAILED_DIR = QUEUE_DIR / "failed"
ASSETS_DIR = WORKSPACE_ROOT / "10_Sources/assets/generated"

COMFY_API_URL = "http://127.0.0.1:8188"

def is_comfy_running():
    try:
        response = requests.get(f"{COMFY_API_URL}/history", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_comfy():
    if is_comfy_running():
        print("ComfyUI is already running.")
        return True
    
    print(f"Starting ComfyUI via {COMFY_RUN_SCRIPT}...")
    # Run in background
    subprocess.Popen([str(COMFY_RUN_SCRIPT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    
    # Wait for it to start
    max_retries = 30
    for i in range(max_retries):
        if is_comfy_running():
            print("ComfyUI started successfully.")
            return True
        time.sleep(2)
        print(f"Waiting for ComfyUI... ({i+1}/{max_retries})")
    
    print("Failed to start ComfyUI.")
    return False

def queue_prompt(workflow_json):
    p = {"prompt": workflow_json}
    data = json.dumps(p).encode('utf-8')
    try:
        response = requests.post(f"{COMFY_API_URL}/prompt", data=data)
        if response.status_code != 200:
            print(f"Error: ComfyUI returned status {response.status_code}")
            print(f"Response: {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error queuing prompt: {e}")
        return None

def process_queue():
    # Ensure directories exist
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    queue_files = list(QUEUE_DIR.glob("*.json"))
    if not queue_files:
        print("Queue is empty.")
        return

    if not start_comfy():
        return

    for json_file in queue_files:
        print(f"Processing {json_file.name}...")
        try:
            with open(json_file, 'r') as f:
                workflow = json.load(f)
            
            result = queue_prompt(workflow)
            if result and "prompt_id" in result:
                print(f"Successfully queued: {result['prompt_id']}")
                # Move to done
                shutil.move(str(json_file), str(DONE_DIR / json_file.name))
            else:
                print(f"Failed to queue {json_file.name}")
                shutil.move(str(json_file), str(FAILED_DIR / json_file.name))
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            shutil.move(str(json_file), str(FAILED_DIR / json_file.name))

    print("Queue processing finished.")
    # We leave ComfyUI running for now, user can shut it down manually or we could add a shutdown method.

def sync_outputs(prefix_filter=None):
    """
    Move files from ComfyUI output to Wiki assets.
    If prefix_filter is provided, only move files starting with that prefix.
    """
    if not COMFY_OUTPUT_DIR.exists():
        return

    # If no filter is provided, we still want to avoid system files or accidental clutter
    new_files = list(COMFY_OUTPUT_DIR.glob("*"))
    for f in new_files:
        if f.is_file() and f.name != "_output_images_will_be_put_here":
            # If a filter is active, skip files that don't match
            if prefix_filter and not f.name.startswith(prefix_filter):
                continue

            target_path = ASSETS_DIR / f.name
            
            # Avoid overwriting by adding a timestamp if a file with the same name exists
            if target_path.exists():
                timestamp = int(time.time())
                target_path = ASSETS_DIR / f"{f.stem}_{timestamp}{f.suffix}"

            print(f"Moving {f.name} to {target_path.name}...")
            shutil.move(str(f), str(target_path))
            
            # Create a simple markdown reference in the wiki
            note_path = WORKSPACE_ROOT / f"20_Wiki/Design/Generated_{f.stem}.md"
            if not note_path.exists():
                with open(note_path, 'w') as note:
                    note.write(f"---\ntitle: Generated {f.stem}\ntags: [design, generated]\n---\n\n")
                    note.write(f"![[{target_path.name}]]\n\n")
                    note.write(f"Generated on: {time.ctime(os.path.getmtime(target_path))}\n")

if __name__ == "__main__":
    import sys
    # Ensure directories exist
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            start_comfy()
        elif command == "process":
            process_queue()
        elif command == "sync":
            filter_val = sys.argv[2] if len(sys.argv) > 2 else None
            sync_outputs(filter_val)
        elif command == "status":
            print("Running" if is_comfy_running() else "Stopped")
    else:
        # Default behavior: process queue then sync outputs
        process_queue()
        print("Waiting a bit for generation to finish...")
        # In a real scenario, we'd poll for prompt completion, 
        # but for this simple version, we'll wait and sync.
        time.sleep(10)
        sync_outputs()
