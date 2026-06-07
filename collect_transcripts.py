#!/usr/bin/env python3
"""
Setup:
    pip install requests
    export SUPADATA_API_KEY="your_api_key_here"

Usage:
    python collect_transcripts.py
"""

import os
import re
import sys
import time
import datetime
import requests

# Dictionary mapping author-slug -> list of video URLs.
# Pre-filled with a validated example for testing.
SOURCES = {
    "ross-simmonds": [
        "https://www.youtube.com/watch?v=VXxFJAg7YJw",
        "https://www.youtube.com/watch?v=YDqpxuGkfhw",
        "https://www.youtube.com/watch?v=SINviDvBPxA",
    ],
}

def extract_video_id(url):
    """
    Extracts the 11-character YouTube video ID from a URL.
    Returns None if no valid ID is found.
    """
    # Match standard watch?v=, short youtu.be/, embed/, shorts/ or direct ID
    pattern = r'(?:v=|\/v\/|embed\/|youtu\.be\/|\/shorts\/|^)([a-zA-Z0-9_-]{11})(?:\?|&|$)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def parse_transcript(data):
    """
    Robustly parses the transcript content from the Supadata API response.
    Handles three shapes:
    1. Plain string in 'content'
    2. List of segments (each with a 'text' field) in 'content' or root
    3. Plain string or list of segments in a 'text' field
    """
    if isinstance(data, str):
        return data.strip()
    
    if isinstance(data, dict):
        # Case 1 & 2: check 'content' key
        content = data.get("content")
        if content is not None:
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                return parse_list_of_segments(content)
        
        # Case 3: check 'text' key
        text = data.get("text")
        if text is not None:
            if isinstance(text, str):
                return text.strip()
            if isinstance(text, list):
                return parse_list_of_segments(text)
                
    if isinstance(data, list):
        return parse_list_of_segments(data)
        
    return ""

def parse_list_of_segments(segments):
    """
    Helper to join segments containing 'text' keys or string elements.
    """
    text_pieces = []
    for item in segments:
        if isinstance(item, dict):
            t = item.get("text")
            if t is not None:
                text_pieces.append(str(t))
        elif isinstance(item, str):
            text_pieces.append(item)
    return " ".join(text_pieces).strip()

def main():
    api_key = os.environ.get("SUPADATA_API_KEY")
    if not api_key:
        print("Error: SUPADATA_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please set it before running this script:", file=sys.stderr)
        print("  export SUPADATA_API_KEY=\"your_api_key\"", file=sys.stderr)
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    transcripts_dir = os.path.join(base_dir, "research", "youtube-transcripts")

    success_count = 0
    skipped_count = 0
    error_count = 0
    total_count = 0

    today_date = datetime.date.today().isoformat()

    print("Starting YouTube transcript collection...")
    print(f"Destination: {transcripts_dir}")
    print("-" * 60)

    for author_slug, urls in SOURCES.items():
        # Title case author name from slug
        author_name = " ".join(part.capitalize() for part in author_slug.split("-"))
        
        # Create directories if they do not exist
        author_dir = os.path.join(transcripts_dir, author_slug)
        
        for url in urls:
            total_count += 1
            
            # Check for placeholders
            if "VIDEO_ID" in url:
                print(f"[SKIP] {author_slug}: Placeholder URL found ({url})")
                skipped_count += 1
                continue
                
            video_id = extract_video_id(url)
            if not video_id:
                print(f"[SKIP] {author_slug}: Could not extract video ID from URL ({url})")
                skipped_count += 1
                continue

            # Check if video_id is a placeholder literal
            if video_id == "VIDEO_ID":
                print(f"[SKIP] {author_slug}: Placeholder video ID found ({url})")
                skipped_count += 1
                continue

            # Call Supadata API
            endpoint = "https://api.supadata.ai/v1/youtube/transcript"
            params = {
                "url": url,
                "text": "true"
            }
            headers = {
                "x-api-key": api_key
            }

            try:
                # Polite delay
                time.sleep(1.0)
                
                response = requests.get(endpoint, params=params, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    print(f"[ERROR] {author_slug}: {video_id} failed with HTTP status {response.status_code}")
                    error_count += 1
                    continue

                # Parse response content robustly
                try:
                    data = response.json()
                    transcript = parse_transcript(data)
                except ValueError:
                    # Non-JSON content (plain text)
                    transcript = response.text.strip()

                if not transcript:
                    print(f"[ERROR] {author_slug}: {video_id} returned empty transcript content")
                    error_count += 1
                    continue

                # Write out file
                os.makedirs(author_dir, exist_ok=True)
                file_path = os.path.join(author_dir, f"{video_id}.md")
                
                # Format file content
                content_lines = [
                    "---",
                    f'author: "{author_name}"',
                    f'source_url: "{url}"',
                    f'video_id: "{video_id}"',
                    'lang: "en"',
                    f'collected: "{today_date}"',
                    "---",
                    "",
                    transcript
                ]
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(content_lines) + "\n")

                print(f"[OK] {author_slug}: {video_id} saved successfully")
                success_count += 1

            except Exception as e:
                print(f"[ERROR] {author_slug}: {video_id} encountered exception: {e}")
                error_count += 1

    print("-" * 60)
    print("Collection run finished.")
    print(f"Total processed: {total_count}")
    print(f"Successes: {success_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    main()
