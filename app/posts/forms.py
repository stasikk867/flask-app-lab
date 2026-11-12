from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    SelectField,
    SubmitField
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=150)]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    enabled = BooleanField("Active", default=True)

    publish_date = DateTimeLocalField(
        "Publication date",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Technology"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")


class DeletePostForm(FlaskForm):
    submit = SubmitField("Confirm deletion")
