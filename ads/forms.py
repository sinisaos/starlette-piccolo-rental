from wtforms import Form, IntegerField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, ValidationError


class AdForm(Form):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    price = IntegerField("Price", validators=[InputRequired()])
    room = IntegerField("Number of rooms", validators=[InputRequired()])
    visitor = IntegerField(
        "Maximum visitors per apartment", validators=[InputRequired()]
    )
    address = StringField("Address", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])

    def validate_price(form, field):
        if type(field.data) != int:
            raise ValidationError("Price must be integer")


CHOICES = [((str(i), str(i))) for i in range(1, 6)]


class AdEditForm(Form):
    title = StringField(validators=[InputRequired()])
    content = TextAreaField(validators=[InputRequired()])
    price = IntegerField(validators=[InputRequired()])
    room = IntegerField(validators=[InputRequired()])
    visitor = IntegerField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    city = StringField(validators=[InputRequired()])

    def validate_price(form, field):
        if type(field.data) != int:
            raise ValidationError("Price must be integer")


class ReviewForm(Form):
    content = TextAreaField(validators=[InputRequired()])
    grade = SelectField("Ad grade", choices=CHOICES)


class ReviewEditForm(Form):
    content = TextAreaField(validators=[InputRequired()])
    grade = SelectField("Ad grade", choices=CHOICES)


class RentForm(Form):
    start_date = DateField(validators=[InputRequired()])
    end_date = DateField(validators=[InputRequired()])
