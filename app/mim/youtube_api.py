#!/usr/bin/python
import os

from apiclient.discovery import build
from apiclient.errors import HttpError

import util

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
if 'YOUTUBE_ID' in os.environ:
    YOUTUBE_APP_ID, DEVELOPER_KEY = os.environ['YOUTUBE_ID'], os.environ['YOUTUBE_SECRET'] # helpers.secretkey_config("youtube")
else:
    YOUTUBE_APP_ID, DEVELOPER_KEY = util.secretkey_config("youtube")
VIDEO_URL = "https://youtube.com/watch?v="
CHANNEL_URL = "https://youtube.com/channel/"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def search(options):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        # only return videos at this point
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(format_result(search_result))

    return videos


def format_result(search_result):
    video = {"content_type": "video",
             "id": search_result["id"]["videoId"],
             "title": search_result["snippet"]["title"],
             "authors": [
                 {"name": search_result["snippet"]["channelTitle"],
                  "url": CHANNEL_URL + search_result["snippet"]["channelId"]}
             ],
             "description": search_result["snippet"]["description"],
             "date": search_result["snippet"]["publishedAt"],
             "url": VIDEO_URL + search_result["id"]["videoId"],
             "thumbnail": search_result["snippet"]["thumbnails"]["high"]
             }
    return video


def example():
    options = helpers.Options("Educational Technology", 25)

    try:
        print search(options)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


# example()
