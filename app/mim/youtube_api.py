#!/usr/bin/python
import os
import random
import isodate
import Recommender as r

from apiclient.discovery import build
from apiclient.errors import HttpError

from . import logger

import util

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
if 'YOUTUBE_ID' in os.environ:
    YOUTUBE_APP_ID, DEVELOPER_KEY = os.environ['YOUTUBE_ID'], os.environ['YOUTUBE_SECRET']
else:
    YOUTUBE_APP_ID, DEVELOPER_KEY = util.secretkey_config("youtube")
VIDEO_URL = "https://youtube.com/watch?v="
CHANNEL_URL = "https://youtube.com/channel/"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def get_one(options):
    videos, nextPage = search(options) # TODO - Should store these videos fully to use the API less

    # ensure unique result based on user history
    videos = util.get_unique(videos)
    if len(videos) > 0:
        single_video = pick_option(videos)
    else:
        # if there aren't any unique videos, go to the next page and search again
        options.pageToken = nextPage
        return get_one(options)

    # get extra details:
    id = single_video["id"]
    entry = youtube.videos().list(part='snippet,contentDetails,statistics', id=id).execute()
    single_video["description"] = get_full_description(id, entry)
    single_video["duration"] = format_duration(get_duration(id, entry))
    return single_video


def search(options):
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results,
        pageToken=options.pageToken
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        # only return videos at this point
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(format_result(search_result))

    return videos, search_response["nextPageToken"]


def format_result(search_result):
    video = {"content_type": "video",
             "id": search_result["id"]["videoId"],
             "title": search_result["snippet"]["title"],
             "author":
                 {"name": search_result["snippet"]["channelTitle"],
                  "url": CHANNEL_URL + search_result["snippet"]["channelId"]}
             ,
             "description": search_result["snippet"]["description"],
             "date": search_result["snippet"]["publishedAt"],
             "url": VIDEO_URL + search_result["id"]["videoId"],
             "thumbnail": search_result["snippet"]["thumbnails"]["high"]
             # "time": search_result["contentDetails"]["duration"]
             }
    return video


def get_full_description(video_id, entry):
    '''
    Full description only loaded in snippet of individual/list of ids pulled back
    :param video_id: the id of the video(s) to get back [comma separated list if more than one]
    :return: a string containing the full description of the video
    '''
    if entry is None:
        entry = youtube.videos().list(part='snippet', id=video_id).execute()
    return entry["items"][0]["snippet"]["description"]


def get_duration(video_id, entry):
    if entry is None:
        entry = youtube.videos().list(part='snippet', id=video_id).execute()
    return entry["items"][0]["contentDetails"]["duration"]

def format_duration(duration):
    '''
    Format Duration string object into human readable format
    Use tips from https://stackoverflow.com/a/539360
    :param duration: string object of ISO 8601 duration
    :return: string formatted (HH:MM:SS)
    '''
    dur = isodate.parse_duration(duration)
    s = dur.total_seconds()
    h, remainder = divmod(s, 3600)
    m, s = divmod(remainder, 60)
    duration = "(%d:%02d:%02d)" % (h,m,s)
    return duration


def pick_option(videos):
    """
    Pick a video from the list using recommendation score or random if rec scores all too low
    :param videos: an array of videos formatted in format_results()
    :return: A single video option
    """
    # random choice (default)
    video = videos[random.randint(0, len(videos) - 1)]

    # use recommendation engine
    options = []
    user = util.get_user()
    for v in videos:
        option = {
            "user": user,
            "content_id": v["id"]
        }
        options.append(option)
    predictions = r.predict_options(options)
    if max(predictions) is not 0:
        # pick the highest predicted value, otherwise if no prediction available do random
        video = videos[predictions.index(max(predictions))]

    return video


def example():
    options = util.Options("Educational Technology", 25)

    try:
        print search(options)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


# example()
