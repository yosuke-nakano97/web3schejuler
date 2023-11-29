from apps.app import youtubeinfo
import json
from flask import flash
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

youtube = youtubeinfo.BuildApiService()

# チャンネル情報をもらってくる(name id icon)
def GetChannelIds(url):
    ch_info = []
    try:
        youtubeinfo.QuotaSub(100)
        respond = youtube.search().list(
        part ="snippet",
        type = "channel",
        q = url,
        maxResults = 1
        ).execute()
        # name
        for item in respond['items']:
            snippet = item['snippet']
            name = snippet['title']
        ch_info.append(name)
        #icon
        for item in respond['items']:
            snippet = item['snippet']
            thumbnails = snippet['thumbnails']
            thumbnail = thumbnails['default']
            icon = thumbnail['url']
        ch_info.append(icon)
        #id
        for item in respond['items']:
            snippet = item['snippet']
            id = snippet['channelId']
        ch_info.append(id)
        ch_info.append(GetPlaylistId(id))
        return ch_info
    except HttpError:
        flash("request was denied")

def GetChannelInfo(id):
    ch_info = []
    try:
        youtubeinfo.QuotaSub(1)
        respond = youtube.channels().list(
        part ="snippet",
        id = id,
        maxResults = 1
        ).execute()
        # name
        for item in respond['items']:
            snippet = item['snippet']
            name = snippet['title']
        ch_info.append(name)
        #icon
        for item in respond['items']:
            snippet = item['snippet']
            thumbnails = snippet['thumbnails']
            thumbnail = thumbnails['default']
            icon = thumbnail['url']
        ch_info.append(icon)
    except HttpError:
        flash("request was denied")

    return ch_info

#Get the playlist with channel's all video 
def GetPlaylistId(ch_id):
    try:
        youtubeinfo.QuotaSub(1)
        respond = youtube.channels().list(
        part ="contentDetails",
        id = ch_id,
        maxResults = 1
        ).execute()

        for item in respond["items"]:
            contentDetail = item['contentDetails']
            relatedPlaylists = contentDetail['relatedPlaylists']
            playlist_id = relatedPlaylists['uploads']
        return playlist_id

    except HttpError:
        print("request was denied")
        flash("error")

