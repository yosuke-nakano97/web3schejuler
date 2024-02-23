import sqlalchemy, os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.event import listen
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DATABASE_PATH")
print(db_path)
print(3)
Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, autoincrement=True)
    goods_name = Column(String(length=255))
    user_id = Column(Integer, ForeignKey('user.id'))
    price = Column(Integer)
    oshi = Column(String(length=255))
    message_id = Column(Integer, default=0, index=True)
    created_at = Column(DateTime, index=True)
    user = relationship("User")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    total_use = Column(Integer)
    year_use = Column(Integer)
    month_use = Column(Integer)


bot_engine = sqlalchemy.create_engine("sqlite:///" + db_path, echo=False)

Base.metadata.create_all(bind=bot_engine)

def update_created_at(mapper, connection, target):
    if not target.created_at:
        target.created_at = datetime.now(pytz.timezone('Asia/Tokyo'))

listen(Expense, 'before_insert', update_created_at)