from pathlib import Path
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from apps.config import config
from apps.youtubeinfo import YouTubeInfo

load_dotenv()
csrf = CSRFProtect()
scheduler = BackgroundScheduler()
youtubeinfo = YouTubeInfo()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)

    from apps.schejule import views as sche_views
    from apps.vken import views as vken_views
    from apps.schejule.dbmanage import UpdateCall,ResetQuota

    app.register_blueprint(sche_views.schejule, url_prefix="/schejule")
    app.register_blueprint(vken_views.vken, url_prefix="/vken")

    for hour in range(4, 24):  # 4時から23時までの時間をループ
        scheduler.add_job(UpdateCall, args=[app], trigger=CronTrigger(hour=hour, minute=52, timezone="Asia/Tokyo"))

    # ResetQuota関数を毎日0時に実行するスケジュールを設定
    scheduler.add_job(ResetQuota, trigger=CronTrigger(hour=0, minute=0, timezone="Asia/Tokyo"))
 
    scheduler.start()

    return app