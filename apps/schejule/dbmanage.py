from apps.schejule.models import Channel, Stream, sche_engine
import apps.programs.channel as ch
import apps.programs.stream as st
from apps.app import youtubeinfo
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from flask import flash
from datetime import datetime
import pytz


def RegisterChannel(url):
    youtubeinfo.CheckQuotaRemain()
    info = ch.GetChannelIds(url)
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        # 基本系列：新しくレコードを作成する
        channel = Channel(
            id=info[2],
            name=info[0],
            icon_path=info[1],
            playlist=info[3]
        )
        session.add(channel)
        session.commit()
        session.close()
        flash("登録完了")

    except Exception as e:
        session.rollback()
        UpdateChannelInfo(info[2],info)
    finally:
        if session is not None:
            session.close()
       
def UpdateChannelInfo(id,info):
    try:
        youtubeinfo.CheckQuotaRemain()
        Session = sessionmaker(bind=sche_engine)
        session = Session()

        channel = session.query(Channel).filter_by(id=id).first()
        channel.name = info[0]
        channel.icon_path = info[1]
        session.commit()
        session.close()
        flash("更新完了")
        return 1
    except Exception as e:
        flash("something wrong in UpdateChannelInfo")
        print(e)
        return 0

def UpdateChannel():
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        channels = session.query(Channel).all()
        for channel in channels:
            channelid = channel.id
            info = ch.GetstreamInfo(channelid)
            UpdateChannelInfo(channelid,info)
    except Exception as e:
        print(f"somethingwronginUpdateChannel:{e}")

def DeleteChannel(ch_id):
    print(ch_id)

    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        # IDをもらってきて対応するレコードを削除
        channel = session.query(Channel).filter_by(id=ch_id).first()
        # あった
        if channel:
            related_streams = session.query(Stream).filter_by(channel_id=ch_id).all()
            if related_streams:
                for stream in related_streams:
                    session.delete(stream)
            session.delete(channel)
            session.commit()
            flash("Channel deleted successfully.")
        # ない
        else:
            flash("Channel not found.")

    except Exception as e:
        flash("Something went wrong in DeleteChannel")
        print(e)

    finally:
        session.close()

def UpdateStream():
    # 今の時間よりもStarttimeが遅いものを削除する
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        youtubeinfo.CheckQuotaRemain()
        system_timezone = pytz.timezone('Asia/Jakarta')
        current_time=datetime.now()
        current_time_jst_minus_two = current_time.astimezone(system_timezone)
        session.query(Stream).filter(Stream.starttime < current_time_jst_minus_two).delete()
        session.commit()

    except Exception as e:
        # 削除で問題発生
        session.rollback()
        print(f"UpdateSrteam:delete{e}")

    finally:
        session.close()
        
    # チャンネルIDもらってビデオIDもらって登録する
    channels = session.query(Channel).all()
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
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        # 基本系列：新しくレコードを作成する
        stream = Stream(
            id=info[0],
            channel_id=ch_id,
            title=info[1],
            thumbnail_path=info[3],
            starttime=info[2],
        )
        session.add(stream)
        session.commit()
        return 0

    except Exception as e:
        # IDとそれに対応するデーターがもうあった場合：
        session.rollback()
        # 更新処理
        if (UpdateStreamInfo(info)!=0):
            # 更新が失敗
            flash("something wrong in Register Stream")
        return 1

def DeleteStream(id):
    
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        session.query(Stream).filter(Stream.id == id).delete()
        session.commit()
        flash("削除完了")
        return 0

    except Exception as e:
        session.rollback()
        flash("削除失敗")
        print(e)
        return 1 

    finally:
        session.close()

def UpdateStreamInfo(info):
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        print(info[0])
        stream = session.query(Stream).filter_by(id=info[0]).first()
        stream.title = info[1]
        stream.thumbnail_path = info[3]
        stream.starttime = info[2]
        session.commit()
        return 0
    except Exception as e:
        session.rollback()
        flash("something wrong in UpdatestreamInfo")
        print(f"error{e}")
        return 1

# バックグラウンドで更新する時の処理たち
def UpdateCall(app):
    with app.app_context():
        UpdateStreamNotFlash()
        UpdateChannelNotFlash()
        print("2finish")

def UpdateStreamNotFlash():
    youtubeinfo.CheckQuotaRemain()
    # 今の時間よりもStarttimeが遅いものを削除する
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        system_timezone = pytz.timezone('Asia/Jakarta')
        current_time=datetime.now()
        current_time_jst_minus_two = current_time.astimezone(system_timezone)
        session.query(Stream).filter(Stream.starttime < current_time_jst_minus_two).delete()
        session.commit()

    except Exception as e:
        # 削除で問題発生
        session.rollback()
        print(f"UpdateSrteam:delete{e}")

    finally:
        session.close()
        
    # チャンネルIDもらってビデオIDもらって登録する
    channels = session.query(Channel).all()
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
    session.close()

def UpdateStreamInfoNotFlash(info):
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        print(info[0])
        stream = session.query(Stream).filter_by(id=info[0]).first()
        stream.title = info[1]
        stream.thumbnail_path = info[3]
        stream.starttime = info[2]
        session.commit()
        return 0

    except Exception as e:
        print(f"error:{e}")
        return 1

def RegisterStreamNotFlash(info,ch_id):
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        # 基本系列：新しくレコードを作成する
        stream = Stream(
            id=info[0],
            channel_id=ch_id,
            title=info[1],
            thumbnail_path=info[3],
            starttime=info[2],
        )
        session.add(stream)
        session.commit()
        return 0

    except Exception as e:
        # IDとそれに対応するデーターがもうあった場合：
        session.rollback()
        # 更新処理
        if (UpdateStreamInfo(info)!=0):
            # 更新が失敗
            print(f"something wrong in Register Stream:{e}")
        return 1

def UpdateChannelNotFlash():
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        channels = session.query(Channel).all()
        for channel in channels:
            print(channel)
            info = ch.GetChannelInfo(channel.id)
            print(info)
            UpdateChannelInfoNotFlash(channel.id,info)
    except Exception as e:
        print(f"somethingwronginUpdateChannel:{e}")

def UpdateChannelInfoNotFlash(id,info):
    try:
        Session = sessionmaker(bind=sche_engine)
        session = Session()
        youtubeinfo.CheckQuotaRemain()
        channel = session.query(Channel).filter_by(id=id).first()
        channel.name = info[0]
        channel.icon_path = info[1]
        session.commit()
        session.close()
        return 1
    except Exception as e:
        print(e)
        return 0
# 日付が変更されたらクオートを元に戻す
def ResetQuota():
    youtubeinfo.QuotaReset()