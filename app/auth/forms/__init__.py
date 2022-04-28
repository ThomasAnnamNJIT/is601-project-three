from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, DataRequired


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField("Upload")


class RegisterForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    about = StringField(validators=[InputRequired(), Length(min=10, max=100)], render_kw={"placeholder": "About"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")
