from flask import Flask, render_template, request, redirect, flash, url_for
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import Email
# from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG'] = True
users = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="homepage")


class User:
    def __init__(self):
        global users

    def db(self, user_obj):
        user_names = [user["username"] for user in users]
        if user_obj["username"] in user_names:
            return "User already registered"
        users.append(user_obj)
        print(users)
        return "success"

    def user_login(self, user_obj):
        print(users)
        emails = [user["email"] for user in users]
        if user_obj["email"] in emails:
            for user in users:
                if user_obj["password"] == user["password"]:
                    return "success"
                return "wrong username/password combination"
        return "user not found"


class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm')


# form.username.data, form.email.data,form.password.data
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    # print(vars(form))
    if request.method == 'POST' and form.validate():
        user = User()
        db_session = {'username': form.username.data, 'email': form.email.data, 'password': form.password.data}
        register_user = user.db(db_session)
        # print(register_user)
        if register_user == "success":
            flash("Welcome to Shopping App")
            return redirect(url_for('dashboard'))
        return redirect(url_for('signup'))
    return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


class EmailPasswordForm(Form):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[])


@app.route('/login', methods=["GET", "POST"])
def login():
    form = EmailPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        user = User()
        login_data = {"email": form.email.data, "password": form.password.data}
        login_user = user.user_login(login_data)
        if login_user == "success":
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
