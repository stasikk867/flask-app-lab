from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
    FileField,
    IntegerField,
    DecimalField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    Regexp,
    NumberRange,
)


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(
                min=3,
                max=100,
                message="Назва має містити від 3 до 100 символів."
            )
        ]
    )

    content = TextAreaField(
        "Опис товару",
        render_kw={"rows": 5, "cols": 40},
        validators=[
            DataRequired(message="Введіть опис товару.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну."),
            NumberRange(
                min=0.01,
                message="Ціна має бути більшою за 0."
            )
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("", "Оберіть категорію"),
            ("electronics", "Електроніка"),
            ("clothing", "Одяг"),
            ("books", "Книги"),
            ("food", "Їжа"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть категорію.")
        ]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(message="Введіть кількість."),
            NumberRange(
                min=0,
                message="Кількість не може бути від'ємною."
            )
        ]
    )

    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені формати: JPG, JPEG, PNG."
            )
        ]
    )

    submit = SubmitField("Зберегти")
