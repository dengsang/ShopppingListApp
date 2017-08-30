from flask import Flask, render_template, request, redirect, flash, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="homepage")


class User:
    def __init__(self):
        self.username = []
        self.email = []
        self.password = []

    def db(self):
        user = {}
        db_session = {'username:', 'email:', 'password:'}
        db_session.update(user)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


# form.username.data, form.email.data,form.password.data
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db_session = {'username:', 'email:', 'password:'}
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        db_session.update(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
