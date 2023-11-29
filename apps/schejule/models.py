from datetime import datetime
import pytz
from apps.app import db

system_timezone = pytz.timezone('Asia/Tokyo')
current_time=datetime.now()
current_time_jst = current_time.astimezone(system_timezone)

class Channel(db.Model):
    __tablename__ = "channel"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, index=True)
    icon_path = db.Column(db.String)
    playlist = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=current_time_jst)
    update_at = db.Column(db.DateTime, default=current_time_jst, onupdate=current_time_jst)
    stream = db.relationship("Stream", backref="channel", order_by="desc(Stream.starttime)")

class Stream(db.Model):
    __tablename__ = "stream"
    id = db.Column(db.String, primary_key=True)
    channel_id = db.Column(db.String, db.ForeignKey('channel.id'))
    title = db.Column(db.String)
    thumbnail_path = db.Column(db.String)
    starttime = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, default=current_time_jst)
    update_at = db.Column(db.DateTime, default=current_time_jst, onupdate=current_time_jst)