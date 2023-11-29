from pathlib import Path
from apps.config import config
from apps.youtubeinfo import YouTubeInfo
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
csrf = CSRFProtect()
scheduler = BackgroundScheduler()
youtubeinfo = YouTubeInfo()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    from apps.schejule import views as sche_views
    from apps.schejule.dbmanage import UpdateCall,ResetQuota

    app.register_blueprint(sche_views.schejule, url_prefix="/schejule")

    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=4, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=5, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=6, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=7, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=8, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=9, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=10, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=11, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=12, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=13, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=14, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=15, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=16, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=17, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=18, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=19, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=20, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=21, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=22, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=23, minute=45, timezone="Asia/Tokyo"))
    scheduler.add_job(ResetQuota, trigger=CronTrigger(hour=0, minute=0, timezone="Asia/Tokyo"))
 
    scheduler.start()

    return app