#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import helpers

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = helpers.secretkey_config("youtube")
VIDEO_URL = "https://youtube.com/watch?v="
CHANNEL_URL = "https://youtube.com/channel/"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def youtube_search(options):
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
    video = {"title": search_result["snippet"]["title"],
             "author": search_result["snippet"]["channelTitle"],
             "authorURL": CHANNEL_URL + search_result["snippet"]["channelId"],
             "description": search_result["snippet"]["description"],
             "date": search_result["snippet"]["publishedAt"],
             "url": VIDEO_URL + search_result["id"]["videoId"],
             "thumbnail": search_result["snippet"]["thumbnails"]["high"]
             }
    return video


def example():
    options = helpers.Options("Educational Technology", 25)

    try:
        print youtube_search(options)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


example()
