import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_extract.py <video_id>")
        sys.exit(1)
    
    v_id = sys.argv[1]
    print(f"--- Extracting Transcript for {v_id} ---")
    text = extract_transcript(v_id)
    print(text[:1000] + "...") # Print first 1000 chars
