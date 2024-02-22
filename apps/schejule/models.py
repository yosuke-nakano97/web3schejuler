import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

Base = declarative_base()


system_timezone = pytz.timezone('Asia/Tokyo')
current_time=datetime.now()
current_time_jst = current_time.astimezone(system_timezone)

class Channel(Base):
    __tablename__ = "channel"
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    icon_path = Column(String)
    playlist = Column(String, unique=True)
    created_at = Column(DateTime, default=current_time_jst)
    update_at = Column(DateTime, default=current_time_jst, onupdate=current_time_jst)
    stream = relationship("Stream", backref="channel", order_by="desc(Stream.starttime)")

class Stream(Base):
    __tablename__ = "stream"
    id = Column(String, primary_key=True)
    channel_id = Column(String, ForeignKey('channel.id'))
    title = Column(String)
    thumbnail_path = Column(String)
    starttime = Column(DateTime, index=True)
    created_at = Column(DateTime, default=current_time_jst)
    update_at = Column(DateTime, default=current_time_jst, onupdate=current_time_jst)

sche_engine = sqlalchemy.create_engine('sqlite:///scheduler.sqlite3', echo=True, connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=sche_engine)

def update_created_at(mapper, connection, target):
    if not target.created_at:
        target.created_at = datetime.now(pytz.timezone('Asia/Tokyo'))

listen(Channel, 'before_insert', update_created_at)
listen(Stream, 'before_insert', update_created_at)
