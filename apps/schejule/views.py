from flask import Blueprint, redirect, render_template, url_for, request, flash
from datetime import datetime
from apps.schejule.forms import RegisterForm
from apps.schejule.models import  Channel, Stream
import apps.schejule.dbmanage as dbmanage
from apps.app import db
from apps.app import youtubeinfo

schejule = Blueprint(
    "schejule",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@schejule.route("/")
def index():
    streams = (
        db.session.query(Channel, Stream)
        .join(Stream)
        .order_by(Stream.starttime.asc())
        .all()
    )
    db.session.close()

    stream_group = {}
    week_info = {
        "0":["月","rgb(255, 244, 189)"],
        "1":["火","rgb(211, 255, 189)"],
        "2":["水","rgb(189, 255, 222)"],
        "3":["木","rgb(189, 232, 255)"],
        "4":["金","rgb(255, 255, 189)"],
        "5":["土","rgb(255, 189, 255)"],
        "6":["日","rgb(255, 189, 189)"]
    }
    for stream in streams:
        starttime_date = stream.Stream.starttime.strftime('%m/%d')
        if starttime_date not in stream_group:
            stream_group[starttime_date] = {'streams': []}
        weekday_number = stream.Stream.starttime.strftime('%w')
        stream_group[starttime_date]['weekday'] = week_info[weekday_number]
        stream_group[starttime_date]['streams'].append(stream)

    form = RegisterForm()
    print(f"{youtubeinfo.quota}")

    return render_template(
        "schejule/index.html",
        stream_group=stream_group,
        form=form,
    )

@schejule.route("/register", methods=["POST"])
def channel_register():
    form = RegisterForm()
    if form.validate_on_submit():
        url = form.channel_url.data
        dbmanage.RegisterChannel(url)
        return redirect(url_for("schejule.index"))
    flash("チャンネルの形式がおかしいです！")
    return redirect(url_for("schejule.index")) 

@schejule.route("/update", methods=["POST"])
def stream_update():
    dbmanage.UpdateStream()
    
    return redirect(url_for("schejule.index")) 

@schejule.route("/select")
def select_channel():
    channels = db.session.query(Channel).all()
    form = RegisterForm()

    return render_template(
        "schejule/select.html",
        channels=channels,
        form=form
    )

@schejule.route("/delete/<channel_id>", methods=["POST","GET"])
def delete_channel(channel_id):
    dbmanage.DeleteChannel(channel_id)
    return redirect(url_for("schejule.index")) 
