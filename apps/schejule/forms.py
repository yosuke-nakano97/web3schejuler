from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import URL

class RegisterForm(FlaskForm):
    channel_url = StringField(
        "channel_url",
        validators=[
            URL(message="incorrect url")
        ],
    )
    submit = SubmitField("更新")