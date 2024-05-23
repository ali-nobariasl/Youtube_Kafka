import logging
import sys
import requests
from config import config




def main():
    logging.info("Start ...")
    link = "https://www.googleapis.com/youtube/v3/playlistItems?"
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]
    
    resonse = requests.get(link, params={
        "key" : google_api_key, 
        "playlistId": youtube_playlist_id ,
        "part": "contentDetails",
    })
    
    logging.debug("GOT %s", resonse.text )




if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
    
    
