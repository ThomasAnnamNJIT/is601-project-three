from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, PasswordInput


class DeleteForm(FlaskForm):
    username = StringField(default="")
    confirm = SubmitField("Confirm")


class EditForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[DataRequired()],
                             widget=PasswordInput(hide_value=False),
                             render_kw={"placeholder": "Password"})
    # TODO: Add this later
    about = StringField(validators=[DataRequired()], widget=TextArea(),
                        render_kw={"placeholder": "About", "rows": 10})
    submit = SubmitField("Submit")
