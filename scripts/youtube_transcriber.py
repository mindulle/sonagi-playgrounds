import sys
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def fetch_transcript(video_id):
    try:
        # Some versions use list_transcripts, some use list() on an instance
        # Let's try the most common one first
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except AttributeError:
            # Fallback to instance method if class method is missing
            transcript_list = YouTubeTranscriptApi().list(video_id)
            
        # Try to get Korean, then English
        try:
            transcript = transcript_list.find_transcript(['ko'])
        except:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except:
                # Get the first available
                transcript = next(iter(transcript_list))
        
        data = transcript.fetch()
        # Some versions return objects, some return dicts
        texts = []
        for item in data:
            if isinstance(item, dict):
                texts.append(item.get('text', ''))
            else:
                texts.append(getattr(item, 'text', str(item)))
        
        full_text = " ".join(texts)
        # Add line breaks every ~500 chars to prevent Obsidian indexing crash
        wrapped_text = ""
        for i in range(0, len(full_text), 500):
            wrapped_text += full_text[i:i+500] + "\n"
        return wrapped_text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcriber.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    v_id = get_video_id(url)
    if not v_id:
        print("Invalid YouTube URL")
        sys.exit(1)
        
    print(f"--- Fetching transcript for {v_id} ---")
    content = fetch_transcript(v_id)
    
    # Save to a file in 20_Wiki/_resources/transcripts/
    os.makedirs("20_Wiki/_resources/transcripts", exist_ok=True)
    safe_title = v_id # Could fetch title with yt-dlp if needed
    file_path = f"20_Wiki/_resources/transcripts/{safe_title}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Transcript for {url}\n\n")
        f.write(content)
    
    print(f"Saved to {file_path}")
