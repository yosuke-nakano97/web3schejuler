from apps.app import youtubeinfo 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

youtube = youtubeinfo.BuildApiService()

def GetRecentVideoId(playlist_id):
    try:
        youtubeinfo.QuotaSub(1)
        respond =youtube.playlistItems().list(
            part = "contentDetails",
            playlistId = playlist_id,
            maxResults=5
        ).execute()
    except HttpError:
        print("request was denied")
    ids = []
    for item in respond['items']:
        data = item['contentDetails']
        ids.append(data['videoId'])

    return ids


def GetstreamInfo(video_id):
    try:
        youtubeinfo.QuotaSub(1)
        respond =youtube.videos().list(
            part = "liveStreamingDetails,snippet",
            id = video_id
        ).execute()

        #終わってるかどうか判定
        items = respond['items']
        item = items[0]
        snippet = item['snippet']
        status = snippet['liveBroadcastContent']
        if status == "upcoming":
            #いろんな情報ゲット
            #time
            liveStreamingDetails = item['liveStreamingDetails']
            time = liveStreamingDetails['scheduledStartTime']
            # 開始時刻が今から１週間いないかどうか
            now = datetime.datetime.now()
            time = TimeCalibration(time)
            if time - now > datetime.timedelta(weeks=1):
                return None
            #title
            title = snippet['title']
            #thumbnail
            thumbnails = snippet['thumbnails']
            thumbnail = thumbnails['medium']
            thumbnail_url = thumbnail['url']
            stream_info =[video_id,title,time,thumbnail_url]
            return stream_info
        else:
            return None
            
    except HttpError:
        print("request was denied")
        return None

    except KeyError:
        return None


# calculate JPT
def TimeCalibration(time):
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    dt = datetime.datetime.strptime(time,fmt)
    print(dt)
    jpt = dt + datetime.timedelta(hours=9)
    return jpt