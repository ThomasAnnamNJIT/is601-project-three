from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.widgets import TextArea


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")


class RegisterForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    about = StringField(validators=[InputRequired()], widget=TextArea(),
                        render_kw={"placeholder": "About"})


class LoginForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
