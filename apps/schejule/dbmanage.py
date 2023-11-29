from apps.app import db
from apps.schejule.models import Channel,Stream
import apps.programs.channel as ch
import apps.programs.stream as st
from apps.app import youtubeinfo
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from flask import flash
from datetime import datetime
import pytz


def RegisterChannel(url):
    youtubeinfo.CheckQuotaRemain()
    info = ch.GetChannelIds(url)
    try:
        # 基本系列：新しくレコードを作成する
        channel = Channel(
            id=info[2],
            name=info[0],
            icon_path=info[1],
            playlist=info[3]
        )
        db.session.add(channel)
        db.session.commit()
        db.session.close()
        flash("登録完了")

    except Exception as e:
        db.session.rollback()
        UpdateChannelInfo(info[2],info)
    finally:
        if db.session is not None:
            db.session.close()
       
def UpdateChannelInfo(id,info):
    try:
        youtubeinfo.CheckQuotaRemain()

        channel = db.session.query(Channel).filter_by(id=id).first()
        channel.name = info[0]
        channel.icon_path = info[1]
        db.session.commit()
        db.session.close()
        flash("更新完了")
        return 1
    except Exception as e:
        flash("something wrong in UpdateChannelInfo")
        print(e)
        return 0

def UpdateChannel():
    try:
        channels = db.session.query(Channel).all()
        for channel in channels:
            channelid = channel.id
            info = ch.GetstreamInfo(channelid)
            UpdateChannelInfo(channelid,info)
    except Exception as e:
        print(f"somethingwronginUpdateChannel:{e}")

def DeleteChannel(ch_id):
    print(ch_id)

    try:
        # IDをもらってきて対応するレコードを削除
        channel = db.session.query(Channel).filter_by(id=ch_id).first()
        # あった
        if channel:
            related_streams = db.session.query(Stream).filter_by(channel_id=ch_id).all()
            if related_streams:
                for stream in related_streams:
                    db.session.delete(stream)
            db.session.delete(channel)
            db.session.commit()
            flash("Channel deleted successfully.")
        # ない
        else:
            flash("Channel not found.")

    except Exception as e:
        flash("Something went wrong in DeleteChannel")
        print(e)

    finally:
        db.session.close()

def UpdateStream():
    # 今の時間よりもStarttimeが遅いものを削除する
    try:
        youtubeinfo.CheckQuotaRemain()
        system_timezone = pytz.timezone('Asia/Jakarta')
        current_time=datetime.now()
        current_time_jst_minus_two = current_time.astimezone(system_timezone)
        db.session.query(Stream).filter(Stream.starttime < current_time_jst_minus_two).delete()
        db.session.commit()

    except Exception as e:
        # 削除で問題発生
        db.session.rollback()
        print(f"UpdateSrteam:delete{e}")

    finally:
        db.session.close()
        
    # チャンネルIDもらってビデオIDもらって登録する
    channels = db.session.query(Channel).all()
    for channel in channels:
        print(channel)
        video_ids = st.GetRecentVideoId(channel.playlist)
        for video_id in video_ids:
            print(f"videoid:{video_id}")
            info = st.GetstreamInfo(video_id)
            print(f"info:{info}")
            if info is not None:
                if RegisterStream(info,channel.id)!=0:
                    UpdateStreamInfo(info)
    flash("update完了")

def RegisterStream(info,ch_id):
    try:
        # 基本系列：新しくレコードを作成する
        stream = Stream(
            id=info[0],
            channel_id=ch_id,
            title=info[1],
            thumbnail_path=info[3],
            starttime=info[2],
        )
        db.session.add(stream)
        db.session.commit()
        return 0

    except Exception as e:
        # IDとそれに対応するデーターがもうあった場合：
        db.session.rollback()
        # 更新処理
        if (UpdateStreamInfo(info)!=0):
            # 更新が失敗
            flash("something wrong in Register Stream")
        return 1

def DeleteStream(id):
    try:
        db.session.query(Stream).filter(Stream.id == id).delete()
        db.session.commit()
        flash("削除完了")
        return 0

    except Exception as e:
        db.session.rollback()
        flash("削除失敗")
        print(e)
        return 1 

    finally:
        db.session.close()

def UpdateStreamInfo(info):
    try:
        print(info[0])
        stream = db.session.query(Stream).filter_by(id=info[0]).first()
        stream.title = info[1]
        stream.thumbnail_path = info[3]
        stream.starttime = info[2]
        db.session.commit()
        return 0
    except Exception as e:
        db.session.rollback()
        flash("something wrong in UpdatestreamInfo")
        print(f"error{e}")
        return 1

# バックグラウンドで更新する時の処理たち
def UpdateCall(app):
    with app.app_context():
        UpdateStreamNotFlash()
        print("------------------------1finish-------------------------------")
        UpdateChannelNotFlash()
        print("2finish")

def UpdateStreamNotFlash():
    youtubeinfo.CheckQuotaRemain()
    # 今の時間よりもStarttimeが遅いものを削除する
    try:
        system_timezone = pytz.timezone('Asia/Jakarta')
        current_time=datetime.now()
        current_time_jst_minus_two = current_time.astimezone(system_timezone)
        db.session.query(Stream).filter(Stream.starttime < current_time_jst_minus_two).delete()
        db.session.commit()

    except Exception as e:
        # 削除で問題発生
        db.session.rollback()
        print(f"UpdateSrteam:delete{e}")

    finally:
        db.session.close()
        
    # チャンネルIDもらってビデオIDもらって登録する
    channels = db.session.query(Channel).all()
    for channel in channels:
        print(channel)
        video_ids = st.GetRecentVideoId(channel.playlist)
        for video_id in video_ids:
            # print(f"videod:{video_id}")i
            info = st.GetstreamInfo(video_id)
            print(f"info:{info}")
            if info is not None:
                if RegisterStream(info,channel.id)!=0:
                    UpdateStreamInfo(info)
    db.session.close()

def UpdateStreamInfoNotFlash(info):
    try:
        print(info[0])
        stream = db.session.query(Stream).filter_by(id=info[0]).first()
        stream.title = info[1]
        stream.thumbnail_path = info[3]
        stream.starttime = info[2]
        db.session.commit()
        return 0

    except Exception as e:
        print(f"error:{e}")
        return 1

def RegisterStreamNotFlash(info,ch_id):
    try:
        # 基本系列：新しくレコードを作成する
        stream = Stream(
            id=info[0],
            channel_id=ch_id,
            title=info[1],
            thumbnail_path=info[3],
            starttime=info[2],
        )
        db.session.add(stream)
        db.session.commit()
        return 0

    except Exception as e:
        # IDとそれに対応するデーターがもうあった場合：
        db.session.rollback()
        # 更新処理
        if (UpdateStreamInfo(info)!=0):
            # 更新が失敗
            print(f"something wrong in Register Stream:{e}")
        return 1

def UpdateChannelNotFlash():
    try:
        channels = db.session.query(Channel).all()
        for channel in channels:
            print(channel)
            info = ch.GetChannelInfo(channel.id)
            print(info)
            UpdateChannelInfoNotFlash(channel.id,info)
    except Exception as e:
        print(f"somethingwronginUpdateChannel:{e}")

def UpdateChannelInfoNotFlash(id,info):
    try:
        youtubeinfo.CheckQuotaRemain()
        channel = db.session.query(Channel).filter_by(id=id).first()
        channel.name = info[0]
        channel.icon_path = info[1]
        db.session.commit()
        db.session.close()
        return 1
    except Exception as e:
        print(e)
        return 0
# 日付が変更されたらクオートを元に戻す
def ResetQuota():
    youtubeinfo.QuotaReset()