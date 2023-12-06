import os
import json
import argparse
import re
from dataclasses import dataclass, asdict
from typing import Any, List
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_fixed
from ratelimit import limits, RateLimitException
from ratelimit.decorators import sleep_and_retry

from dotenv import load_dotenv
load_dotenv()

# Define a data class for video metadata
@dataclass
class VideoMetadata:
    id: str
    title: str
    description: str
    tags: List[str]
    category_id: str
    privacy_status: str

def format_title(original_title: str) -> str:
    # Regex to match the date format in the title
    match = re.match(r"GMT(\d{4})(\d{2})(\d{2})", original_title)
    if match:
        # Extract the date and reformat it
        year, month, day = match.groups()
        formatted_title = f"{year}-{month}-{day} CNCF TAG Observability Meeting"
        return formatted_title
    return original_title


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@sleep_and_retry
@limits(calls=10, period=60)
def process_video(youtube: Resource, video_metadata: VideoMetadata, dry_run: bool) -> None:
    """process_video _summary_

    _extended_summary_

    Args:
        youtube (Resource): _description_
        video_metadata (VideoMetadata): _description_
        dry_run (bool): _description_
    """
    if dry_run:
        print(f"Dry Run - Video ID: {video_metadata.id}, New Title: {video_metadata.title}")
    else:
        # Update video metadata
        update_request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_metadata.id,
                "snippet": {
                    "title": video_metadata.title,
                    "description": video_metadata.description,
                    "tags": video_metadata.tags,
                    "categoryId": video_metadata.category_id,
                },
                "status": {
                    "privacyStatus": video_metadata.privacy_status
                }
            }
        )
        update_request.execute()


def process_videos(api_key: str, channel_id: str, dry_run: bool) -> List[VideoMetadata]:
    """process_videos _summary_

    _extended_summary_

    Args:
        api_key (str): _description_
        channel_id (str): _description_
        dry_run (bool): _description_

    Returns:
        List[VideoMetadata]: _description_
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    collected_metadata = []

    try:
        next_page_token = None
        while True:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type="video"
            )
            response = request.execute()

            for item in response.get('items', []):
                video_id = item['id']['videoId']
                video_request = youtube.videos().list(part="snippet,status", id=video_id)
                video_response = video_request.execute()

                for video_item in video_response.get('items', []):
                    original_title = video_item['snippet']['title']
                    print(f"Processing video {video_id} with title {original_title}")
                    if original_title.startswith("GMT"):
                        video_metadata = VideoMetadata(
                            id=video_item['id'],
                            title=format_title(original_title),                 # title fixup from zoom GMTxxx to yyyy-mm-dd TAG Obs Meeting happens here
                            description=video_item['snippet']['description'],
                            tags=video_item['snippet'].get('tags', []),
                            category_id=video_item['snippet']['categoryId'],
                            privacy_status=video_item['status']['privacyStatus']
                        )
                        process_video(youtube, video_metadata, dry_run)
                        collected_metadata.append(video_metadata)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
    except RateLimitException:
        print("Rate limit exceeded")

    return collected_metadata

def save_metadata_to_json(metadata: List[VideoMetadata], filename: str):
    with open(filename, 'w') as file:
        json.dump([asdict(video) for video in metadata], file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="YouTube Metadata Processor")
    # parser.add_argument("api_key", help="YouTube API key")
    parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
    #YOUTUBE_ACCOUNT_ID = os.environ.get("YOUTUBE_ACCOUNT_ID")

    YOUTUBE_CHANNEL_ID = os.environ.get("YOUTUBE_CHANNEL_ID")
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

    args = parser.parse_args()

    if YOUTUBE_API_KEY is None or YOUTUBE_CHANNEL_ID is None:
        print("YouTube API key and Channel ID are required")
    else:
        collected_metadata = process_videos(YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID, args.dry_run)
        save_metadata_to_json(collected_metadata, 'youtube_metadata.json')

if __name__ == "__main__":
    main()

