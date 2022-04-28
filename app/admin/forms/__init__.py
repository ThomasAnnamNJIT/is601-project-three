from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.widgets import TextArea


class DeleteForm(FlaskForm):
    username = StringField(default="")
    confirm = SubmitField("Confirm")


class AddForm(FlaskForm):
    username = EmailField(validators=[DataRequired()],
                          render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    # TODO: Add this later
    about = StringField(validators=[InputRequired(), Length(min=10, max=100)], widget=TextArea(),
                        render_kw={"placeholder": "About"})
    submit = SubmitField("Submit")
