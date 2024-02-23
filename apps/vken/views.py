from flask import Blueprint, redirect, render_template, url_for, request, flash
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from apps.vken.models import User, Expense, bot_engine

vken = Blueprint(
    "vken",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@vken.route("/")
def index():
    try:
        Session = sessionmaker(bind=bot_engine)
        session = Session()
        records = (
            session.query(User)
            .order_by(User.total_use)
            .all()
        )
        session.close()
    except Exception as e:
        pass

    return render_template(
        "vken/index.html",
        records = records,
    )

@vken.route("/detail/<user_id>")
def userdetail(user_id):
    print("with id")
    try:
        # セッション生成
        Session = sessionmaker(bind=bot_engine)
        session = Session()
        # ユーザーIDでレコード検索
        records = session.query(Expense).filter_by(user_id=user_id).order_by(Expense.created_at).all()
        
        print(records)
        
    except Exception as e:
        # 何か例外が起こったらここで対応
        print(e)
        
    finally:
        # 絶対セッション閉じてから出ていく
        session.close()
    
    return render_template(
        "vken/detail.html",
        records = records,
    )



@vken.route("/adminseacretmanagesiite")
def detail():
    return redirect(url_for("schejule.index"))