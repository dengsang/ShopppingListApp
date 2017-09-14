from flask import Flask, render_template, request, redirect, flash, url_for
from forms import RegistrationForm, TelephoneForm, EmailPasswordForm


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x13\x82\xe8\xf8\rQ\x168\x11\x7fs\x1a\xcaA/k\x83\x18\x19\xe1g?\xf4@\xd1'
app.config['DEBUG'] = True
users = []
items = []


class User:
    def __init__(self):
        global users
        # self.username = username
        # self.email = email
        # self.password = password

    def db(self, user_obj):
        user_names = [user["username"] for user in users]
        if user_obj["username"] in user_names:
            return "User already registered"
        users.append(user_obj)
        # print(users)
        return "success"

    def user_login(self, user_obj):
        # print(users)
        emails = [user["email"] for user in users]
        if user_obj["email"] in emails:
            for user in users:
                if user_obj["password"] == user["password"]:
                    return "success"
                return "wrong username/password combination"
        return "user not found"


class AddList:
    def __init__(self):
        global items
        # self.item = item
        # self.quantity = quantity
        # self.price = price

    def add_list(self, item_obj):
        user_items = [item["item"] for item in items]
        if item_obj["item"] in user_items:
            return "Item already in a list"
        items.append(item_obj)
        # print(items)
        return "success"

    def delete_item(self, item_obj):
        user_items = [item["item"] for item in items]
        if item_obj["item"] in user_items:
            items.clear()
            flash('Item deleted')
            return "success"


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="homepage")


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


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = TelephoneForm(request.form)
    if request.method == 'POST' and form.validate():
        user = AddList()
        db_list = {'item': form.item.data, 'quantity': form.quantity.data, 'price': form.price.data}
        item_list = user.add_list(db_list)
        # print(item_list)
        if item_list == "success":
            flash('Item Added Successfully')
            return redirect(url_for('dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, data=items)


@app.route('/', methods=['GET', 'POST'])
def delete():
    form = TelephoneForm(request.form)
    if request.method == 'POST' and form.validate():
        user = AddList()
        db_list = {'item': form.item.data, 'quantity': form.quantity.data, 'price': form.price.data}
        item_list = user.delete_item(db_list)
        # print(item_list)
        if item_list == "success":
            flash("Item Added Successfully")
            return redirect(url_for('dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, data=items)


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


@app.route('/list_form')
def list_form():
    return render_template('add_list.html', data=items)


if __name__ == '__main__':
    app.run()
