import logging
import sys
import requests
import json 
import pformat
from config import config

list_link = "https://www.googleapis.com/youtube/v3/playlistItems"
video_link = "https://www.googleapis.com/youtube/v3/videos"

def fetch_playlist_items_page(google_api_key,youtube_playlist_id, page_token= None):

    response = requests.get(list_link, 
        params={
            "key" : google_api_key, 
            "playlistId": youtube_playlist_id ,
            "part": "contentDetails",
            "pageToken": page_token,
    })
    
    payload =json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload

def fetch_videos_page(google_api_key,video_id, page_token= None):

    response = requests.get(video_link, 
        params={
            "key" : google_api_key, 
            "id": video_id ,
            "part": "snippet, statistics",
            "pageToken": page_token,
    })
    
    payload =json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload


def fetch_playlist_items(google_api_key,youtube_playlist_id, page_token= None):
    
    payload = fetch_playlist_items_page(google_api_key,youtube_playlist_id, page_token)
    
    yield from payload["items"]
    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        yield from fetch_playlist_items(google_api_key,youtube_playlist_id, next_page_token)

def fetch_videos(google_api_key,youtube_playlist_id, page_token= None):
    
    payload = fetch_videos_page(google_api_key,youtube_playlist_id, page_token)
    
    yield from payload["items"]
    next_page_token = payload.get("nextPageToken")
    if next_page_token is not None:
        yield from fetch_videos(google_api_key,youtube_playlist_id, next_page_token)

def summariz_video(video):
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
    }

def main():
    logging.info("Start ...")
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]
    
    for v_item in fetch_playlist_items(google_api_key,youtube_playlist_id):
        video_id = v_item["contentDetails"]["videoId"]
        for video in fetch_videos(google_api_key,video_id):
            logging.info("GOT %s", summariz_video(video))



if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
    
    
