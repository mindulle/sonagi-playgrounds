import requests
import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_DIRS = ["10_Sources", "20_Wiki"]
INDEXER_SCRIPT = "00_System/scripts/wiki_indexer.py"
COOLDOWN = 10  # Seconds to wait before re-indexing to handle bulk changes

class WikiHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_triggered = 0

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".md"):
            current_time = time.time()
            if current_time - self.last_triggered > COOLDOWN:
                print(f"--- Change detected in {event.src_path}. Triggering Re-indexing... ---")
                try:
                    # Run the indexer script using the venv python
                    subprocess.run([".venv/bin/python3", INDEXER_SCRIPT], check=True)
                    self.last_triggered = time.time()
                except Exception as e:
                    print(f"Error during auto-indexing: {e}")

if __name__ == "__main__":
    event_handler = WikiHandler()
    observer = Observer()
    for d in WATCH_DIRS:
        if os.path.exists(d):
            observer.schedule(event_handler, d, recursive=True)
        else:
            print(f"Warning: Directory {d} not found.")
    
    print(f"--- Auto-indexing Watcher Started ---")
    print(f"Watching: {', '.join(WATCH_DIRS)}")
    observer.start()
    try:
        while True:
            time.sleep(60)
            try:
                requests.get("http://100.82.184.115:3001/api/push/BHWYsjMv2x?status=up&msg=OK&ping=", timeout=5)
            except Exception:
                pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
