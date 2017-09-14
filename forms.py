from wtforms import Form, StringField, PasswordField, validators, IntegerField
from wtforms.validators import Email


class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm')


class TelephoneForm(Form):
    item = StringField('item', [validators.required()])
    quantity = IntegerField('quantity', [validators.required()])
    price = IntegerField('price')


class EmailPasswordForm(Form):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[])
